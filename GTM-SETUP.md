# GTM — wat je in de container moet aanmaken

Container `GTM-M7W5SPL3` staat in de pagina (head + noscript). De pagina duwt
zelf events in de dataLayer. In GTM moet je die nog oppikken.

## 1 · Variabelen (Variables -> User-Defined -> New -> Data Layer Variable)

| Naam | Data Layer Variable Name |
|---|---|
| `dlv - cta_id` | `cta_id` |
| `dlv - package` | `package` |
| `dlv - step` | `step` |

## 2 · Triggers (Triggers -> New -> Custom Event)

| Naam | Event name |
|---|---|
| `CE - generate_lead` | `generate_lead` |
| `CE - form_start` | `form_start` |
| `CE - phone_click` | `phone_click` |
| `CE - cta_click` | `cta_click` |
| `CE - select_package` | `select_package` |

## 3 · Tags

**GA4 — Lead**
- Type: GA4 Event, Measurement ID: die van rslr.be
- Event Name: `generate_lead`
- Trigger: `CE - generate_lead`

**GA4 — Phone click**
- Event Name: `phone_click`, parameter `cta_id` = `{{dlv - cta_id}}`
- Trigger: `CE - phone_click`

**Google Ads — Conversie**
- Type: Google Ads Conversion Tracking
- Conversion ID + Label uit Google Ads (nieuwe conversieactie "PPF aanvraag")
- Trigger: `CE - generate_lead`

**Google Ads — Remarketing**
- Type: Google Ads Remarketing, trigger: All Pages
- Zodat je bezoekers van deze pagina kan retargeten

## 4 · LET OP — hostname-filters

Deze container draait al op `rslr.be`. Controleer bij elke bestaande trigger of
er een conditie op **Page Hostname** staat die `rslr.be` exact matcht. Zulke
triggers vuren niet op `ppf.rslr.be`.

Zet ze om naar `Page Hostname` **contains** `rslr.be`, of voeg
`ppf.rslr.be` expliciet toe. Dit is de meest voorkomende reden dat een
subdomein "geen data" lijkt te hebben.

Idem voor GA4: als er cross-domain/referral-exclusies staan, voeg
`ppf.rslr.be` toe zodat een bezoeker die van rslr.be komt geen nieuwe sessie start.

## 5 · Cookiebanner / consent

Draait de CMP van rslr.be via deze container (Cookiebot, Complianz, CookieYes)?
Dan verschijnt hij automatisch ook hier — controleren in Preview.
Zo niet, dan moet er een banner bij voor je advertentietags aanzet.

## 6 · Testen

GTM **Preview** -> `https://ppf.rslr.be` -> doorloop:

- [ ] pagina laden -> `gtm.js` + remarketing vuurt
- [ ] klik pakket-CTA -> `select_package` met `package`
- [ ] eerste toetsaanslag in formulier -> `form_start` (één keer)
- [ ] telefoonlink -> `phone_click`
- [ ] formulier verstuurd -> `generate_lead` + Google Ads-conversie
