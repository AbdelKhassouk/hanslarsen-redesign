MALERFIRMAET HANS LARSEN — HJEMMESIDE
======================================

Statisk site. Ingen build, ingen afhængigheder — filerne kan uploades som de er.

FILER
-----
  index.html            Forside
  om-os.html            Om os
  kontakt.html          Kontakt
  styles.css            Styling (delt på alle sider)
  script.js             Menu, animationer, formular (delt på alle sider)
  hanslarsenlogo.png    Logo (sort tekst, transparent baggrund)
  sitemap.xml           Til søgemaskiner
  robots.txt            Til søgemaskiner
  .nojekyll             Kun til GitHub Pages-preview — kan slettes ved upload

  images/
    hold.jpg            Fællesbillede — brugt som forsidens hero
    elbil-front.jpg     Elvarebil forfra
    elbil-bag.jpg       Elvarebil bagfra ("Vi maler byen grøn")
    amo-plakat.jpg      Plakat over arbejdsmiljøorganisationen
    logo-hvid.png       Logo i hvid — bruges i den mørke footer
    malermestre.png     Danske Malermestre-mærket
    team/               Portrætter, ét pr. medarbejder

  billeder-original/    De originale, ubeskårne filer fra jer. Bruges ikke af
                        siden — ligger her som arkiv.

  _gen/                 Generator. Se "SÅDAN RETTER DU TEAMET" nedenfor.


SÅDAN TESTER DU LOKALT
----------------------
Dobbeltklik på index.html virker, men brug helst en lille server:

    cd hanslarsen
    python -m http.server 8000

Åbn så http://localhost:8000


SÅDAN RETTER DU TEAMET
----------------------
Medarbejderne står tre steder (forside, om-os, kontakt) og skal være ens.
Derfor findes der en lille generator:

  1. Ret listen TEAM øverst i _gen/partials.py
     - navn, rolle, telefon, e-mail og sti til foto
     - foto=None giver et pænt "Foto på vej"-felt med initialer
     - rækkefølgen i listen er rækkefølgen på siden
  2. Kør:  python _gen/build.py
  3. index.html, om-os.html og kontakt.html er nu opdateret

Vil du hellere rette i hånden, kan du det — HTML'en er helt almindelig.
Husk så at rette alle tre sider.


NÅR DE NYE BILLEDER ER TAGET
----------------------------
Freddy Sørensen og Katrine Lund mangler foto.

  1. Beskær billedet kvadratisk, ca. 400x400 px
  2. Gem som images/team/freddy-soerensen.jpg og images/team/katrine-lund.jpg
  3. Sæt stien ind i _gen/partials.py i stedet for None
  4. Kør python _gen/build.py


INGEN KONTAKTFORMULAR
---------------------
Siden har med vilje ingen formular. Kunder skal ringe eller skrive
direkte — hovednummeret og mailen står i toppen, i bunden og i
"Ring eller skriv til os"-kortet på forsiden og kontaktsiden.
Hver medarbejder har desuden sit eget direkte nummer på sit kort.


HÅNDVERKSGRUPPEN
----------------
Firmaet er en del af Håndverksgruppen. Det står tre steder:

  - Forsiden: en smal stribe under nøgletallene
  - Om os:    sektionen "En del af Håndverksgruppen" med tal og citat
  - Footeren: "EN DEL AF"-logo på alle tre sider

Logoet ligger i to udgaver:
  images/handverksgruppen.svg        til lys baggrund
  images/handverksgruppen-hvid.svg   til den mørke footer

NB: navnet staves "Håndverksgruppen" med v — ikke "Håndværksgruppen".
Sådan staver koncernen selv, også på deres danske sider.

Tal og citat i sektionen kommer fra Håndverksgruppens egen
pressemeddelelse om opkøbet og fra handverksgruppen.com/da.
Ret dem i _gen/partials.py (HG_QUOTE og HG_FACTS), hvis de ændrer sig.


SÅDAN LÆGGER DU DEN ONLINE
--------------------------
Upload alle filer og mapper til roden af webserveren. Alle stier er
relative, så der skal ikke rettes noget.
