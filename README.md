# Malerfirmaet Hans Larsen — redesign

Preview: **https://abdelkhassouk.github.io/hanslarsen-redesign/**

Statisk site på seks sider, bygget fra `_gen/` med `python _gen/build.py`.

> **Skal siden på hanslarsen.dk?** Følg [deploy/SKIFT-TIL-NY-SIDE.md](deploy/SKIFT-TIL-NY-SIDE.md).
> Upload aldrig filerne fra repo-roden — de er GitHub-preview'et og har `noindex`.

| Side | Adresse |
|---|---|
| Forside | `/` |
| Om os | `/om-os/` |
| Håndverksgruppen | `/haandverksgruppen/` |
| Grøn omstilling | `/groen-omstilling/` |
| Arbejdsmiljø (AMO) | `/arbejdsmiljoe/` |
| Kontakt | `/kontakt/` |

Siderne ligger som mapper (`om-os/index.html`), så adresserne er de samme,
som WordPress-siden brugte, og som Google allerede kender.

## Tre byggemål

| Kommando | Mål | Bruges til |
|---|---|---|
| `python _gen/build.py` | repo-roden | GitHub-preview'et (`noindex`) |
| `python _gen/build.py --prod` | `dist/` | FTP-upload til webhotellet |
| `python _gen/build.py --wp-plugin` | `dist-wp/hanslarsen-site.zip` | WordPress-plugin |

Håndverksgruppen, Grøn omstilling og Arbejdsmiljø har hver sin side, som
kunden bad om. De krydslinker til hinanden gennem "Læs også"-kortene
nederst, og de står alle i menuen og i footeren.

Menuen klapper sammen til hamburger-ikonet allerede ved 1040 px — seks
punkter kan ikke stå ved siden af logoet på en mindre bærbar.

## Hvad er nyt

**Billeder.** Fællesbilledet er nu forsidens hero i stedet for et stockfoto,
og det fylder hele bredden på "Om os". De to elbiler bærer en ny sektion,
*Grøn omstilling*, på både forside og "Om os". AMO-plakaten ligger på "Om os"
med en læsbar HTML-udgave ved siden af, så den også virker på mobil.
Alle billeder ligger lokalt — siden henter ikke længere fra `wp-content`.

**Team.** Ny rækkefølge, og to nye kolleger:

1. Morten Larsen — Malermester
2. Allan Christiansson — Konduktør
3. Rikke Mini Nielsen — Konduktør
4. Berit Anderson — Bogholder
5. Jacob Lundgren — Formand
6. **Freddy Sørensen — Formand** *(nyt)*
7. Lars Nielsen — Chauffør
8. **Katrine Lund — Kontorassistent** *(nyt)*

Freddy og Katrine har et "Foto på vej"-felt med initialer, indtil billederne
er taget. Katrine stod ikke i den udleverede rækkefølge, så hun er sat sidst
— sig til, hvis hun skal et andet sted hen.

## Grøn omstilling

Grøn omstilling har fået sin egen side og sit eget punkt i menuen — indholdet
rummer nu arbejdsgange, dokumentation (EPD, DGNB) og tre referenceprojekter,
og det er for meget til en sektion. Forsiden har en kort teaser, der linker
videre.

Referenceprojekterne står i `REFERENCER` i `_gen/build.py` og indeholder
**kun projektnavnet** — plus kundens egen tilføjelse om at Stenlængegård er
svanemærket byggeri. Skal der stå mere om et projekt, skal teksten komme fra
jer; den skal ikke gættes.

## En del af Håndverksgruppen

Firmaet er en del af **Håndverksgruppen**. Det har sin egen side, plus en
stribe på forsiden og et logo i footeren på alle sider. Brødteksten er
kundens egen, ordret.

> Navnet staves **Håndverksgruppen** med *v* — det er koncernens egen
> stavemåde, også på deres danske sider.

Tallene på faktakortet (160+ virksomheder, 4.700 medarbejdere, 4 lande) kommer
fra [handverksgruppen.com](https://www.handverksgruppen.com/da/) og er det
eneste på siden, der ikke er kundens egen formulering.

## Ingen kontaktformular

Formularen er fjernet på kundens ønske. I stedet står der et
"Ring eller skriv til os"-kort med hovednummer og mail — og hver medarbejder
har sit eget direkte nummer på sit kort.

## Rediger teamet

Medarbejderne står på flere sider og skal være ens. Ret dem ét sted:

```
1. Ret listen TEAM i _gen/partials.py
2. python _gen/build.py                  (og --prod / --wp-plugin ved næste deploy)
```

Se [readme.txt](readme.txt) for detaljer, herunder hvad der skal gøres,
når de nye fotos er taget.

## Bemærk

`.nojekyll`, stub-filerne `om-os.html` m.fl. og denne README hører kun til
GitHub-preview'et. Produktionsbygget i `dist/` og plugin-zip'en indeholder
dem ikke.
