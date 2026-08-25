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


KONTAKTFORMULAR
---------------
Formularen viser en kvittering, men sender ikke e-mail af sig selv.
For at få den til at sende:

  - Formspree (formspree.io) — gratis op til 50 mails/måned
  - Web3Forms (web3forms.com) — gratis
  - Eller jeres egen mailserver

Se kommentaren i script.js under "Form submit handler" — der ligger et
færdigt eksempel, der bare skal have et ID sat ind.


SÅDAN LÆGGER DU DEN ONLINE
--------------------------
Upload alle filer og mapper til roden af webserveren. Alle stier er
relative, så der skal ikke rettes noget.
