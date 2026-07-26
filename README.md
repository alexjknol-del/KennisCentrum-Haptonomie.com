# KennisCentrum Haptonomie

Broncode voor kenniscentrum-haptonomie.com, een onafhankelijk informatieplatform over haptonomie en haptotherapie.

## Structuur

- `src/templates/base.html` — basislayout (header, navigatie, footer)
- `src/pages/` — HTML-fragmenten per pagina, incl. `src/pages/nieuws/` voor artikelen
- `public/` — gegenereerde statische site (wordt gedeployed, `assets/` bevat CSS en SVG's)
- `build.py` — rendert de fragmenten in `src/pages/` via `base.html` naar `public/`

## Bouwen

```
python3 build.py
```

Genereert de volledige site in `public/`. Geen verdere buildstap nodig; `public/` kan direct als statische site worden gehost.

## Hosting

De site is gebouwd om als statische site (bijv. via Cloudflare Pages) te worden gehost, met `public/` als outputmap en zonder build command op de hostingpartij.
