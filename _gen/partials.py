# -*- coding: utf-8 -*-
"""Shared building blocks for the three static pages of hanslarsen.dk.

Run _gen/build.py to regenerate index.html, om-os.html and kontakt.html.
The generated files are plain hand-editable HTML; this generator only exists
so the header, nav, footer and the team grid cannot drift apart between pages.
"""

SITE = 'https://www.hanslarsen.dk'

# ---------------------------------------------------------------- icons ---
IC_PHONE = ('<path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 '
            '19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 '
            '2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 '
            '002.81.7A2 2 0 0122 16.92z"/>')
IC_MAIL = ('<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>'
           '<polyline points="22,6 12,13 2,6"/>')
IC_PIN = '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/>'
IC_CLOCK = '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
IC_ARROW = '<path d="M5 12h14M13 5l7 7-7 7"/>'
IC_CHECK = '<path d="M20 6L9 17l-5-5"/>'
IC_EXT = '<path d="M7 17L17 7M17 7H7M17 7V17"/>'
IC_MENU = '<path d="M4 6h16M4 12h16M4 18h16"/>'
IC_CLOSE = '<path d="M6 6l12 12M6 18L18 6"/>'
IC_SHIELD = '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
IC_HEART = '<path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l8.8 8.8 8.8-8.8a5.5 5.5 0 000-7.8z"/>'
IC_USERS = '<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>'
IC_CHAT = '<path d="M21 11.5a8.4 8.4 0 01-9 8.4 8.5 8.5 0 01-3.8-.9L3 21l1.9-5.7A8.4 8.4 0 013.6 11 8.5 8.5 0 0112 3a8.4 8.4 0 019 8.5z"/>'
IC_HANDSHAKE = '<path d="M11 17l2 2a1 1 0 001.4 0l3-3M9 15l2 2M2 12l4-4 5 3 3-3 4 4M22 12l-4 4"/>'


def svg(paths, size=14, sw='2.5', cls=''):
    c = ' class="%s"' % cls if cls else ''
    return ('<svg%s width="%s" height="%s" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="%s" aria-hidden="true">%s</svg>'
            % (c, size, size, sw, paths))


# ----------------------------------------------------------------- team ---
# Order confirmed by the client. Katrine Lund was not part of their numbered
# list, so she is appended last -- move her dict to reorder the whole site.
TEAM = [
    dict(navn='Morten Larsen', rolle='Malermester', tlf='20 77 35 86',
         e164='+4520773586', mail='ml@hanslarsen.dk', foto='images/team/morten-larsen.jpg'),
    dict(navn='Allan Christiansson', rolle='Konduktør', tlf='40 31 35 86',
         e164='+4540313586', mail='ac@hanslarsen.dk', foto='images/team/allan-christiansson.jpg'),
    dict(navn='Rikke Mini Nielsen', rolle='Konduktør', tlf='44 14 35 86',
         e164='+4544143586', mail='rn@hanslarsen.dk', foto='images/team/rikke-mini-nielsen.jpg'),
    dict(navn='Berit Anderson', rolle='Bogholder', tlf='55 72 35 86',
         e164='+4555723586', mail='maler@hanslarsen.dk', foto='images/team/berit-anderson.jpg'),
    dict(navn='Jacob Lundgren', rolle='Formand', tlf='40 97 42 40',
         e164='+4540974240', mail='jl@hanslarsen.dk', foto='images/team/jacob-lundgren.jpg'),
    # Photo not taken yet -- foto=None renders the initials placeholder.
    dict(navn='Freddy Sørensen', rolle='Formand', tlf='29 11 42 40',
         e164='+4529114240', mail='fs@hanslarsen.dk', foto=None),
    dict(navn='Lars Nielsen', rolle='Chauffør', tlf='40 79 35 86',
         e164='+4540793586', mail=None, foto='images/team/lars-nielsen.jpg'),
    dict(navn='Katrine Lund', rolle='Kontorassistent', tlf='55 72 35 86',
         e164='+4555723586', mail='kl@hanslarsen.dk', foto=None),
]


def initials(navn):
    dele = navn.split()
    return (dele[0][0] + dele[-1][0]).upper()


def team_card(p):
    if p['foto']:
        photo = ('<div class="team-photo" style="background-image: url(\'%s\');" '
                 'role="img" aria-label="Foto af %s"></div>' % (p['foto'], p['navn']))
    else:
        photo = ('<div class="team-photo placeholder" role="img" '
                 'aria-label="Foto af %s mangler endnu">'
                 '<span class="initials" aria-hidden="true">%s</span>'
                 '<span class="pending">Foto på vej</span></div>'
                 % (p['navn'], initials(p['navn'])))
    links = ['<a href="tel:%s" aria-label="Ring til %s">%s%s</a>'
             % (p['e164'], p['navn'], svg(IC_PHONE), p['tlf'])]
    if p['mail']:
        links.append('<a href="mailto:%s" aria-label="Send e-mail til %s">%s%s</a>'
                     % (p['mail'], p['navn'], svg(IC_MAIL), p['mail']))
    linkhtml = ('\n' + ' ' * 12).join(links)
    return ('      <article class="team-card">\n'
            '        %s\n'
            '        <div class="team-info">\n'
            '          <h3>%s</h3>\n'
            '          <div class="role">%s</div>\n'
            '          <div class="team-contact-info">\n'
            '            %s\n'
            '          </div>\n'
            '        </div>\n'
            '      </article>' % (photo, p['navn'], p['rolle'], linkhtml))


TEAM_GRID = ('    <div class="team-grid reveal-stagger">\n'
             + '\n'.join(team_card(p) for p in TEAM)
             + '\n    </div>')


def team_section(alt=False, intro=True):
    """The 'Folkene bag' section, identical on all three pages."""
    cls = ' class="alt"' if alt else ''
    lead = ('      <p>Det er os, der tager telefonen, kigger på opgaven og sørger for, at det hele '
            'bliver gjort rigtigt. Du er velkommen til at kontakte os direkte.</p>\n') if intro else ''
    return ('\n<!-- TEAM -->\n'
            '<section%s aria-labelledby="team-title">\n'
            '  <div class="container">\n'
            '    <div class="section-head center reveal">\n'
            '      <span class="section-tag">Vores team</span>\n'
            '      <h2 id="team-title" class="section-title" style="margin-top: 8px;">Folkene bag</h2>\n'
            '%s'
            '    </div>\n'
            '%s\n'
            '  </div>\n'
            '</section>\n' % (cls, lead, TEAM_GRID))


# ------------------------------------------------------------- head/nav ---
def head(title, desc, keywords, canonical, og_title, og_desc, extra_style='', ld=''):
    return '''<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- Primary Meta Tags -->
<title>{title}</title>
<meta name="title" content="{title}">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="author" content="Malerfirmaet Hans Larsen">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:image" content="{site}/images/hold.jpg">
<meta property="og:image:width" content="1260">
<meta property="og:image:height" content="900">
<meta property="og:image:alt" content="Hele holdet fra Malerfirmaet Hans Larsen foran firmaets biler i Næstved">
<meta property="og:locale" content="da_DK">
<meta property="og:site_name" content="Malerfirmaet Hans Larsen">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="{site}/images/hold.jpg">

<!-- Favicon -->
<link rel="icon" type="image/png" href="hanslarsenlogo.png">
<link rel="apple-touch-icon" href="hanslarsenlogo.png">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<meta name="theme-color" content="#D8262C">

<!-- Stylesheet -->
<link rel="stylesheet" href="styles.css">
{extra_style}
<!-- The reveal animations need JS. Without it the page must still be readable. -->
<noscript><style>.reveal,.reveal-left,.reveal-right,.reveal-stagger > *{{opacity:1 !important;transform:none !important;}}</style></noscript>
{ld}</head>
<body>

<a href="#main" class="skip-link">Spring til indhold</a>
'''.format(title=title, desc=desc, keywords=keywords, canonical=canonical,
           og_title=og_title, og_desc=og_desc, site=SITE,
           extra_style=extra_style, ld=ld)


TOPBAR = '''
<!-- TOPBAR -->
<div class="topbar">
  <div class="container topbar-inner">
    <div class="topbar-info">
      <a href="tel:+4555723586" aria-label="Ring til os">
        %s
        55 72 35 86
      </a>
      <a href="mailto:maler@hanslarsen.dk" aria-label="Send os en e-mail">
        %s
        maler@hanslarsen.dk
      </a>
    </div>
    <div class="topbar-extras">
      <span class="topbar-meta">Mandag — fredag · 7:00 — 16:00</span>
      <a href="https://malermestre.dk/" target="_blank" rel="noopener" class="topbar-malermestre" title="Medlem af Danske Malermestre">
        <img src="images/malermestre.png" alt="Danske Malermestre" width="113" height="65" />
      </a>
    </div>
  </div>
</div>
''' % (svg(IC_PHONE), svg(IC_MAIL))


def nav(active):
    def item(href, label):
        if href == active:
            return '      <li><a href="%s" class="active" aria-current="page">%s</a></li>' % (href, label)
        return '      <li><a href="%s">%s</a></li>' % (href, label)
    return '''
<!-- NAV -->
<nav role="navigation" aria-label="Hovednavigation">
  <div class="container nav-inner">
    <a href="index.html" class="logo" aria-label="Forside">
      <div class="logo-mark">
        <img src="hanslarsenlogo.png" alt="Malerfirmaet Hans Larsen" width="660" height="122" />
      </div>
    </a>
    <button class="menu-toggle" id="menuToggle" aria-label="Åbn menu" aria-expanded="false" aria-controls="navMenu">
      %s
      %s
    </button>
    <ul class="nav-menu" id="navMenu">
%s
%s
%s
      <li><a href="kontakt.html" class="nav-cta">Få et tilbud</a></li>
    </ul>
  </div>
</nav>
''' % (svg(IC_MENU, 24, cls='icon-open'), svg(IC_CLOSE, 24, cls='icon-close'),
       item('index.html', 'Forside'), item('om-os.html', 'Om os'),
       item('kontakt.html', 'Kontakt'))


FOOTER = '''
<!-- FOOTER -->
<footer role="contentinfo">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-logo">
          <img src="images/logo-hvid.png" alt="Malerfirmaet Hans Larsen" width="660" height="122" loading="lazy" />
        </div>
        <p>Et af Næstveds ældste malerfirmaer. Grundlagt i 1947 og drevet af Malermester Morten Larsen.</p>
      </div>
      <div class="footer-col">
        <h2>Menu</h2>
        <ul class="footer-list">
          <li><a href="index.html">Forside</a></li>
          <li><a href="om-os.html">Om os</a></li>
          <li><a href="kontakt.html">Kontakt</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>Kontakt</h2>
        <ul class="footer-list">
          <li class="icon-row">
            %s
            <span>Erantisvej 49<br>4700 Næstved</span>
          </li>
          <li class="icon-row">
            %s
            <a href="tel:+4555723586">55 72 35 86</a>
          </li>
          <li class="icon-row">
            %s
            <a href="mailto:maler@hanslarsen.dk">maler@hanslarsen.dk</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-meta">© 1947—2026 Malerfirmaet Hans Larsen · CVR 79099716</div>
      <a href="https://malermestre.dk/" target="_blank" rel="noopener" class="footer-link">
        Medlem af Danske Malermestre
        %s
      </a>
    </div>
  </div>
</footer>

<script src="script.js"></script>
</body>
</html>
''' % (svg(IC_PIN), svg(IC_PHONE), svg(IC_MAIL), svg(IC_EXT, 11, '3'))


MAP_IFRAME = '''<iframe
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2274.846127816702!2d11.77481451308919!3d55.23841843137896!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x4652be63fc358ff1%3A0x42ab8bc99394aec0!2sMalermester%20Hans%20Larsen.%20N%C3%A6stved%20ApS!5e0!3m2!1sda!2sdk!4v1777550130747!5m2!1sda!2sdk"
        allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        title="Find Malerfirmaet Hans Larsen på kortet"></iframe>'''


def contact_info_list(extra_style=''):
    rows = [
        (IC_PHONE, 'Telefon', '<a href="tel:+4555723586">55 72 35 86</a>'),
        (IC_MAIL, 'E-mail', '<a href="mailto:maler@hanslarsen.dk">maler@hanslarsen.dk</a>'),
        (IC_PIN, 'Adresse',
         '<a href="https://maps.google.com/?q=Erantisvej+49,+4700+N%C3%A6stved" '
         'target="_blank" rel="noopener">Erantisvej 49, 4700 Næstved</a>'),
        (IC_CLOCK, 'Åbningstider', 'Mandag — fredag, 7:00 — 16:00'),
    ]
    items = '\n'.join(
        '          <li class="contact-info-item">\n'
        '            <div class="contact-info-icon">\n'
        '              %s\n'
        '            </div>\n'
        '            <div class="contact-info-text">\n'
        '              <small>%s</small>\n'
        '              <strong>%s</strong>\n'
        '            </div>\n'
        '          </li>' % (svg(ic, 18, '2'), label, value)
        for ic, label, value in rows)
    return '        <ul class="contact-info-list"%s>\n%s\n        </ul>' % (extra_style, items)


def form_card():
    return '''      <div class="form-card reveal-right">
        <div id="formContent">
          <h2>Vi ringer dig op</h2>
          <p>Udfyld formularen — så ringer vi dig op inden for 24 timer på hverdage.</p>
          <form id="contactForm" name="kontaktformular">
            <div class="form-row">
              <div class="form-group">
                <label for="name">Navn *</label>
                <input type="text" id="name" name="name" required placeholder="Dit fulde navn" autocomplete="name">
              </div>
              <div class="form-group">
                <label for="phone">Telefon *</label>
                <input type="tel" id="phone" name="phone" required placeholder="55 72 35 86" autocomplete="tel">
              </div>
            </div>
            <div class="form-group">
              <label for="email">E-mail</label>
              <input type="email" id="email" name="email" placeholder="dig@email.dk" autocomplete="email">
            </div>
            <div class="form-group">
              <label for="type">Type opgave</label>
              <select id="type" name="type">
                <option value="">Vælg...</option>
                <option>Privat</option>
                <option>Virksomhed</option>
                <option>Entreprise</option>
                <option>Andet</option>
              </select>
            </div>
            <div class="form-group">
              <label for="message">Beskriv kort hvad det handler om</label>
              <textarea id="message" name="message" placeholder="Fx: indvendig maling af stue og køkken, ca. 50 m²..."></textarea>
            </div>
            <button type="submit" class="form-submit">
              Send forespørgsel
              %s
            </button>
            <p class="form-disclaimer">Vi ringer dig op inden for 24 timer på hverdage. Dine oplysninger bruges kun til at besvare din forespørgsel.</p>
          </form>
        </div>
        <div class="form-success" id="formSuccess" role="status" aria-live="polite">
          <div class="form-success-icon">
            %s
          </div>
          <h2>Tak for din henvendelse!</h2>
          <p>Vi har modtaget din forespørgsel og ringer dig op inden for 24 timer på hverdage.</p>
        </div>
      </div>''' % (svg(IC_ARROW), svg(IC_CHECK, 26))


# --------------------------------------------------- grøn omstilling ------
def groen_section(img, alt, reverse=False):
    rev = ' reverse' if reverse else ''
    points = [
        'Elbiler i vognparken — vi kører ud til opgaverne uden udstødning.',
        'Mindre støj og os i boligkvarterer og på indendørs arbejdspladser.',
        'Grøn omstilling som en del af den daglige drift — ikke som en kampagne.',
    ]
    li = '\n'.join('          <li>%s<span>%s</span></li>' % (svg(IC_CHECK, 17, '2.5'), p)
                   for p in points)
    return '''
<!-- GRØN OMSTILLING -->
<section class="green-band" aria-labelledby="groen-title">
  <div class="container">
    <div class="split%s">
      <div class="split-media portrait reveal-left">
        <img src="%s" alt="%s" loading="lazy" width="900" height="1200">
        <div class="media-badge green">
          <div class="num">EL</div>
          <div class="label">Vognpark</div>
        </div>
      </div>
      <div class="split-content reveal-right">
        <span class="green-tag">Grøn omstilling</span>
        <h2 id="groen-title" class="section-title" style="margin-top: 6px; margin-bottom: 18px;">Vi maler byen grøn</h2>
        <p>Vores vision har siden 1947 været solidt håndværk, der udvikler sig i linje med samfundet. Det gælder også, når vi kører ud til opgaverne.</p>
        <p>Derfor er elbilerne rykket ind i vognparken. Det er den samme maler, der møder op — bare uden udstødning i indkørslen.</p>
        <ul class="green-points">
%s
        </ul>
        <p class="green-quote">„Vi maler byen grøn — fordi vi værdsætter miljøet.”</p>
      </div>
    </div>
  </div>
</section>
''' % (rev, img, alt, li)
