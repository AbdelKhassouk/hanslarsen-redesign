# -*- coding: utf-8 -*-
"""Write index.html, om-os.html, groen-omstilling.html and kontakt.html."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from partials import (SITE, TOPBAR, FOOTER, MAP_IFRAME, TEAM, svg, nav, head,
                      team_section, contact_info_list, contact_cta, groen_teaser,
                      groen_list, hg_section, hg_strip,
                      IC_ARROW, IC_PHONE, IC_CHECK, IC_SHIELD, IC_HEART,
                      IC_USERS, IC_CHAT, IC_HANDSHAKE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write(name, html):
    path = os.path.join(ROOT, name)
    io.open(path, 'w', encoding='utf-8', newline='\n').write(html)
    print('  %-16s %6.1f KB' % (name, os.path.getsize(path) / 1024))


# =========================================================== FORSIDE ======
INDEX_STYLE = '''
<!-- Page-specific styles -->
<style>
.hero { position: relative; }
.hero-inner {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 32px;
  min-height: 520px;
  display: flex;
  align-items: center;
  background: var(--black);
  box-shadow: var(--shadow-lg);
}
.hero-bg {
  position: absolute;
  inset: 0;
  background-image: linear-gradient(90deg, rgba(18,18,18,0.93) 0%, rgba(18,18,18,0.86) 34%, rgba(18,18,18,0.55) 62%, rgba(18,18,18,0.18) 100%),
    url('images/hold.jpg');
  background-size: cover;
  background-position: center 42%;
  transition: transform 8s linear;
}
.hero-inner:hover .hero-bg { transform: scale(1.04); }
.hero-content {
  position: relative;
  z-index: 2;
  color: white;
  padding: 64px 56px;
  max-width: 660px;
}
.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--red);
  color: white;
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 22px;
  border-radius: 4px;
}
.hero h1 {
  font-size: clamp(32px, 4.8vw, 52px);
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.05;
  margin-bottom: 20px;
}
.hero h1 .red { color: var(--red); }
.hero p {
  font-size: 17px;
  max-width: 540px;
  margin-bottom: 28px;
  line-height: 1.6;
  color: rgba(255,255,255,0.9);
}
.hero-actions { display: flex; gap: 12px; flex-wrap: wrap; }
.hero-caption {
  position: absolute;
  right: 22px;
  bottom: 18px;
  z-index: 2;
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 700;
  color: rgba(255,255,255,0.65);
  background: rgba(0,0,0,0.35);
  padding: 6px 12px;
  border-radius: 99px;
  backdrop-filter: blur(4px);
}

/* Stats bar */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  margin-top: -40px;
  position: relative;
  z-index: 3;
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-200);
  overflow: hidden;
}
.stat-item {
  padding: 24px 20px;
  text-align: center;
  border-right: 1px solid var(--gray-200);
}
.stat-item:last-child { border-right: 0; }
.stat-num {
  font-size: 32px;
  font-weight: 800;
  color: var(--red);
  line-height: 1;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}
.stat-label {
  font-size: 12px;
  color: var(--gray-700);
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Services */
.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.service-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 32px 28px;
  transition: all 0.3s var(--transition);
  text-align: center;
}
.service-card:hover {
  border-color: var(--red);
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}
.service-icon {
  width: 60px;
  height: 60px;
  background: var(--red-soft);
  color: var(--red);
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  transition: all 0.3s var(--transition);
}
.service-card:hover .service-icon {
  background: var(--red);
  color: white;
  transform: scale(1.05);
}
.service-card h3 {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 10px;
  letter-spacing: -0.01em;
}
.service-card p {
  color: var(--gray-700);
  font-size: 14px;
  line-height: 1.65;
}

/* Front page contact */
.contact-front-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 48px;
  align-items: start;
}

@media (max-width: 960px) {
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .stat-item:nth-child(2) { border-right: 0; }
  .stat-item:nth-child(1), .stat-item:nth-child(2) { border-bottom: 1px solid var(--gray-200); }
  .services-grid { grid-template-columns: 1fr; gap: 16px; }
  .contact-front-grid { grid-template-columns: 1fr; gap: 32px; }
}

@media (max-width: 760px) {
  .hero-inner { margin-top: 20px; min-height: auto; border-radius: 8px; }
  .hero-bg {
    background-image: linear-gradient(180deg, rgba(18,18,18,0.80) 0%, rgba(18,18,18,0.90) 100%),
      url('images/hold.jpg');
  }
  .hero-content { padding: 48px 28px; }
  .hero-caption { display: none; }
  .stats-bar { margin-top: -20px; grid-template-columns: 1fr 1fr; }
  .stat-num { font-size: 26px; }
  .stat-label { font-size: 11px; }
}
</style>
'''

INDEX_LD = '''<!-- Structured Data: LocalBusiness -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.hanslarsen.dk/",
  "name": "Malerfirmaet Hans Larsen",
  "alternateName": "Malermester Hans Larsen Næstved ApS",
  "description": "Et af Næstveds ældste malerfirmaer. Grundlagt 1947, drevet af Malermester Morten Larsen. Vi løser opgaver for private, virksomheder og større entreprenører.",
  "url": "https://www.hanslarsen.dk/",
  "logo": "https://www.hanslarsen.dk/hanslarsenlogo.png",
  "image": "https://www.hanslarsen.dk/images/hold.jpg",
  "telephone": "+4555723586",
  "email": "maler@hanslarsen.dk",
  "foundingDate": "1947",
  "vatID": "DK79099716",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Erantisvej 49",
    "postalCode": "4700",
    "addressLocality": "Næstved",
    "addressRegion": "Region Sjælland",
    "addressCountry": "DK"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 55.23842,
    "longitude": 11.77481
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "07:00",
    "closes": "16:00"
  },
  "priceRange": "$$",
  "areaServed": [
    { "@type": "City", "name": "Næstved" },
    { "@type": "AdministrativeArea", "name": "Sjælland" },
    { "@type": "City", "name": "København" }
  ],
  "parentOrganization": {
    "@type": "Organization",
    "name": "Håndverksgruppen",
    "url": "https://www.handverksgruppen.com/da"
  },
  "sameAs": [
    "https://malermestre.dk/",
    "https://www.handverksgruppen.com/da"
  ]
}
</script>
'''

SERVICES = [
    ('<path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/>', 'Private kunder',
     'Indvendig og udvendig maling for private hjem i Næstved og omegn — solidt håndværk fra A til Z.'),
    ('<path d="M3 21h18M6 21V8h12v13M9 12h6M9 16h6"/>', 'Virksomheder',
     'Små og mellemstore virksomheder — vi løser opgaver, der holder, og forstyrrer mindst muligt.'),
    ('<path d="M2 22h20M4 22V10l8-6 8 6v12M9 22v-7h6v7M9 7h6"/>', 'Entrepriser',
     'Større entreprenøropgaver i samarbejde med lokale virksomheder og større entreprenører — en stor del foregår ind mod hovedstaden.'),
]

STATS = [('1947', 'Grundlagt'), ('70', 'Malere ansat'),
         ('2', 'Generationer'), ('EL', 'I vognparken')]

index_html = (
    head(
        title='Malerfirmaet Hans Larsen — Malermester i Næstved siden 1947',
        desc='Malerfirmaet Hans Larsen er et af Næstveds ældste malerfirmaer. Grundlagt i 1947 og drevet af Malermester Morten Larsen. Vi løser private opgaver, virksomhedsopgaver og større entrepriser — lokalt og ind mod hovedstaden.',
        keywords='malerfirma næstved, malermester næstved, maler næstved, malerfirma sjælland, hans larsen, entreprenør maler, privat maler, erhvervsmaler',
        canonical=SITE + '/',
        og_title='Malerfirmaet Hans Larsen — Malermester i Næstved siden 1947',
        og_desc='Et af Næstveds ældste malerfirmaer. Grundlagt 1947 og drevet af Malermester Morten Larsen. 70 malere klar til private, virksomheder og større entrepriser.',
        extra_style=INDEX_STYLE, ld=INDEX_LD)
    + TOPBAR
    + nav('index.html')
    + '''
<main id="main">

<!-- HERO -->
<section class="hero" aria-labelledby="hero-title">
  <div class="container">
    <div class="hero-inner reveal">
      <div class="hero-bg" aria-hidden="true"></div>
      <div class="hero-content">
        <div class="hero-tag">Malermester · Næstved siden 1947</div>
        <h1 id="hero-title">Et af Næstveds <span class="red">ældste malerfirmaer</span></h1>
        <p>Grundlagt i 1947 og drevet af Malermester Morten Larsen. Vi er 70 malere, der løser opgaver for private, virksomheder og større entreprenører — lokalt i Næstved og ind mod hovedstaden.</p>
        <div class="hero-actions">
          <a href="kontakt.html" class="btn">
            Få et tilbud
            %s
          </a>
          <a href="tel:+4555723586" class="btn btn-outline">
            %s
            55 72 35 86
          </a>
        </div>
      </div>
      <span class="hero-caption">Hele holdet · Erantisvej 49, Næstved</span>
    </div>
  </div>
</section>
''' % (svg(IC_ARROW), svg(IC_PHONE))
    # ---- stats -----------------------------------------------------------
    + '''
<!-- STATS BAR -->
<section style="padding: 0;" aria-label="Nøgletal">
  <div class="container">
    <div class="stats-bar reveal-stagger">
%s
    </div>
  </div>
</section>
''' % '\n'.join(
        '      <div class="stat-item">\n'
        '        <div class="stat-num">%s</div>\n'
        '        <div class="stat-label">%s</div>\n'
        '      </div>' % (n, l) for n, l in STATS)
    # ---- del af Håndverksgruppen ----------------------------------------
    + hg_strip()
    # ---- om os glimpse ---------------------------------------------------
    + '''
<!-- OM OS -->
<section aria-labelledby="about-title">
  <div class="container">
    <div class="split">
      <div class="split-media portrait reveal-left">
        <img src="images/elbil-front.jpg" alt="Malerfirmaet Hans Larsens elvarebil med firmaets logo" loading="lazy" width="900" height="1200">
        <div class="media-badge">
          <div class="num">1947</div>
          <div class="label">Grundlagt</div>
        </div>
      </div>
      <div class="split-content reveal-right">
        <span class="section-tag">Velkommen</span>
        <h2 id="about-title" class="section-title" style="margin-top: 6px; margin-bottom: 18px;">Solidt håndværk gennem to generationer</h2>
        <p>Malerfirmaet Hans Larsen ApS blev grundlagt i 1947 og bygger på samme vision som ved den spæde start: at sætte kunden i centrum med solidt håndværk, som udvikler sig i linje med samfundet.</p>
        <p>I dag drives firmaet med 70 malere af Malermester Morten Larsen, som har overtaget tøjlerne fra sin far, Malermester Hans Larsen.</p>
        <p>Den udvikling kan man se på vejen: elbilerne er rykket ind i vognparken.</p>
        <a href="om-os.html" class="btn btn-ghost" style="margin-top: 16px;">
          Læs mere om os
          %s
        </a>
      </div>
    </div>
  </div>
</section>
''' % svg(IC_ARROW)
    # ---- services --------------------------------------------------------
    + '''
<!-- HVAD VI LAVER -->
<section class="alt" aria-labelledby="services-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="section-tag">Hvad vi laver</span>
      <h2 id="services-title" class="section-title" style="margin-top: 8px;">Malerarbejde i et bredt spektrum</h2>
      <p>Vi henvender os til private, små og mellemstore virksomheder samt større entreprenører.</p>
    </div>
    <div class="services-grid reveal-stagger">
%s
    </div>
  </div>
</section>
''' % '\n'.join(
        '      <div class="service-card">\n'
        '        <div class="service-icon">\n'
        '          %s\n'
        '        </div>\n'
        '        <h3>%s</h3>\n'
        '        <p>%s</p>\n'
        '      </div>' % (svg(icon, 28, '2'), title, body)
        for icon, title, body in SERVICES)
    # ---- grøn omstilling -------------------------------------------------
    + groen_teaser()
    # ---- team ------------------------------------------------------------
    + team_section(alt=False)
    # ---- kontakt ---------------------------------------------------------
    + '''
<!-- KONTAKT -->
<section class="alt" aria-labelledby="contact-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="section-tag">Kontakt</span>
      <h2 id="contact-title" class="section-title" style="margin-top: 8px;">Skal vi kigge forbi?</h2>
      <p>Giv os et kald eller send en mail — så vender vi tilbage hurtigst muligt.</p>
    </div>
    <div class="contact-front-grid">
      <div class="reveal-left">
%s
        <div class="map-wrap" style="margin-top: 20px;">
          %s
        </div>
      </div>

%s
    </div>
  </div>
</section>

</main>
''' % (contact_info_list(' style="margin-top: 0;"'), MAP_IFRAME, contact_cta('forside-cta'))
    + FOOTER)

# ============================================================= OM OS ======
OMOS_STYLE = '''
<!-- Page-specific styles -->
<style>
.values-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 24px;
}
.value-card {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 18px;
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 6px;
  border-left: 3px solid var(--red);
  transition: all 0.25s var(--transition);
}
.value-card:hover {
  border-color: var(--red);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}
.value-icon {
  width: 40px;
  height: 40px;
  background: var(--red-soft);
  color: var(--red);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.value-card h3 {
  font-size: 15px;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: -0.01em;
}
.value-card p {
  font-size: 13px;
  color: var(--gray-700);
  margin: 0;
  line-height: 1.55;
}

/* Customer types */
.customer-types {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.customer-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 32px 28px;
  text-align: center;
  transition: all 0.3s var(--transition);
}
.customer-card:hover {
  border-color: var(--red);
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}
.customer-card .num {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: var(--red);
  margin-bottom: 12px;
}
.customer-card h3 {
  font-size: 18px;
  font-weight: 800;
  margin-bottom: 10px;
}
.customer-card p {
  color: var(--gray-700);
  font-size: 14px;
  line-height: 1.65;
}

@media (max-width: 960px) {
  .values-grid { grid-template-columns: 1fr; }
  .customer-types { grid-template-columns: 1fr; gap: 16px; }
}
</style>
'''

OMOS_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "name": "Om Malerfirmaet Hans Larsen",
  "description": "Et af Næstveds ældste malerfirmaer, grundlagt 1947 og drevet af Malermester Morten Larsen.",
  "url": "https://www.hanslarsen.dk/om-os/",
  "mainEntity": {
    "@type": "LocalBusiness",
    "name": "Malerfirmaet Hans Larsen",
    "foundingDate": "1947",
    "url": "https://www.hanslarsen.dk/"
  }
}
</script>
'''

VALUES = [
    ('<circle cx="12" cy="12" r="10"/><path d="M9 12l2 2 4-4"/>', 'Kunden i centrum',
     'Samme vision som ved den spæde start i 1947 — kunden i centrum, hver gang.'),
    ('<path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>',
     'Solidt håndværk',
     'Håndværk der holder. Vi pakker ikke sammen, før det er, som det skal være.'),
    ('<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
     'Udvikling i linje med samfundet',
     'Miljøhensyn og teknologi er et naturligt led i hverdagen — ikke en eftertanke.'),
    ('<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>',
     'Medlem af Danske Malermestre',
     'Garanti for kvalitet og fagligt håndværk — gennem brancheforeningen.'),
]

CUSTOMERS = [
    ('01', 'Private kunder', 'Indvendig og udvendig maling for private hjem — i Næstved og omegn.'),
    ('02', 'Virksomheder', 'Små og mellemstore virksomheder — vi tilpasser os arbejdsdagen og forstyrrer mindst muligt.'),
    ('03', 'Entrepriser', 'Større entreprenøropgaver i samarbejde med lokale virksomheder og større entreprenører — en stor del foregår ind mod hovedstaden.'),
]

# The four people on the AMO poster, in the order the poster lists them.
AMO = [
    ('Allan Christiansson', 'Konduktør', 'images/team/allan-christiansson.jpg'),
    ('Rikke Mini Nielsen', 'Konduktør', 'images/team/rikke-mini-nielsen.jpg'),
    ('Jacob Lundgren', 'AMR', 'images/team/jacob-lundgren.jpg'),
    ('Lars Nielsen', 'AMR', 'images/team/lars-nielsen.jpg'),
]

AMO_VALUES = [
    (IC_CHECK, 'Vi står sammen om arbejdsmiljøet'),
    (IC_USERS, 'Samarbejde'),
    (IC_SHIELD, 'Sikkerhed'),
    (IC_HEART, 'Trivsel'),
    (IC_CHAT, 'Åbenhed'),
]

omos_html = (
    head(
        title='Om os — Malerfirmaet Hans Larsen | Næstved siden 1947',
        desc='Læs om Malerfirmaet Hans Larsen — et af Næstveds ældste malerfirmaer. Grundlagt 1947, drevet af Malermester Morten Larsen med 70 ansatte malere og en del af Håndverksgruppen.',
        keywords='om hans larsen, malerfirma næstved historie, morten larsen malermester, malerfirma siden 1947, arbejdsmiljø malerfirma, håndverksgruppen',
        canonical=SITE + '/om-os/',
        og_title='Om os — Malerfirmaet Hans Larsen',
        og_desc='Et af Næstveds ældste malerfirmaer. Grundlagt 1947 og drevet af Malermester Morten Larsen.',
        extra_style=OMOS_STYLE, ld=OMOS_LD)
    + TOPBAR
    + nav('om-os.html')
    + '''
<main id="main">

<section class="page-header">
  <div class="container">
    <span class="page-tag">Om os</span>
    <h1>Et af Næstveds ældste malerfirmaer</h1>
    <p>Grundlagt 1947 og drevet i dag af Malermester Morten Larsen med 70 ansatte malere.</p>
  </div>
</section>

<!-- HISTORIEN -->
<section aria-labelledby="historie-title">
  <div class="container">
    <div class="section-head reveal" style="margin-bottom: 32px;">
      <span class="section-tag">Historien</span>
      <h2 id="historie-title" class="section-title" style="margin-top: 8px;">Solidt håndværk i to generationer</h2>
    </div>
    <figure class="photo-figure reveal">
      <div class="photo-band">
        <img src="images/hold.jpg" alt="Hele holdet fra Malerfirmaet Hans Larsen samlet foran firmaets biler på Erantisvej i Næstved" loading="lazy" width="1260" height="900">
        <div class="media-badge">
          <div class="num">1947</div>
          <div class="label">Grundlagt</div>
        </div>
      </div>
      <figcaption class="photo-caption">Hele holdet samlet foran Erantisvej 49 i Næstved.</figcaption>
    </figure>
    <div class="prose-2col reveal">
      <p>Malerfirmaet Hans Larsen ApS er et af byens ældste malerfirmaer. Firmaet blev grundlagt helt tilbage i 1947 og bygger på nøjagtig samme vision som ved den spæde start: at sætte kunden i centrum med solidt håndværk, som udvikler sig i linje med samfundet.</p>
      <p>I dag drives firmaet med 70 malere af Malermester Morten Larsen, som har overtaget tøjlerne fra sin far, Malermester Hans Larsen.</p>
      <p>Hos Malermester Hans Larsen ApS leverer vi kvalitetsmalerarbejde til både erhverv og private kunder. Vi har mange års erfaring i branchen og lægger stor vægt på faglig stolthed, præcision og godt samarbejde.</p>
      <p>Vi arbejder med alt fra nybyggeri og renoveringer til vedligeholdelsesopgaver, og vi tilpasser altid vores løsninger til den enkelte opgave. For os handler det ikke kun om det færdige resultat – men også om processen undervejs. Derfor lægger vi vægt på god dialog, klare aftaler og overholdelse af deadline.</p>
      <p>Vi er en del af Danske Malermestre og arbejder efter gældende standarder og krav i branchen. Samtidig har vi fokus på arbejdsmiljø og trivsel, så vores medarbejdere altid arbejder under gode og sikre forhold.</p>
      <p>Hos os får du en samarbejdspartner, der tager ansvar – hele vejen fra første kontakt til afleveret arbejde.</p>
    </div>
  </div>
</section>

<!-- VÆRDIER -->
<section class="alt" aria-labelledby="values-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="section-tag">Vores værdier</span>
      <h2 id="values-title" class="section-title" style="margin-top: 8px;">Det vi står for</h2>
    </div>
    <div class="values-grid reveal-stagger" style="max-width: 880px; margin: 0 auto;">
%s
    </div>
  </div>
</section>
''' % '\n'.join(
        '      <div class="value-card">\n'
        '        <div class="value-icon">\n'
        '          %s\n'
        '        </div>\n'
        '        <div>\n'
        '          <h3>%s</h3>\n'
        '          <p>%s</p>\n'
        '        </div>\n'
        '      </div>' % (svg(icon, 20, '2'), title, body)
        for icon, title, body in VALUES)
    # ---- del af Håndverksgruppen ----------------------------------------
    + hg_section()
    # ---- kundetyper ------------------------------------------------------
    + '''
<!-- HVEM VI LØSER OPGAVER FOR -->
<section aria-labelledby="customers-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="section-tag">Hvem vi løser opgaver for</span>
      <h2 id="customers-title" class="section-title" style="margin-top: 8px;">Et bredt spektrum af opgaver</h2>
      <p>Firmaet henvender sig både til det private marked, til små og mellemstore virksomheder og til de større entreprenøropgaver.</p>
    </div>
    <div class="customer-types reveal-stagger">
%s
    </div>
  </div>
</section>
''' % '\n'.join(
        '      <div class="customer-card">\n'
        '        <div class="num">%s</div>\n'
        '        <h3>%s</h3>\n'
        '        <p>%s</p>\n'
        '      </div>' % (num, title, body) for num, title, body in CUSTOMERS)
    # ---- arbejdsmiljøorganisation ---------------------------------------
    + '''
<!-- ARBEJDSMILJØORGANISATION -->
<section class="alt" aria-labelledby="amo-title">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Arbejdsmiljø</span>
      <h2 id="amo-title" class="section-title" style="margin-top: 8px;">Arbejdsmiljøorganisation (AMO)</h2>
      <p class="amo-lead">Vi har en aktiv arbejdsmiljøorganisation (AMO), som arbejder systematisk med at sikre et godt og sikkert arbejdsmiljø for alle medarbejdere.</p>
    </div>
    <div class="amo-intro reveal">
      <p>Arbejdsmiljøorganisationens opgave er blandt andet at forebygge arbejdsulykker og nedslidning, sikre gode arbejdsforhold på byggepladser, følge op på APV og løbende forbedringer samt skabe trivsel og dialog på tværs af organisationen.</p>
      <p>Vi arbejder ud fra den tilgang, at et godt arbejdsmiljø er en forudsætning for høj kvalitet i det arbejde, vi leverer.</p>
    </div>
    <h3 class="amo-subhead reveal">Vores arbejdsmiljøteam</h3>
    <div class="amo-intro reveal">
      <p>Vores arbejdsmiljøorganisation består af engagerede medarbejdere fra virksomheden, som arbejder tæt sammen om at sikre et sikkert og sundt arbejdsmiljø i hverdagen.</p>
      <p>Teamet består af både ledelses- og medarbejderrepræsentanter, som bidrager med input fra byggepladserne og sikrer løbende forbedringer.</p>
    </div>
    <div class="amo-roster reveal-stagger">
%s
    </div>
    <div class="amo-values reveal">
%s
    </div>
    <figure class="amo-figure reveal">
      <a href="images/amo-plakat.jpg" target="_blank" rel="noopener" aria-label="Åbn plakaten over arbejdsmiljøorganisationen i fuld størrelse">
        <img src="images/amo-plakat.jpg" alt="Plakat over arbejdsmiljøorganisationen i Malermester Hans Larsen med Allan Christiansson, Rikke Mini Nielsen, Jacob Lundgren og Lars Nielsen" loading="lazy" width="1326" height="741">
      </a>
      <figcaption>Klik for at se plakaten i fuld størrelse.</figcaption>
    </figure>
  </div>
</section>
''' % ('\n'.join(
        '      <div class="amo-person">\n'
        '        <div class="navn">%s</div>\n'
        '        <div class="rolle">%s</div>\n'
        '      </div>' % (navn, rolle) for navn, rolle, _foto in AMO),
       '\n'.join('      <span%s>%s%s</span>'
                 % (' class="lead"' if i == 0 else '', svg(icon, 16, '2'), label)
                 for i, (icon, label) in enumerate(AMO_VALUES)))
    # ---- team ------------------------------------------------------------
    + team_section(alt=False)
    + '''
<section class="alt compact">
  <div class="container">
    <div style="text-align: center;" class="reveal">
      <a href="kontakt.html" class="btn">
        Kontakt os
        %s
      </a>
    </div>
  </div>
</section>

</main>
''' % svg(IC_ARROW)
    + FOOTER)

# =========================================================== KONTAKT ======
KONTAKT_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": "Kontakt Malerfirmaet Hans Larsen",
  "description": "Kontakt Malerfirmaet Hans Larsen i Næstved. Find adresse, telefon og e-mail.",
  "url": "https://www.hanslarsen.dk/kontakt/",
  "mainEntity": {
    "@type": "LocalBusiness",
    "name": "Malerfirmaet Hans Larsen",
    "telephone": "+4555723586",
    "email": "maler@hanslarsen.dk",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Erantisvej 49",
      "postalCode": "4700",
      "addressLocality": "Næstved",
      "addressCountry": "DK"
    }
  }
}
</script>
'''

# Employee list as structured data -- helps Google show the right person.
KONTAKT_TEAM_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Medarbejdere hos Malerfirmaet Hans Larsen",
  "itemListElement": [
%s
  ]
}
</script>
''' % ',\n'.join(
    '    {\n'
    '      "@type": "ListItem",\n'
    '      "position": %d,\n'
    '      "item": {\n'
    '        "@type": "Person",\n'
    '        "name": "%s",\n'
    '        "jobTitle": "%s",\n'
    '        "telephone": "%s"%s,\n'
    '        "worksFor": { "@type": "Organization", "name": "Malerfirmaet Hans Larsen" }\n'
    '      }\n'
    '    }' % (i + 1, p['navn'], p['rolle'], p['e164'],
                ',\n        "email": "%s"' % p['mail'] if p['mail'] else '')
    for i, p in enumerate(TEAM))

kontakt_html = (
    head(
        title='Kontakt — Malerfirmaet Hans Larsen | Næstved',
        desc='Kontakt Malerfirmaet Hans Larsen i Næstved. Ring direkte til malermester, konduktører, formænd eller kontor — se alle direkte numre og vores adresse på Erantisvej 49.',
        keywords='kontakt malerfirma næstved, hans larsen kontakt, malermester morten larsen, tilbud malerfirma, telefonnummer malerfirma næstved',
        canonical=SITE + '/kontakt/',
        og_title='Kontakt — Malerfirmaet Hans Larsen',
        og_desc='Ring direkte til den, opgaven hører til. Se alle direkte numre hos Malerfirmaet Hans Larsen i Næstved.',
        ld=KONTAKT_LD + KONTAKT_TEAM_LD)
    + TOPBAR
    + nav('kontakt.html')
    + '''
<main id="main">

<section class="page-header">
  <div class="container">
    <span class="page-tag">Kontakt</span>
    <h1>Lad os tale sammen</h1>
    <p>Ring direkte til den, opgaven hører til — eller giv os et kald på hovednummeret, så finder vi den rette.</p>
  </div>
</section>
'''
    # ---- team first: this is what people come to the contact page for ----
    + team_section(alt=False)
    # ---- form + info -----------------------------------------------------
    + '''
<!-- KONTAKT OG ADRESSE -->
<section class="alt" aria-labelledby="skriv-title">
  <div class="container">
    <div class="contact-grid">
      <div class="reveal-left">
        <span class="section-tag">Find os</span>
        <h2 id="skriv-title" class="section-title" style="margin-top: 8px; margin-bottom: 12px;">Vi har til huse i Næstved</h2>
        <p style="color: var(--gray-700); line-height: 1.7; font-size: 15px;">Vi løser opgaver lokalt i Næstved og ind mod hovedstaden. Ring eller skriv — vi er klar til at hjælpe dig.</p>
%s
      </div>

%s
    </div>
  </div>
</section>

<!-- KORT -->
<section aria-labelledby="kort-title">
  <div class="container">
    <div class="section-head reveal">
      <span class="section-tag">Find os</span>
      <h2 id="kort-title" class="section-title" style="margin-top: 8px;">Sådan finder du os</h2>
      <p>Erantisvej 49, 4700 Næstved.</p>
    </div>
    <div class="map-wrap reveal">
      %s
    </div>
  </div>
</section>

</main>
''' % (contact_info_list(), contact_cta('kontakt-cta'), MAP_IFRAME)
    + FOOTER)

# =================================================== GRØN OMSTILLING ======
GROEN_LD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Grøn omstilling — Malermester Hans Larsen ApS",
  "description": "Sådan arbejder Malermester Hans Larsen ApS med grøn omstilling: materialevalg dokumenteret med EPD, minimering af spild, affaldssortering og erfaring fra svanemærket og DGNB-certificeret byggeri.",
  "url": "https://www.hanslarsen.dk/groen-omstilling/",
  "about": {
    "@type": "LocalBusiness",
    "name": "Malerfirmaet Hans Larsen",
    "url": "https://www.hanslarsen.dk/"
  }
}
</script>
'''

# Reference projects, exactly as the client listed them. Only Stenlængegård
# came with a qualifier -- anything else about these projects would be
# invention, so the cards carry the name and nothing more.
REFERENCER = [
    ('DTU Hørsholm', ''),
    ('Lyngby Storcenter / Comwell Hotel', ''),
    ('Daginstitutionen Stenlængegård', 'Opført som svanemærket byggeri'),
]

GROEN_STYLE = '''
<!-- Page-specific styles -->
<style>
.ref-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.ref-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-top: 3px solid var(--hg-green);
  border-radius: 8px;
  padding: 28px 26px;
  transition: all 0.3s var(--transition);
}
.ref-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}
.ref-card h3 {
  font-size: 17px;
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1.35;
}
.ref-icon {
  color: #2E7D5B;
  margin-bottom: 14px;
}
.ref-badge {
  display: inline-block;
  margin-top: 14px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--hg-green-dark);
  background: rgba(100,162,2,0.1);
  border-radius: 99px;
  padding: 6px 12px;
}

@media (max-width: 960px) {
  .ref-grid { grid-template-columns: 1fr; gap: 16px; }
}
</style>
'''

groen_html = (
    head(
        title='Grøn omstilling — Malermester Hans Larsen ApS | Næstved',
        desc='Sådan arbejder Malermester Hans Larsen ApS med grøn omstilling: materialer med lavere miljøpåvirkning dokumenteret med EPD, minimering af spild, korrekt affaldssortering og erfaring fra svanemærket og DGNB-certificeret byggeri.',
        keywords='grøn omstilling malerfirma, bæredygtigt malerarbejde, EPD maling, svanemærket byggeri maler, DGNB maler, miljøvenlig maler næstved',
        canonical=SITE + '/groen-omstilling/',
        og_title='Grøn omstilling — Malermester Hans Larsen ApS',
        og_desc='Grøn omstilling handler for os ikke om enkeltstående tiltag, men om en ansvarlig tilgang i hele processen — fra materialevalg til udførelse og aflevering.',
        extra_style=GROEN_STYLE, ld=GROEN_LD)
    + TOPBAR
    + nav('groen-omstilling.html')
    + '''
<main id="main">

<section class="page-header">
  <div class="container">
    <span class="page-tag">Grøn omstilling</span>
    <h1>Vi maler byen grøn</h1>
    <p>Hos Malermester Hans Larsen ApS arbejder vi aktivt med grøn omstilling som en naturlig del af vores hverdag.</p>
  </div>
</section>

<!-- INTRO -->
<section aria-labelledby="groen-intro-title">
  <div class="container">
    <div class="split">
      <div class="split-media portrait reveal-left">
        <img src="images/elbil-bag.jpg" alt="Grøn elvarebil med teksten „Vi maler byen grøn — fordi vi værdsætter miljøet”" loading="lazy" width="900" height="1200">
        <div class="media-badge green">
          <div class="num">EL</div>
          <div class="label">Vognpark</div>
        </div>
      </div>
      <div class="split-content reveal-right">
        <span class="green-tag">Vores tilgang</span>
        <h2 id="groen-intro-title" class="section-title" style="margin-top: 6px; margin-bottom: 18px;">Ansvarlige løsninger, der holder</h2>
        <p>Vi har fokus på at levere løsninger, der både er holdbare, ansvarlige og tilpasset fremtidens krav.</p>
        <p>Vi vælger, hvor det er muligt, materialer med lavere miljøpåvirkning og samarbejder med leverandører, der kan dokumentere deres produkter gennem f.eks. miljøvaredeklarationer (EPD). Samtidig har vi fokus på korrekt behandling og anvendelse af materialer, så både kvalitet og levetid optimeres.</p>
        <p class="green-quote">„Vi maler byen grøn — fordi vi værdsætter miljøet.”</p>
      </div>
    </div>
  </div>
</section>

<!-- HVAD VI LÆGGER VÆGT PÅ -->
<section class="green-band" aria-labelledby="vaegt-title">
  <div class="container">
    <div class="split reverse">
      <div class="split-media portrait reveal-right">
        <img src="images/elbil-front.jpg" alt="Malermester Hans Larsens hvide elvarebil set forfra" loading="lazy" width="900" height="1200">
      </div>
      <div class="split-content reveal-left">
        <span class="green-tag">I vores arbejde</span>
        <h2 id="vaegt-title" class="section-title" style="margin-top: 6px; margin-bottom: 18px;">Det lægger vi vægt på</h2>
%s
        <h3 class="groen-subhead">I praksis betyder det, at vi</h3>
%s
      </div>
    </div>
  </div>
</section>

<!-- REFERENCER -->
<section aria-labelledby="ref-title">
  <div class="container">
    <div class="section-head center reveal">
      <span class="green-tag">Referencer</span>
      <h2 id="ref-title" class="section-title" style="margin-top: 8px;">Projekter med høje krav til bæredygtighed</h2>
      <p>Vi har erfaring fra projekter med høje krav til bæredygtighed, herunder:</p>
    </div>
    <div class="ref-grid reveal-stagger">
%s
    </div>
    <p class="groen-note reveal">Vi arbejder desuden med dokumentation, der understøtter bæredygtige valg, herunder EPD-data og krav i forbindelse med DGNB-certificerede byggerier.</p>
  </div>
</section>

<!-- AFRUNDING -->
<section class="green-band compact" aria-labelledby="groen-slut-title">
  <div class="container">
    <div class="groen-closing reveal">
      <h2 id="groen-slut-title">Ikke enkeltstående tiltag</h2>
      <p>Grøn omstilling handler for os ikke om enkeltstående tiltag, men om en ansvarlig tilgang i hele processen – fra materialevalg til udførelse og aflevering.</p>
      <a href="kontakt.html" class="btn btn-groen">
        Tal med os om jeres projekt
        %s
      </a>
    </div>
  </div>
</section>

</main>
''' % (
        groen_list([
            'effektiv planlægning for at minimere spild og unødvendig transport',
            'korrekt affaldssortering på byggepladser',
            'anvendelse af produkter, der lever op til gældende miljøkrav',
            'løbende udvikling af vores kompetencer',
        ]),
        groen_list([
            'Rådgiver om materialevalg med fokus på miljø og holdbarhed',
            'Planlægger arbejdet for at minimere spild',
            'Sikrer korrekt udførelse i forhold til både kvalitet og miljø',
        ]),
        '\n'.join(
            '      <div class="ref-card">\n'
            '        %s\n'
            '        <h3>%s</h3>\n'
            '%s'
            '      </div>' % (svg(IC_CHECK, 20, '2.5', 'ref-icon'), navn,
                             '        <span class="ref-badge">%s</span>\n' % badge if badge else '')
            for navn, badge in REFERENCER),
        svg(IC_ARROW))
    + FOOTER)

print('Writing pages:')
write('index.html', index_html)
write('om-os.html', omos_html)
write('groen-omstilling.html', groen_html)
write('kontakt.html', kontakt_html)
