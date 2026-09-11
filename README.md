# Malerfirmaet Hans Larsen — redesign

Preview: **https://abdelkhassouk.github.io/hanslarsen-redesign/**

Statisk site — tre sider, ingen build, ingen afhængigheder. Filerne kan
uploades direkte til webserveren, som de ligger.

| Side | Fil |
|---|---|
| Forside | [index.html](index.html) |
| Om os | [om-os.html](om-os.html) |
| Grøn omstilling | [groen-omstilling.html](groen-omstilling.html) |
| Kontakt | [kontakt.html](kontakt.html) |

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

Firmaet er en del af **Håndverksgruppen**. Det står tre steder: en stribe på
forsiden, en fuld sektion på "Om os", og et logo i footeren på alle sider.
Brødteksten er kundens egen, ordret.

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

Medarbejderne står på alle tre sider og skal være ens. Ret dem ét sted:

```
1. Ret listen TEAM i _gen/partials.py
2. python _gen/build.py
```

Se [readme.txt](readme.txt) for detaljer, herunder hvad der skal gøres,
når de nye fotos er taget.

## Bemærk

`.nojekyll` og denne README er kun til GitHub Pages-previewet og kan
slettes, når siden lægges op på hanslarsen.dk.
