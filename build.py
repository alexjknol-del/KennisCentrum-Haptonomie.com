#!/usr/bin/env python3
"""Static site generator for KennisCentrum Haptonomie.
Renders HTML fragments in src/pages/ into base.html and writes clean-URL
output to public/. No client-side framework, no build step needed on the
host — public/ is served as-is.
"""
import shutil
from pathlib import Path
from jinja2 import Template

ROOT = Path(__file__).parent
SRC = ROOT / "src"
PUBLIC = ROOT / "public"
YEAR = 2026
AUTHOR = "Marit Veenhuizen"

base_template = Template((SRC / "templates" / "base.html").read_text(encoding="utf-8"))

# path -> (fragment file, title, description, nav, canonical)
PAGES = [
    ("index.html", "home.html",
     "Informatieplatform over haptonomie en haptotherapie",
     "KennisCentrum Haptonomie brengt uitleg, achtergrond en actuele artikelen samen over haptonomie en haptotherapie.",
     "home", "/"),
    ("over/index.html", "over.html",
     "Over dit platform",
     "Wat KennisCentrum Haptonomie wel en niet is, wie erachter zit en hoe de artikelen tot stand komen.",
     "over", "/over/"),
    ("wat-is-haptonomie/index.html", "wat-is-haptonomie.html",
     "Wat is haptonomie",
     "Herkomst, uitgangspunten en het verschil tussen haptonomie en haptotherapie, uitgelegd in gewone taal.",
     "watis", "/wat-is-haptonomie/"),
    ("een-haptotherapeut-vinden/index.html", "een-haptotherapeut-vinden.html",
     "Een haptotherapeut vinden",
     "Waar op te letten bij het kiezen van een haptotherapeut, met een praktijkvoorbeeld uit Amsterdam en Muiden.",
     "vinden", "/een-haptotherapeut-vinden/"),
    ("veelgestelde-vragen/index.html", "veelgestelde-vragen.html",
     "Veelgestelde vragen",
     "Antwoord op de vragen die het vaakst opkomen over haptonomie en haptotherapie.",
     "faq", "/veelgestelde-vragen/"),
    ("contact/index.html", "contact.html",
     "Contact",
     "Vragen, aanvullingen of een correctie doorgeven kan per e-mail naar info@kenniscentrum-haptonomie.com.",
     "contact", "/contact/"),
    ("privacybeleid/index.html", "privacybeleid.html",
     "Privacybeleid",
     "Privacybeleid van KennisCentrum Haptonomie.",
     "", "/privacybeleid/"),
    ("cookiebeleid/index.html", "cookiebeleid.html",
     "Cookiebeleid",
     "Cookiebeleid van KennisCentrum Haptonomie.",
     "", "/cookiebeleid/"),
    ("nieuws/index.html", "nieuws-index.html",
     "Nieuws",
     "Actuele artikelen over haptonomie en haptotherapie: toepassingen, vergoeding en verwante vormen van lichaamsgerichte begeleiding.",
     "nieuws", "/nieuws/"),
]

ARTICLES = [
    ("nieuws/verschil-haptonomie-haptotherapie/index.html",
     "nieuws/verschil-haptonomie-haptotherapie.html",
     "Haptonomie en haptotherapie: het verschil in de praktijk",
     "Twee begrippen die vaak door elkaar worden gebruikt, maar niet hetzelfde betekenen. Een uitleg met voorbeelden.",
     "/nieuws/verschil-haptonomie-haptotherapie/"),
    ("nieuws/haptotherapie-stress-burnout/index.html",
     "nieuws/haptotherapie-stress-burnout.html",
     "Haptotherapie bij stress en burn-outklachten: wat gebeurt er in een sessie",
     "Hoe haptotherapeuten werken aan herstel van contact met het eigen lichaam bij overspanning en burn-out.",
     "/nieuws/haptotherapie-stress-burnout/"),
    ("nieuws/haptonomische-zwangerschapsbegeleiding/index.html",
     "nieuws/haptonomische-zwangerschapsbegeleiding.html",
     "Haptonomische zwangerschapsbegeleiding: contact maken met een ongeboren kind",
     "Wat deze specifieke vorm van begeleiding inhoudt en wat er in de praktijk tijdens sessies gebeurt.",
     "/nieuws/haptonomische-zwangerschapsbegeleiding/"),
    ("nieuws/vergoeding-haptotherapie-2026/index.html",
     "nieuws/vergoeding-haptotherapie-2026.html",
     "Wordt haptotherapie vergoed? Overzicht voor 2026",
     "Wat aanvullende verzekeringen doorgaans dekken, waar dat per verzekeraar verschilt en welke vragen te stellen zijn.",
     "/nieuws/vergoeding-haptotherapie-2026/"),
    ("nieuws/lichaamsgerichte-therapie-vergelijking/index.html",
     "nieuws/lichaamsgerichte-therapie-vergelijking.html",
     "Lichaamsgerichte therapie: waar haptonomie wel en niet bij aansluit",
     "Een overzicht van hoe haptotherapie zich verhoudt tot fysiotherapie, Mensendieck-oefentherapie en psychosomatische fysiotherapie.",
     "/nieuws/lichaamsgerichte-therapie-vergelijking/"),
    ("nieuws/leven-met-chronische-klachten/index.html",
     "nieuws/leven-met-chronische-klachten.html",
     "Leven met chronische klachten: de rol van voelen en bewustwording",
     "Hoe lichaamsgerichte aandacht kan helpen bij het omgaan met langdurige pijn- of spanningsklachten.",
     "/nieuws/leven-met-chronische-klachten/"),
    ("nieuws/structureel-schoonmaakonderhoud-zorg-onderwijs/index.html",
     "nieuws/structureel-schoonmaakonderhoud-zorg-onderwijs.html",
     "Waarom structureel schoonmaakonderhoud onmisbaar is in zorg en onderwijs",
     "Waarom schoonmaak in zorg en onderwijs geen incidentele activiteit is, maar een structureel proces dat samenhangt met gezondheid en veiligheid.",
     "/nieuws/structureel-schoonmaakonderhoud-zorg-onderwijs/"),
]


def render_page(out_rel, fragment_rel, title, description, nav, canonical, og_type="website"):
    fragment_path = SRC / "pages" / fragment_rel
    content = fragment_path.read_text(encoding="utf-8")
    html = base_template.render(
        title=title,
        description=description,
        nav=nav,
        canonical=canonical,
        content=content,
        year=YEAR,
        author_name=AUTHOR,
        og_type=og_type,
        schema=None,
    )
    out_path = PUBLIC / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  wrote {out_rel}")


def main():
    # Clean previously generated HTML (keep assets/)
    for item in PUBLIC.iterdir():
        if item.name == "assets":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    print("Rendering pages...")
    for out_rel, fragment_rel, title, description, nav, canonical in PAGES:
        render_page(out_rel, fragment_rel, title, description, nav, canonical)

    print("Rendering articles...")
    for out_rel, fragment_rel, title, description, canonical in ARTICLES:
        render_page(out_rel, fragment_rel, title, description, "nieuws", canonical, og_type="article")

    # 404 page
    not_found_content = """
<div class="page-header">
  <div class="wrap">
    <span class="eyebrow">Pagina niet gevonden</span>
    <h1>Deze pagina bestaat niet (meer)</h1>
    <p class="page-lede">De opgevraagde pagina is niet gevonden. Mogelijk is de link verouderd of onjuist getypt.</p>
  </div>
</div>
<div class="content-wrap"><div class="wrap no-aside">
  <p><a href="/">Terug naar de homepage</a> of bekijk het <a href="/nieuws/">nieuwsoverzicht</a>.</p>
</div></div>
"""
    html = base_template.render(
        title="Pagina niet gevonden",
        description="Deze pagina bestaat niet (meer).",
        nav="", canonical="/404/", content=not_found_content,
        year=YEAR, author_name=AUTHOR, og_type="website", schema=None,
    )
    (PUBLIC / "404.html").write_text(html, encoding="utf-8")
    print("  wrote 404.html")

    # robots.txt
    (PUBLIC / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://kenniscentrum-haptonomie.com/sitemap.xml\n",
        encoding="utf-8",
    )
    print("  wrote robots.txt")

    # sitemap.xml
    all_paths = ["/"] + [c for *_, c in PAGES if c != "/"] + [c for *_, c in ARTICLES]
    urls = "\n".join(
        f"  <url><loc>https://kenniscentrum-haptonomie.com{p}</loc></url>" for p in all_paths
    )
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    (PUBLIC / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("  wrote sitemap.xml")

    # Cloudflare Pages headers (basic hardening)
    headers = """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), camera=(), microphone=()
"""
    (PUBLIC / "_headers").write_text(headers, encoding="utf-8")
    print("  wrote _headers")

    print("Done.")


if __name__ == "__main__":
    main()
