# Skift www.hanslarsen.dk til den nye side

Der er to veje. **Vej A kræver kun WordPress-login** og er den anbefalede.

Uanset vej bliver disse ting **ikke rørt**:

| | |
|---|---|
| E-mail | Kører på Microsoft 365 (MX → `outlook.com`). Ingen DNS ændres. |
| DNS | Ligger hos Curanet. Intet ændres. |
| SSL / HTTPS | Webhotellets certifikat bruges som hidtil. |
| Google Search Console | TXT-verificeringen i DNS er urørt. |
| WordPress | Indhold, database, tema og brugere bliver liggende. Intet slettes. |

De adresser Google kender — `/`, `/om-os/`, `/kontakt/` — virker uændret.
Gamle WordPress-adresser (`/hello-world/`, `/author/admin/`, `/feed/`,
`/wp-sitemap.xml` …) sendes videre med 301, så ingen links ender i en fejl.

---

## Vej A — via WordPress (anbefalet)

Den nye side lægges ind som et plugin. Når det er slået til, viser WordPress
den nye side i stedet for det gamle tema. **Fortryd = "Deaktivér".**

Testet på WordPress 6.3.10 (samme version som hanslarsen.dk) med de samme
fire plugins som produktionen, på PHP 7.4 og 8.2: 116 tjek, alle grønne, inkl.
at alt er identisk med før efter deaktivering.

Før go-live blev de fire produktions-plugins gennemgået kode for kode. Det fandt
én blokerende fejl i version 1.0.0: WordPress selv sender `hanslarsen.dk` videre
til `www`, og pluginet sprang det over. Rettet i **1.0.1**. `wp.py` nægter at
aktivere en ældre version.

### 0. Tag en backup
Selvom intet slettes: tag en backup i Curanet-panelet eller med et
backup-plugin, før du starter.

### 1. Upload pluginet — men aktivér det ikke
wp-admin → **Plugins → Tilføj nyt → Upload plugin** → vælg

    dist-wp/hanslarsen-site.zip

→ **Installer nu**. Stop der. Klik *ikke* "Aktivér plugin".

Ligger der allerede en ældre version, siger WordPress at pluginet er
installeret — klik **Erstat den nuværende med den uploadede** (*Replace current
with uploaded*).

(Zip'en bygges med `python _gen/build.py --wp-plugin`.)

### 2. Lav en applikationsadgangskode
wp-admin → **Brugere → Profil** → rul ned til **Adgangskoder til
applikationer** → navn: `deploy` → **Tilføj**. Kopiér koden.

Det er *ikke* din login-adgangskode. Den kan kun bruges til API'et og kan
tilbagekaldes med ét klik.

### 3. Læg den i `deploy/.deploy-env`
Filen er git-ignoreret og kommer aldrig på GitHub.

    HL_WP_USER=admin
    HL_WP_APP_PASSWORD=abcd efgh ijkl mnop qrst uvwx

### 4. Skift
**Hav en fane åben, hvor du er logget ind i wp-admin**, mens der skiftes.
Limit Login Attempts låser login efter fire forkerte forsøg, men en session der
allerede er logget ind, bliver ikke ramt — så kan du altid nå "Deaktivér".

    python deploy/wp.py status             # tjekker login og at pluginet ligger der
    python deploy/wp.py activate           # tørkørsel
    python deploy/wp.py activate --yes     # skifter

`activate --yes` slår pluginet til og tjekker straks live-siden: alle seks
sider, hvert billede, stylesheet og link, redirect-kæden fra
`http://hanslarsen.dk/`, at `/wp-login.php` stadig virker, HSTS og 404-siden.
**Fejler noget kritisk, slår den selv pluginet fra igen.**

### Fortryd
    python deploy/wp.py deactivate --yes

— eller gå direkte til **https://www.hanslarsen.dk/wp-admin/** → Plugins →
**Deaktivér** ved "Hans Larsen — ny hjemmeside". Pluginet tømmer
LiteSpeed-/sidecache ved både til og fra, så skiftet ses med det samme.

Log ind med den *normale* adgangskode. Applikationsadgangskoden virker ikke på
login-siden, og hvert forsøg med den tæller som et forkert login.

### Se den gamle side, mens den nye er aktiv
Logget ind som administrator: tilføj `?hls-gammel` til en adresse, fx
`https://www.hanslarsen.dk/?hls-gammel`. Besøgende ser altid den nye side.

### Bagefter
- Tag en ny backup i **All-in-One WP Migration** og kald den "ny hjemmeside".
  En gendannelse af en ældre backup slår den nye side fra igen.
- Tilbagekald applikationsadgangskoden (samme sted som den blev oprettet).
- Google Search Console → Sitemaps → indsend `https://www.hanslarsen.dk/sitemap.xml`.

### Godt at vide, mens den nye side er aktiv
- **Under Construction kan ikke skjule den nye side.** Skal der vises en
  vedligeholdelses-side, så deaktivér "Hans Larsen — ny hjemmeside" først.
- **Rør ikke Indstillinger → HTTPS Redirection.** Gemmer man der, skriver
  pluginet hele `.htaccess` om — og det er den, der sender http til https.

---

## Vej B — via FTP (hvis WordPress senere skal helt væk)

Kræver FTP-login fra Curanet-panelet ("Tekniske oplysninger" / "Brugere").
Siden lægges op som rene filer; WordPress bliver liggende på serveren som
nødplan, men lukkes ned udadtil.

    python _gen/build.py --prod            # bygger dist/

    # deploy/.deploy-env
    HL_FTP_HOST=...
    HL_FTP_USER=...
    HL_FTP_PASS=...

    python deploy/deploy.py inspect        # kigger, ændrer intet
    python deploy/deploy.py deploy         # tørkørsel
    python deploy/deploy.py deploy --yes

Sådan passer den på:
1. Downloader hver fil, der bliver overskrevet (`.htaccess`, `robots.txt`) til `_backup/`.
2. Tester den nye `.htaccess` i en midlertidig mappe først. Afviser serveren
   den, afbrydes alt, før live-siden røres.
3. Uploader billeder og CSS før siderne, forsiden næstsidst, `.htaccess` sidst.
4. Tjekker live-siden. Ved kritisk fejl lægges alt automatisk tilbage.

Fortryd når som helst:

    python deploy/deploy.py rollback _backup/<tidspunkt>/manifest.json --yes

Testet mod en FTPS-server med en kopi af en WordPress-installation: 47 tjek,
alle grønne, inkl. at serveren er byte-for-byte identisk efter tilbagerulning.

---

## Upload ALDRIG filerne fra repo-roden

`index.html`, `om-os/` osv. i roden af repoet er **GitHub-preview'et**. De har
`<meta name="robots" content="noindex">`, så kopien på GitHub ikke konkurrerer
med hanslarsen.dk i Google. Lagt på hanslarsen.dk ville de fjerne firmaet fra
Google.

Til produktion: `dist/` (vej B) eller `dist-wp/hanslarsen-site.zip` (vej A).

---

## Fundet undervejs

Ikke en del af skiftet, men værd at vide:

- **WordPress 6.3.10 er gammel.** Den nye side skjuler temaet, men WordPress
  kører stadig bag vej A. Opdatér WordPress og plugins, eller gå til vej B.
- **Brugernavnet `admin` er offentligt** — både via `/author/admin/` (lukket af
  den nye side) og `https://www.hanslarsen.dk/wp-json/wp/v2/users` (ikke lukket).
  Sørg for en stærk adgangskode og gerne to-faktor-login.
- **Standard-indlægget "Hello world!"** lå i Googles sitemap. Adressen sendes nu
  videre til forsiden.
