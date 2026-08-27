# RSLR — PPF Landingpage

Statische landingpage voor `ppf.rslr.be`. Geen framework, geen npm, geen build-tooling
behalve één Python-scriptje voor de copy.

---

## 1 · Copy aanpassen

1. Open **`copy.md`** en pas de tekst aan achter de `:`.
2. Run `python3 build.py`
3. `index.html` is opnieuw gegenereerd. Committen en pushen.

Het script waarschuwt bij typfouten in sleutels, dubbele sleutels en lege waarden.

**Bewerk `index.html` niet met de hand** — die wordt overschreven.
Structuur of CSS wijzigen doe je in `template.html`.

HTML in copy mag: `<br>`, `<b>`, `<em>`, `<span class="serif">…</span>`.

| Bestand | Wat |
|---|---|
| `copy.md` | Alle tekst. Dit bewerk je. |
| `template.html` | Structuur, CSS, JS met `{{sleutels}}`. |
| `build.py` | `copy.md` + `template.html` -> `index.html` |
| `index.html` | Wat live gaat. Gegenereerd. |
| `CNAME` | `ppf.rslr.be` |
| `.nojekyll` | Nodig voor GitHub Pages. |

---

## 2 · Formulier laten werken

GitHub Pages is puur statisch: geen server, geen PHP, geen mail. Het formulier
moet dus naar een externe dienst posten. Twee opties, ingebouwd in
`template.html` bovenaan het script.

### A · Web3Forms — de makkelijkste (aanbevolen)

Geen account, geen scenario, geen onderhoud. Leads komen als mail binnen.

1. Ga naar **web3forms.com**, vul het e-mailadres in waar de leads naartoe moeten
   (`info@r-carstyling.be`) en klik **Create Access Key**.
2. Je krijgt direct een key per mail. Zet die in `template.html`:

   ```js
   var WEB3FORMS_KEY = 'abcd1234-....';
   ```

3. `python3 build.py`, committen, pushen.

Gratis tot 250 aanvragen per maand. De key staat publiek in de HTML — dat hoort
zo, spam wordt afgevangen door de honeypot in de pagina plus hun eigen filter.

> Wil je later toch alles in je eigen flow: Web3Forms kan naast de mail ook naar
> een webhook posten. Je hoeft de pagina dan niet aan te raken.

### B · Eigen webhook — Make, Zapier, n8n

Laat `WEB3FORMS_KEY` leeg en zet je webhook-URL in `FORM_ENDPOINT`.

Make-specifiek: **Webhooks -> Custom webhook**, daarachter **JSON -> Parse JSON**.
Als sample voor de data structure:

```json
{"wagen":"Porsche 992.2 GT3 RS","pakket":"Full (€ 5.500)","naam":"Jan Peeters","email":"jan@voorbeeld.be","telefoon":"+32 470 00 00 00","pagina":"https://ppf.rslr.be/","tijdstip":"2026-08-26T09:00:00.000Z"}
```

De pagina post met `Content-Type: text/plain`. Dat is bewust: met
`application/json` stuurt de browser eerst een CORS-preflight (`OPTIONS`), en die
handelen Make- en Zapier-webhooks niet af. De submit faalt dan stil.

### Beide leeg?

Dan valt het formulier terug op een `mailto:`-link. Die opent de mailclient van
de bezoeker en werkt slecht op mobiel. **Niet gebruiken voor advertentieverkeer.**

---

## 3 · Live zetten

### Repo pushen

```bash
cd rslr-ppf
git init
git add .
git commit -m "PPF landingpage"
git branch -M main
git remote add origin git@github.com:<gebruiker>/rslr-ppf.git
git push -u origin main
```

Op een gratis GitHub-plan moet de repo publiek staan voor Pages.

### Pages aanzetten

**Settings -> Pages** -> Source: *Deploy from a branch* -> branch `main`,
folder `/ (root)` -> **Save**.

### Subdomein koppelen

`CNAME` staat al in de repo. Bij de DNS-provider van rslr.be:

| Type | Naam | Waarde |
|---|---|---|
| CNAME | `ppf` | `<gebruiker>.github.io` |

Veel providers willen een trailing dot: `<gebruiker>.github.io.`

Daarna in **Settings -> Pages** het custom domain invullen als het er niet staat,
en **Enforce HTTPS** aanvinken zodra dat aanklikbaar wordt. Dat kan tot een uur
duren omdat GitHub eerst een Let's Encrypt-certificaat uitgeeft.

---

## 4 · Testen voor de advertenties aangaan

- [ ] `https://ppf.rslr.be` opent met slotje
- [ ] Formulier ingevuld op **mobiel** -> mail komt binnen
- [ ] Formulier ingevuld op desktop -> mail komt binnen
- [ ] Verstuur binnen 3 seconden na laden -> mag **niet** aankomen (spamfilter)
- [ ] Vul het verborgen veld `website` via devtools -> mag **niet** aankomen
- [ ] Klik op een pakket-CTA -> dat pakket staat voorgeselecteerd in het formulier
- [ ] Telefoonlink werkt op mobiel
- [ ] GTM preview: `generate_lead`, `phone_click`, `cta_click` vuren

---

## 5 · Nog niet in orde

- **GTM-container** ontbreekt. De `dataLayer`-pushes staan er wel
  (`cta_click`, `phone_click`, `select_package`, `form_start`, `generate_lead`),
  maar zonder container meet je niets en kan je geen conversies terugkoppelen
  naar Google Ads.
- **Cookiebanner** ontbreekt. Nodig zodra GTM met advertentietags erin zit.
  Als rslr.be al een CMP heeft, hoort die hier ook.
- **Afbeeldingen** komen van `rslr.be/wp-content/...`. Werkt, maar zet ze
  self-hosted in de repo voor je hier betaald verkeer op stuurt.

## 6 · Nog te bevestigen door RSLR

- [ ] € 2.200 / € 5.500 — inclusief of exclusief btw?
- [ ] Zones front-pakket (koplampen? dorpels?)
- [ ] Garantietermijn folie
- [ ] Ophaalservice: gratis, forfait, of per kilometer?
- [ ] Voorschot bij boeking, ja of nee, hoeveel?
- [ ] Twee extra PPF-testimonials
- [ ] Middentier tussen € 2.200 en € 5.500 — reële prijs?
