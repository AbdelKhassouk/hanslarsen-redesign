#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Put the static site from dist/ on the Curanet webhotel behind www.hanslarsen.dk.

WordPress is never deleted. Every file that gets overwritten is downloaded
first, a canary copy proves the new .htaccess is accepted by the server
before the live one is touched, and if the live site fails its checks
afterwards everything is put back automatically.

  python deploy/deploy.py inspect                 look, change nothing
  python deploy/deploy.py deploy                  dry run: print the plan
  python deploy/deploy.py deploy --yes            do it
  python deploy/deploy.py rollback _backup/<stamp>/manifest.json --yes

Credentials are read from the environment, or from deploy/.deploy-env
(git-ignored, KEY=VALUE per line). They are never printed.

  HL_FTP_HOST   host name from the Curanet panel ("Tekniske oplysninger")
  HL_FTP_USER   FTP user ("Brugere")
  HL_FTP_PASS   FTP password
  HL_FTP_ROOT   optional: web root on the FTP server, auto-detected if unset
"""
import argparse
import datetime as dt
import ftplib
import io
import json
import os
import posixpath
import ssl
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DIST = os.path.join(REPO, 'dist')
BACKUPS = os.path.join(REPO, '_backup')

SITE = checks.CANONICAL
WEBROOT_CANDIDATES = ['www', 'public_html', 'httpdocs', 'html', '.']


def say(msg=''):
    print(msg, flush=True)


# ------------------------------------------------------------ config ------
def load_env():
    # deploy/.deploy-env or .deploy-env in the repo root -- both are git-ignored.
    for path in (os.path.join(HERE, '.deploy-env'), os.path.join(os.path.dirname(HERE), '.deploy-env')):
        if not os.path.isfile(path):
            continue
        for line in io.open(path, encoding='utf-8-sig'):
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    missing = [k for k in ('HL_FTP_HOST', 'HL_FTP_USER', 'HL_FTP_PASS') if not os.environ.get(k)]
    if missing:
        sys.exit('Mangler: %s  (sæt dem som miljøvariabler eller i deploy/.deploy-env)'
                 % ', '.join(missing))
    return os.environ['HL_FTP_HOST'], os.environ['HL_FTP_USER'], os.environ['HL_FTP_PASS']


# ------------------------------------------------------------ remote ------
class SessionReuseFTP_TLS(ftplib.FTP_TLS):
    """ftplib.FTP_TLS that resumes the control channel's TLS session on the
    data channel, as ProFTPD and vsftpd require by default."""

    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname=self.host,
                                            session=self.sock.session)
        return conn, size


class Remote:
    """Thin wrapper over FTP with explicit TLS (what Curanet offers on 21)."""

    def __init__(self, host, user, password, port=21, tls=True, verify_tls=True):
        if not tls and host not in ('127.0.0.1', 'localhost'):
            sys.exit('Ukrypteret FTP er kun tilladt mod localhost.')
        if tls:
            ctx = ssl.create_default_context()
            if not verify_tls:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            self.ftp = SessionReuseFTP_TLS(context=ctx, timeout=60)
        else:
            self.ftp = ftplib.FTP(timeout=60)
        self.ftp.encoding = 'utf-8'
        self.ftp.connect(host, port)
        self.ftp.login(user, password)
        if tls:
            self.ftp.prot_p()
        self.ftp.set_pasv(True)
        self.ftp.voidcmd('TYPE I')

    def close(self):
        try:
            self.ftp.quit()
        except Exception:
            self.ftp.close()

    def is_dir(self, path):
        cur = self.ftp.pwd()
        try:
            self.ftp.cwd(path)
            return True
        except ftplib.error_perm:
            return False
        finally:
            self.ftp.cwd(cur)

    def entries(self, path):
        """{name: 'file'|'dir'} for a directory, or None if it does not exist."""
        try:
            out = {}
            for name, facts in self.ftp.mlsd(path, facts=['type']):
                t = facts.get('type', '')
                if t in ('cdir', 'pdir') or name in ('.', '..'):
                    continue
                out[name] = 'dir' if t == 'dir' else 'file'
            return out
        except ftplib.error_perm:
            # Servers disagree on the code for a missing directory (550, 501,
            # 450) -- and 500/501 can also mean "no MLSD". Ask directly.
            if not self.is_dir(path):
                return None
        # Directory exists but MLSD is unsupported: NLST + CWD probing.
        try:
            names = [posixpath.basename(n) for n in self.ftp.nlst(path)]
        except ftplib.error_perm:
            return None
        return {n: ('dir' if self.is_dir(posixpath.join(path, n)) else 'file')
                for n in names if n not in ('.', '..')}

    def kind(self, path):
        parent, name = posixpath.split(path.rstrip('/'))
        listing = self.entries(parent or '.')
        return None if listing is None else listing.get(name)

    def download(self, remote, local):
        os.makedirs(os.path.dirname(local), exist_ok=True)
        with open(local, 'wb') as fh:
            self.ftp.retrbinary('RETR ' + remote, fh.write)

    def upload(self, local, remote):
        with open(local, 'rb') as fh:
            self.ftp.storbinary('STOR ' + remote, fh)

    def mkdir(self, path):
        self.ftp.mkd(path)

    def delete(self, path):
        self.ftp.delete(path)

    def rmdir(self, path):
        self.ftp.rmd(path)


def join(*parts):
    p = posixpath.join(*[x for x in parts if x not in ('', '.')])
    return p or '.'


def detect_webroot(remote):
    forced = os.environ.get('HL_FTP_ROOT')
    if forced:
        if remote.entries(forced) is None:
            sys.exit('HL_FTP_ROOT=%s findes ikke på serveren.' % forced)
        return forced
    hits = []
    for cand in WEBROOT_CANDIDATES:
        listing = remote.entries(cand)
        if listing and ('wp-config.php' in listing or 'wp-login.php' in listing):
            hits.append(cand)
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit('Kunne ikke finde WordPress-mappen (%s). Sæt HL_FTP_ROOT.'
                 % ', '.join(WEBROOT_CANDIDATES))
    sys.exit('Flere mulige webroots: %s. Sæt HL_FTP_ROOT.' % ', '.join(hits))


# -------------------------------------------------------------- plan ------
def local_files():
    if not os.path.isfile(os.path.join(DIST, 'index.html')) or \
       not os.path.isfile(os.path.join(DIST, '.htaccess')):
        sys.exit('dist/ er ikke bygget. Kør:  python _gen/build.py --prod')
    files = []
    for dirpath, _dirs, names in os.walk(DIST):
        for n in names:
            full = os.path.join(dirpath, n)
            files.append(os.path.relpath(full, DIST).replace(os.sep, '/'))

    def order(rel):
        # Assets first, so no page ever appears without its CSS and images;
        # the home page next to last; .htaccess -- the actual switch -- last.
        if rel == '.htaccess':
            return (4, rel)
        if rel == 'index.html':
            return (3, rel)
        if rel.endswith('.html'):
            return (2, rel)
        return (1, rel)
    return sorted(files, key=order)


def build_plan(remote, root):
    plan, dir_cache = [], {}

    def listing(d):
        if d not in dir_cache:
            dir_cache[d] = remote.entries(d)
        return dir_cache[d]

    for rel in local_files():
        rdir = join(root, posixpath.dirname(rel))
        entries = listing(rdir)
        exists = entries is not None and entries.get(posixpath.basename(rel)) == 'file'
        if entries is not None and entries.get(posixpath.basename(rel)) == 'dir':
            sys.exit('Konflikt: %s er en mappe på serveren.' % join(root, rel))
        plan.append({'rel': rel, 'remote': join(root, rel), 'overwrite': exists})
    return plan


# ---------------------------------------------------------- manifest ------
class Manifest:
    def __init__(self, path, data=None):
        self.path = path
        self.data = data or {}

    @classmethod
    def new(cls, stamp, host, root):
        d = os.path.join(BACKUPS, stamp)
        os.makedirs(d, exist_ok=True)
        m = cls(os.path.join(d, 'manifest.json'), {
            'stamp': stamp, 'host': host, 'root': root, 'status': 'started',
            'created_dirs': [], 'created_files': [], 'overwritten': [],
        })
        m.save()
        return m

    @classmethod
    def load(cls, path):
        return cls(path, json.load(io.open(path, encoding='utf-8')))

    @property
    def dir(self):
        return os.path.dirname(self.path)

    def save(self):
        tmp = self.path + '.tmp'
        json.dump(self.data, io.open(tmp, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
        os.replace(tmp, self.path)


# ----------------------------------------------------------- actions ------
def ensure_dirs(remote, root, rel, manifest):
    parts = posixpath.dirname(rel).split('/') if posixpath.dirname(rel) else []
    cur = root
    for part in parts:
        cur = join(cur, part)
        if remote.kind(cur) is None:
            remote.mkdir(cur)
            if manifest is not None:
                manifest.data['created_dirs'].append(cur)
                manifest.save()


def canary(remote, root, site, stamp):
    """Serve the new .htaccess from a throwaway folder first. If the host
    rejects a directive, only that folder returns 500 -- not the live site."""
    folder = '_deploytest_%s' % stamp
    base = join(root, folder)
    subset = ['.htaccess', 'styles.css', 'script.js', 'index.html', 'om-os/index.html',
              'images/hold.jpg', 'images/logo-hvid.png']
    say('\n[canary] tester den nye .htaccess i /%s/ ...' % folder)
    made_dirs, made_files = [], []
    try:
        remote.mkdir(base)
        made_dirs.append(base)
        for rel in subset:
            d = posixpath.dirname(rel)
            if d:
                cur = base
                for part in d.split('/'):
                    cur = join(cur, part)
                    if remote.kind(cur) is None:
                        remote.mkdir(cur)
                        made_dirs.append(cur)
            remote.upload(os.path.join(DIST, rel), join(base, rel))
            made_files.append(join(base, rel))
        failures = []
        for p in ('/', '/om-os/'):
            ok, info = checks.check_page(site + '/' + folder + p, attempts=3, pause=2, sleep=time.sleep)
            (say('   ok   /%s%s' % (folder, p)) if ok
             else failures.append('/%s%s -> %s' % (folder, p, info)))
        status, _h, _b = checks.get(checks.bust(site + '/' + folder + '/styles.css'))
        (say('   ok   /%s/styles.css' % folder) if status == 200
         else failures.append('/%s/styles.css -> %s' % (folder, status)))
        return failures
    finally:
        for f in reversed(made_files):
            try:
                remote.delete(f)
            except ftplib.Error:
                pass
        for d in sorted(made_dirs, key=len, reverse=True):
            try:
                remote.rmdir(d)
            except ftplib.Error:
                pass
        say('   canary-mappen er fjernet igen')


def do_rollback(remote, manifest):
    say('\n[rollback] lægger den gamle side på plads ...')
    # Old .htaccess first: that alone hands routing back to WordPress.
    over = sorted(manifest.data['overwritten'], key=lambda o: o['remote'] != join(manifest.data['root'], '.htaccess'))
    for o in over:
        remote.upload(os.path.join(manifest.dir, 'overwritten', o['rel']), o['remote'])
        say('   gendannet  %s' % o['remote'])
    for f in reversed(manifest.data['created_files']):
        try:
            remote.delete(f)
        except ftplib.error_perm as e:
            say('   ADVARSEL kunne ikke slette %s: %s' % (f, e))
    say('   slettet    %d nye filer' % len(manifest.data['created_files']))
    for d in sorted(manifest.data['created_dirs'], key=len, reverse=True):
        try:
            remote.rmdir(d)
        except ftplib.error_perm as e:
            say('   ADVARSEL kunne ikke fjerne mappe %s: %s' % (d, e))
    manifest.data['status'] = 'rolled-back'
    manifest.data['rolled_back_at'] = dt.datetime.now().isoformat(timespec='seconds')
    manifest.save()


def cmd_inspect(args):
    host, user, pw = load_env()
    remote = connect(args, host, user, pw)
    try:
        root = detect_webroot(remote)
        listing = remote.entries(root)
        say('Forbundet til %s  (bruger skjult)' % host)
        say('Webroot: %s' % root)
        say('WordPress fundet: %s' % ('ja' if 'wp-config.php' in listing else 'nej'))
        say('\nIndhold i webroot:')
        for name in sorted(listing, key=lambda n: (listing[n] != 'dir', n.lower())):
            say('   %s %s' % ('[mappe]' if listing[name] == 'dir' else '       ', name))
        if listing.get('.htaccess') == 'file':
            buf = io.BytesIO()
            remote.ftp.retrbinary('RETR ' + join(root, '.htaccess'), buf.write)
            say('\nNuværende .htaccess:\n' + '-' * 60)
            say(buf.getvalue().decode('utf-8', 'replace').rstrip())
            say('-' * 60)
        plan = build_plan(remote, root)
        over = [p['remote'] for p in plan if p['overwrite']]
        say('\nNye filer der vil blive lagt op: %d' % sum(1 for p in plan if not p['overwrite']))
        say('Eksisterende filer der vil blive overskrevet (med backup): %d' % len(over))
        for o in over:
            say('   ' + o)
    finally:
        remote.close()


def cmd_deploy(args):
    host, user, pw = load_env()
    remote = connect(args, host, user, pw)
    site = args.site_url.rstrip('/')
    strict = not args.local
    try:
        root = detect_webroot(remote)
        plan = build_plan(remote, root)
        over = [p for p in plan if p['overwrite']]
        say('Webroot:           %s' % root)
        say('Filer i alt:       %d' % len(plan))
        say('  nye:             %d' % (len(plan) - len(over)))
        say('  overskrives:     %d  (backup tages først)' % len(over))
        for p in over:
            say('                   %s' % p['remote'])
        say('Slettes:           ingen — WordPress bliver liggende')
        say('Tjekkes bagefter:  %s' % site)
        if not args.yes:
            say('\nTØRKØRSEL — intet er ændret. Kør igen med --yes for at gøre det.')
            return 0

        stamp = dt.datetime.now().strftime('%Y%m%d-%H%M%S')
        manifest = Manifest.new(stamp, host, root)
        say('\nBackup og manifest: %s' % os.path.relpath(manifest.dir, REPO))

        # 1. Back up everything that is about to be overwritten.
        for p in over:
            local = os.path.join(manifest.dir, 'overwritten', p['rel'])
            remote.download(p['remote'], local)
            manifest.data['overwritten'].append({'rel': p['rel'], 'remote': p['remote']})
            manifest.save()
            say('   backup     %s' % p['remote'])

        # 2. Prove the .htaccess works on this host before touching the live one.
        if not args.skip_canary:
            failures = canary(remote, root, site, stamp)
            if failures:
                manifest.data['status'] = 'aborted-canary'
                manifest.data['canary_failures'] = failures
                manifest.save()
                say('\nAFBRUDT før noget blev ændret. Canary fejlede:')
                for f in failures:
                    say('   ' + f)
                return 2

        # 3. Upload. Assets, then subpages, then home, then .htaccess.
        say('\n[upload]')
        for p in plan:
            ensure_dirs(remote, root, p['rel'], manifest)
            if not p['overwrite']:
                manifest.data['created_files'].append(p['remote'])
                manifest.save()
            remote.upload(os.path.join(DIST, p['rel']), p['remote'])
            say('   %s  %s' % ('overskrev' if p['overwrite'] else 'ny       ', p['remote']))
        manifest.data['status'] = 'uploaded'
        manifest.save()

        # 4. Check the live site. Anything critical failing puts it all back.
        say('\n[tjek af live-siden]')
        crit, warn = checks.run(site, 'ftp', strict=strict, say=say, sleep=time.sleep)
        for w in warn:
            say('   ADVARSEL  ' + w)
        if crit:
            say('\nKRITISK FEJL — ruller tilbage:')
            for c in crit:
                say('   ' + c)
            manifest.data['verify_failures'] = crit
            do_rollback(remote, manifest)
            status, _h, body = checks.get(checks.bust(site + '/'))
            say('\nForsiden efter rollback: HTTP %s, %s' % (
                status, 'den gamle side er tilbage' if not checks.is_new_site(body) else 'TJEK MANUELT'))
            return 3

        manifest.data['status'] = 'deployed'
        manifest.data['warnings'] = warn
        manifest.data['deployed_at'] = dt.datetime.now().isoformat(timespec='seconds')
        manifest.save()
        say('\nFÆRDIG. Den nye side er live på %s' % site)
        say('Fortryd når som helst med:')
        say('   python deploy/deploy.py rollback %s --yes'
            % os.path.relpath(manifest.path, REPO).replace(os.sep, '/'))
        return 0
    finally:
        remote.close()


def cmd_rollback(args):
    manifest = Manifest.load(args.manifest)
    say('Manifest:    %s' % args.manifest)
    say('Status:      %s' % manifest.data.get('status'))
    say('Gendannes:   %d filer' % len(manifest.data['overwritten']))
    say('Slettes:     %d filer, %d mapper (kun dem deploy lagde op)'
        % (len(manifest.data['created_files']), len(manifest.data['created_dirs'])))
    if manifest.data.get('status') == 'rolled-back':
        say('Denne deploy er allerede rullet tilbage.')
        return 0
    if not args.yes:
        say('\nTØRKØRSEL — intet er ændret. Kør igen med --yes.')
        return 0
    host, user, pw = load_env()
    remote = connect(args, host, user, pw)
    try:
        do_rollback(remote, manifest)
    finally:
        remote.close()
    say('Rullet tilbage.')
    return 0


def connect(args, host, user, pw):
    return Remote(host, user, pw, port=args.port, tls=not args.no_tls,
                  verify_tls=not args.insecure_tls)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', type=int, default=21)
    ap.add_argument('--site-url', default=SITE, help='hvor live-tjekket kigger (standard: %(default)s)')
    ap.add_argument('--no-tls', action='store_true', help=argparse.SUPPRESS)
    ap.add_argument('--insecure-tls', action='store_true', help=argparse.SUPPRESS)
    ap.add_argument('--local', action='store_true', help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('inspect')
    d = sub.add_parser('deploy')
    d.add_argument('--yes', action='store_true')
    d.add_argument('--skip-canary', action='store_true', help=argparse.SUPPRESS)
    r = sub.add_parser('rollback')
    r.add_argument('manifest')
    r.add_argument('--yes', action='store_true')
    args = ap.parse_args(argv)
    return {'inspect': cmd_inspect, 'deploy': cmd_deploy, 'rollback': cmd_rollback}[args.cmd](args) or 0


if __name__ == '__main__':
    sys.exit(main())
