# -*- coding: utf-8 -*-
"""Live checks shared by deploy.py (FTP) and wp.py (WordPress plugin).

A check is critical when failing it means visitors, Google or the rollback
path are hurt; the rest are reported as warnings."""
import re
import time
import urllib.error
import urllib.parse
import urllib.request

PAGE_PATHS = ['/', '/om-os/', '/haandverksgruppen/', '/groen-omstilling/',
              '/arbejdsmiljoe/', '/kontakt/']
# In the footer of every new page, never on the WordPress theme.
NEW_MARKER = 'images/logo-hvid.png'
CANONICAL = 'https://www.hanslarsen.dk'


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **kw):
        return None


def get(url, follow=True, method='GET', headers=None):
    req = urllib.request.Request(url, method=method, headers=dict(
        {'User-Agent': 'hanslarsen-deploy-check', 'Cache-Control': 'no-cache'}, **(headers or {})))
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), (e.read() or b'').decode('utf-8', 'replace')
    except Exception as e:       # DNS, TLS, refused, timeout
        return 0, {}, str(e)


def bust(url):
    return url + ('&' if '?' in url else '?') + 'deploycheck=%d' % (time.time() * 1000)


def header(headers, name):
    for k, v in headers.items():
        if k.lower() == name.lower():
            return v
    return ''


def is_new_site(body):
    return NEW_MARKER in body


def check_page(url, attempts=4, pause=3, sleep=time.sleep):
    last = None
    for i in range(attempts):
        status, _h, body = get(bust(url))
        if status == 200 and is_new_site(body):
            return True, status
        last = status
        if i < attempts - 1:
            sleep(pause)
    return False, last


def local_refs(page_url, body):
    origin = '{0.scheme}://{0.netloc}'.format(urllib.parse.urlsplit(page_url))
    refs = re.findall(r'(?:href|src)="([^"]+)"', body) + re.findall(r"url\(\s*['\"]?([^'\")]+)", body)
    out = set()
    for r in refs:
        if re.match(r'^(mailto:|tel:|data:|#)', r):
            continue
        u = urllib.parse.urljoin(page_url, r).split('#')[0]
        if u.startswith(origin):
            out.add(u)
    return sorted(out)


def run(site, mode, strict=True, say=print, sleep=time.sleep):
    """mode 'ftp': WordPress is closed off.  mode 'wp': WordPress must keep
    answering, because wp-admin is how the plugin gets switched off again."""
    site = site.rstrip('/')
    crit, warn = [], []

    bodies = {}
    for p in PAGE_PATHS:
        ok, info = check_page(site + p, sleep=sleep)
        if ok:
            say('   ok   %s' % p)
            bodies[p] = get(site + p)[2]
        else:
            crit.append('%s -> %s (ny side ikke fundet)' % (p, info))

    # Browsers block http:// stylesheets and scripts on an https page.
    mixed = sorted(p for p, b in bodies.items() if re.search(r'http://(www\.)?hanslarsen\.dk', b))
    if mixed:
        crit.append('http://-links til hanslarsen.dk (mixed content) på: %s' % ', '.join(mixed))

    # Every stylesheet, script, image and internal link on every page.
    checked = {}
    for p, body in bodies.items():
        for u in local_refs(site + p, body):
            if u not in checked:
                checked[u] = get(u, method='HEAD')[0]
                if checked[u] == 405:            # some servers refuse HEAD
                    checked[u] = get(u)[0]
    broken = sorted(u for u, s in checked.items() if s != 200)
    if broken:
        crit.extend('død reference: %s (%s)' % (u, checked[u]) for u in broken)
    elif checked:
        say('   ok   %d billeder, styles og links svarer' % len(checked))

    if mode == 'wp':
        s, _h, _b = get(site + '/wp-login.php')
        (say('   ok   /wp-login.php virker stadig') if s == 200
         else crit.append('/wp-login.php -> %s (så kan pluginet ikke slås fra via admin)' % s))
        s, _h, _b = get(site + '/wp-json/')
        (say('   ok   /wp-json/ virker stadig') if s == 200
         else crit.append('/wp-json/ -> %s' % s))

    if strict:
        url, hops, status = 'http://hanslarsen.dk/', 0, 0
        while hops < 6:
            status, h, _b = get(url, follow=False)
            if status in (301, 302, 307, 308):
                url = urllib.parse.urljoin(url, header(h, 'Location'))
                hops += 1
                continue
            break
        if url.rstrip('/') == CANONICAL and status == 200:
            say('   ok   http://hanslarsen.dk/ -> %s (%d hop)' % (url, hops))
        else:
            crit.append('http://hanslarsen.dk/ ender på %s (HTTP %s) efter %d hop' % (url, status, hops))
        # A deep link on the bare domain must land on www in one hop -- WordPress
        # core did that before, and the plugin now has to.
        s, h, _b = get('https://hanslarsen.dk/om-os/', follow=False)
        target = header(h, 'Location')
        if s == 301 and target == CANONICAL + '/om-os/':
            say('   ok   https://hanslarsen.dk/om-os/ -> www')
        else:
            crit.append('https://hanslarsen.dk/om-os/ gav %s -> %s (forventet 301 til www)' % (s, target or '-'))
        s, h, _b = get(site + '/', follow=False)
        (say('   ok   HSTS-header bevaret') if 'max-age=31536000' in header(h, 'Strict-Transport-Security')
         else warn.append('HSTS-header mangler på forsiden'))

    s, h, _b = get(site + '/hello-world/', follow=False)
    (say('   ok   /hello-world/ omdirigeres') if s == 301
     else warn.append('/hello-world/ gav %s, forventet 301' % s))
    s, _h, b = get(site + '/findes-ikke-%d/' % time.time(), follow=False)
    (say('   ok   egen 404-side') if s == 404 and 'Siden findes ikke' in b
     else warn.append('404-siden: HTTP %s' % s))
    if mode == 'wp':
        s, h, _b = get(site + '/admin', follow=False)
        (say('   ok   /admin fører stadig til wp-admin') if s in (301, 302) and 'wp-' in header(h, 'Location')
         else warn.append('/admin gav %s, forventet omdirigering til wp-admin' % s))
    s, h, _b = get(site + '/index.php', follow=False)
    (say('   ok   /index.php -> forsiden') if s == 301 and header(h, 'Location').rstrip('/') == site
     else warn.append('/index.php gav %s -> %s' % (s, header(h, 'Location') or '-')))
    if mode == 'ftp':
        s, _h, _b = get(site + '/wp-login.php', follow=False)
        (say('   ok   WordPress-login lukket') if s == 403
         else warn.append('/wp-login.php gav %s, forventet 403' % s))
    return crit, warn
