#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Switch www.hanslarsen.dk over to the new site through WordPress itself.

The site ships as a plugin (dist-wp/hanslarsen-site.zip). It is uploaded
once in wp-admin; this script then turns it on, checks the live site, and
turns it straight back off again if anything critical fails. Nothing in
WordPress is deleted or edited -- deactivating the plugin is the rollback.

  python deploy/wp.py status                  who am I, is the plugin there
  python deploy/wp.py check                   run the live checks only
  python deploy/wp.py activate                dry run
  python deploy/wp.py activate --yes          switch to the new site
  python deploy/wp.py deactivate --yes        switch back to WordPress

Credentials: an application password, not the WordPress login password.
Create one in wp-admin under Brugere -> Profil -> Adgangskoder til
applikationer, then put it in deploy/.deploy-env (git-ignored):

  HL_WP_USER=admin
  HL_WP_APP_PASSWORD=abcd efgh ijkl mnop qrst uvwx
  HL_WP_URL=https://www.hanslarsen.dk          (optional)

Revoke it in the same place when the job is done.
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402

PLUGIN = 'hanslarsen-site/hanslarsen-site'
ZIP = os.path.join(os.path.dirname(HERE), 'dist-wp', 'hanslarsen-site.zip')
SOURCE = os.path.join(os.path.dirname(HERE), '_gen', 'wp-plugin', 'hanslarsen-site.php')
THEME_MARKER = '/wp-content/themes/'


def expected_version():
    """Version in the plugin source -- the one the zip was built from."""
    m = re.search(r'^\s*\*\s*Version:\s*(\S+)', io.open(SOURCE, encoding='utf-8').read(), re.M)
    return m.group(1) if m else None


def old_site_is_back(body, before):
    """WordPress' theme is showing again. Requiring the theme marker (when the
    page had one before) keeps a coming-soon page from passing as "back"."""
    if checks.is_new_site(body):
        return False
    return THEME_MARKER in body if THEME_MARKER in before else True


def say(msg=''):
    print(msg, flush=True)


def load_env():
    # deploy/.deploy-env or .deploy-env in the repo root -- both are git-ignored.
    for path in (os.path.join(HERE, '.deploy-env'), os.path.join(os.path.dirname(HERE), '.deploy-env')):
        if not os.path.isfile(path):
            continue
        for line in io.open(path, encoding='utf-8-sig'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    missing = [k for k in ('HL_WP_USER', 'HL_WP_APP_PASSWORD') if not os.environ.get(k)]
    if missing:
        sys.exit('Mangler: %s  (se toppen af deploy/wp.py)' % ', '.join(missing))
    url = os.environ.get('HL_WP_URL', checks.CANONICAL).rstrip('/')
    return url, os.environ['HL_WP_USER'], os.environ['HL_WP_APP_PASSWORD']


class WP:
    def __init__(self, url, user, app_password):
        self.url = url
        token = base64.b64encode(('%s:%s' % (user, app_password)).encode()).decode()
        self.auth = 'Basic ' + token

    def call(self, method, route, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            self.url + '/wp-json' + route, data=data, method=method,
            headers={'Authorization': self.auth, 'Content-Type': 'application/json',
                     'User-Agent': 'hanslarsen-deploy'})
        try:
            # Never follow redirects: urllib would quietly resend a POST as a
            # GET, and the plugin status would never change.
            with urllib.request.build_opener(checks._NoRedirect).open(req, timeout=60) as r:
                return r.status, json.loads(r.read().decode('utf-8') or 'null')
        except urllib.error.HTTPError as e:
            if 300 <= e.code < 400:
                return e.code, {'message': 'WordPress omdirigerede til %s — brug præcis %s'
                                % (checks.header(dict(e.headers or {}), 'Location'), checks.CANONICAL)}
            raw = (e.read() or b'').decode('utf-8', 'replace')
            try:
                return e.code, json.loads(raw)
            except ValueError:
                return e.code, {'message': raw[:300]}
        except urllib.error.URLError as e:
            sys.exit('Kan ikke nå %s: %s' % (self.url, e.reason))

    def me(self):
        return self.call('GET', '/wp/v2/users/me?context=edit')

    def plugins(self):
        return self.call('GET', '/wp/v2/plugins')

    def plugin(self):
        status, data = self.call('GET', '/wp/v2/plugins/' + PLUGIN)
        return data if status == 200 else None

    def set_status(self, active):
        return self.call('POST', '/wp/v2/plugins/' + PLUGIN,
                         {'status': 'active' if active else 'inactive'})


def authenticate(wp):
    status, me = wp.me()
    if status == 401:
        sys.exit('Login afvist. Tjek HL_WP_USER og HL_WP_APP_PASSWORD '
                 '(det skal være en applikationsadgangskode, ikke den normale).')
    if status != 200:
        sys.exit('Uventet svar fra WordPress (%s): %s' % (status, me.get('message', me)))
    caps = me.get('capabilities', {})
    if not caps.get('activate_plugins'):
        sys.exit('Brugeren "%s" må ikke aktivere plugins. Der skal bruges en administrator.'
                 % me.get('slug'))
    return me


def wait_until(predicate, attempts=6, pause=2, sleep=time.sleep):
    for i in range(attempts):
        if predicate():
            return True
        if i < attempts - 1:
            sleep(pause)
    return False


def cmd_status(args, wp):
    me = authenticate(wp)
    say('WordPress:     %s' % wp.url)
    say('Logget ind som %s (%s)' % (me.get('slug'), ', '.join(me.get('roles', []))))
    status, plugins = wp.plugins()
    if status == 200:
        names = {p['plugin']: p for p in plugins}
        caches = [p['name'] for p in plugins if p['status'] == 'active' and
                  any(k in p['plugin'] for k in ('litespeed', 'rocket', 'w3-total', 'super-cache'))]
        say('Aktive plugins: %d  %s' % (sum(1 for p in plugins if p['status'] == 'active'),
                                        ('(cache: %s)' % ', '.join(caches)) if caches else ''))
        p = names.get(PLUGIN)
    else:
        p = wp.plugin()
    if not p:
        say('\nPluginet er IKKE uploadet endnu.')
        say('Upload %s under Plugins -> Tilføj nyt -> Upload plugin' % os.path.relpath(ZIP))
        say('(lad være med at aktivere det der — det gør "activate --yes").')
        return 1
    say('\nPlugin:        %s %s' % (p['name'], p['version']))
    say('Status:        %s' % ('AKTIVT — den nye side vises' if p['status'] == 'active'
                               else 'inaktivt — WordPress-siden vises'))
    return 0


def cmd_check(args, wp=None):
    site = args.site_url.rstrip('/') if args.site_url else wp.url
    say('Tjekker %s ...' % site)
    crit, warn = checks.run(site, 'wp', strict=not args.local, say=say)
    for w in warn:
        say('   ADVARSEL  ' + w)
    for c in crit:
        say('   KRITISK   ' + c)
    say('\n%s' % ('Alt kritisk er i orden.' if not crit else '%d kritiske fejl.' % len(crit)))
    return 0 if not crit else 3


def cmd_activate(args, wp):
    authenticate(wp)
    p = wp.plugin()
    if not p:
        sys.exit('Pluginet er ikke uploadet. Upload %s i wp-admin først.' % os.path.relpath(ZIP))
    want = expected_version()
    if want and p['version'] != want:
        sys.exit('Den uploadede version er %s, men den nye er %s.\n'
                 'Upload %s igen i wp-admin (Plugins -> Tilføj nyt -> Upload plugin ->\n'
                 '"Erstat den nuværende med den uploadede") og lad den være inaktiv.'
                 % (p['version'], want, os.path.relpath(ZIP)))
    site = args.site_url.rstrip('/') if args.site_url else wp.url
    strict = not args.local
    say('Plugin:   %s %s (%s)' % (p['name'], p['version'], p['status']))
    say('Side:     %s' % site)
    say('Plan:     aktivér -> tjek live -> deaktivér automatisk ved kritisk fejl')
    if not args.yes:
        say('\nTØRKØRSEL — intet er ændret. Kør igen med --yes.')
        return 0

    before_status, _h, before = checks.get(checks.bust(site + '/'))
    if p['status'] != 'active':
        status, data = wp.set_status(True)
        if status != 200 or data.get('status') != 'active':
            say('Kunne ikke aktivere (%s): %s' % (status, data.get('message', data)))
            return 2
        say('\nAktiveret.')
    else:
        say('\nPluginet var allerede aktivt — tjekker bare.')

    say('\n[tjek af live-siden]')
    crit, warn = checks.run(site, 'wp', strict=strict, say=say)
    for w in warn:
        say('   ADVARSEL  ' + w)
    if not crit:
        say('\nFÆRDIG. Den nye side er live på %s' % site)
        say('Fortryd: python deploy/wp.py deactivate --yes   (eller "Deaktivér" i wp-admin)')
        return 0

    say('\nKRITISK FEJL — slår pluginet fra igen:')
    for c in crit:
        say('   ' + c)
    status, data = wp.set_status(False)
    if status != 200 or data.get('status') != 'inactive':
        say('KUNNE IKKE SLÅ PLUGINET FRA (%s): %s' % (status, data.get('message', data)))
        say('Gør det NU i wp-admin: Plugins -> "Hans Larsen — ny hjemmeside" -> Deaktivér')
        return 4
    back = wait_until(lambda: old_site_is_back(checks.get(checks.bust(site + '/'))[2], before))
    s, _h, _b = checks.get(checks.bust(site + '/'))
    say('Deaktiveret. Forsiden: HTTP %s, %s' % (
        s, 'den gamle side er tilbage' if back else 'TJEK FORSIDEN MANUELT FRA ET ANDET NETVÆRK'))
    if s != before_status:
        say('ADVARSEL: forsiden svarede HTTP %s før og HTTP %s nu.' % (before_status, s))
    return 3


def cmd_deactivate(args, wp):
    authenticate(wp)
    p = wp.plugin()
    if not p:
        say('Pluginet er ikke installeret — WordPress-siden vises allerede.')
        return 0
    if p['status'] != 'active':
        say('Pluginet er allerede slået fra.')
        return 0
    if not args.yes:
        say('TØRKØRSEL — kør igen med --yes for at vise WordPress-siden igen.')
        return 0
    status, data = wp.set_status(False)
    if status != 200 or data.get('status') != 'inactive':
        say('Kunne ikke deaktivere (%s): %s' % (status, data.get('message', data)))
        say('Gør det i wp-admin: Plugins -> "Hans Larsen — ny hjemmeside" -> Deaktivér')
        return 2
    site = args.site_url.rstrip('/') if args.site_url else wp.url
    back = wait_until(lambda: not checks.is_new_site(checks.get(checks.bust(site + '/'))[2]))
    say('Deaktiveret. %s' % ('WordPress-siden vises igen.' if back else
                             'Forsiden viser stadig den nye side — tøm cachen i wp-admin.'))
    return 0 if back else 4


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--site-url', help=argparse.SUPPRESS)
    ap.add_argument('--local', action='store_true', help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('status')
    sub.add_parser('check')
    for name in ('activate', 'deactivate'):
        sub.add_parser(name).add_argument('--yes', action='store_true')
    args = ap.parse_args(argv)
    if args.cmd == 'check' and args.site_url:
        return cmd_check(args)
    url, user, pw = load_env()
    if not args.local and not url.startswith('https://'):
        sys.exit('HL_WP_URL skal starte med https:// — applikationsadgangskoden sendes med hver forespørgsel.')
    wp = WP(url, user, pw)
    return {'status': cmd_status, 'check': cmd_check, 'activate': cmd_activate,
            'deactivate': cmd_deactivate}[args.cmd](args, wp)


if __name__ == '__main__':
    sys.exit(main())
