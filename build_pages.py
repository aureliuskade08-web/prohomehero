"""Builds the service pages (services/<slug>/index.html) and sitemap.xml from pages.py, reusing the header, menu,
estimate form, footer and mobile bar from src/index.src.html so a change there carries to every page.
Run after build.py:  python3 build_pages.py
"""
import html, json, pathlib, re, datetime
from pages import PAGES, ORDER

root = pathlib.Path(__file__).parent
src = (root / "src/index.src.html").read_text()
SITE = "https://www.prohomehero.com"
e = html.escape

def between(start, end, text=src):
    a = text.index(start); b = text.index(end, a) + len(end)
    return text[a:b]

header = between('<header id="nav"', "</header>")
menu = src[src.index('<div id="mobileMenu"'): src.index("<main")].rstrip()
estimate = between('<section id="estimate"', "</section>")
footer = between('<footer class="footer">', "</footer>")
sticky = between('<div class="sticky-cta md:hidden"', "</div>")

ICON = re.search(r'<link rel="icon"[^>]*/>', src).group(0)

def fix(block, root_rel):
    """Point home-page anchors at the home page and asset paths at the site root, from a page two folders deep."""
    block = re.sub(r'href="#(portfolio|services|design|financing|process|about)"', lambda m: f'href="{root_rel}#{m.group(1)}"', block)
    block = block.replace('href="#top"', f'href="{root_rel}"')
    block = block.replace('src="images/', f'src="{root_rel}images/')
    return block

def service_links(root_rel):
    return "".join(f'<a href="{root_rel}services/{s}/">{e(PAGES[s]["name"])}</a>' for s in ORDER)

def build(slug):
    d = PAGES[slug]; rr = "../../"
    url = f"{SITE}/services/{slug}/"
    rows = lambda items: "\n".join(f'<li><div><h3>{e(t)}</h3><p>{e(b)}</p></div></li>' for t, b in items)
    faq = "\n".join(f'<li><div><h3>{e(q)}</h3><p>{e(a)}</p></div></li>' for q, a in d["faq"])
    related = "".join(f'<li><a href="{rr}services/{r}/"><h3>{e(PAGES[r]["name"])}</h3></a></li>' for r in d["related"])
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "@id": url + "#service", "name": d["name"], "serviceType": d["name"], "description": d["description"],
         "url": url, "provider": {"@id": SITE + "/#business"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home Hero", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": d["name"], "item": url}]},
    ]}
    f = fix(footer, rr)
    f = f.replace('<div class="col-span-12 lg:col-span-6">\n        <p class="footer__sign">', '<div class="col-span-12 lg:col-span-4">\n        <p class="footer__sign">', 1)
    f = f.replace('footer__links col-span-12 lg:col-span-3 lg:col-start-7" aria-label="Footer"', 'footer__links col-span-12 lg:col-span-2 lg:col-start-5" aria-label="Footer"', 1)
    f = f.replace('<div class="footer__links col-span-12 lg:col-span-3 lg:col-start-10">', f'<nav class="footer__links col-span-12 lg:col-span-3 lg:col-start-7" aria-label="Services">{service_links(rr)}</nav>\n      <div class="footer__links col-span-12 lg:col-span-3 lg:col-start-10 footer__contact">', 1)
    est = fix(estimate, rr)
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{e(d["title"])}</title>
  <meta name="description" content="{e(d["description"])}" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#F7F3EB" />
  <meta property="og:title" content="{e(d["title"])}" />
  <meta property="og:description" content="{e(d["description"])}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="Home Hero" />
  <meta property="og:image" content="{SITE}/images/kitchen-{d["photo"]:02d}.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preload" href="{rr}fonts/caslon-400.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="{rr}css/styles.css" />
  <link rel="stylesheet" href="{rr}css/tailwind.css" />
  {ICON}
  <link rel="apple-touch-icon" href="{rr}images/apple-touch-icon.png" />
  <script type="application/ld+json">
{json.dumps(jsonld, indent=2)}
  </script>
</head>
<body data-phone="+14705735890" data-phone-display="(470) 573-5890" data-email="info@prohomehero.com" data-service="{e(d["service_value"])}">
  <a class="skip" href="#main">Skip to content</a>
  {fix(header, rr)}

  {fix(menu, rr)}

  <main id="main">
    <section class="py-sec-s page-hero" aria-labelledby="pageTitle">
      <div class="container grid grid-cols-12 gap-x-col gap-y-xl">
        <div class="col-span-12 lg:col-span-7">
          <nav class="crumbs" aria-label="Breadcrumb"><a href="{rr}">Home Hero</a><span aria-hidden="true">/</span><span aria-current="page">{e(d["name"])}</span></nav>
          <h1 id="pageTitle" class="page-title">{e(d["h1"])}</h1>
          <p class="lead pt-lg">{e(d["lead"])}</p>
          <div class="actions pt-xl">
            <a href="#estimate" class="btn">Get a free estimate</a>
            <a data-tel href="tel:+14705735890" class="link">Call <span data-phone-text>(470) 573-5890</span></a>
          </div>
        </div>
        <figure class="arch col-span-12 lg:col-span-4 lg:col-start-9">
          <img src="{rr}images/kitchen-{d["photo"]:02d}.jpg" alt="{e(d["photo_alt"])}" width="900" height="1200" />
        </figure>
      </div>
    </section>

    <section class="py-sec-s band-paper2" aria-labelledby="incTitle">
      <div class="container">
        <div class="head grid grid-cols-12 gap-x-col gap-y-lg"><h2 id="incTitle" class="col-span-12 lg:col-span-8">{e(d["included_title"])}</h2></div>
        <ul class="rows">
{rows(d["included"])}
        </ul>
      </div>
    </section>

    <section class="py-sec-s" aria-labelledby="optTitle">
      <div class="container">
        <div class="head grid grid-cols-12 gap-x-col gap-y-lg"><h2 id="optTitle" class="col-span-12 lg:col-span-8">{e(d["options_title"])}</h2></div>
        <ul class="rows">
{rows(d["options"])}
        </ul>
        <div class="actions pt-xl">
          <a href="{rr}#design" class="btn btn--quiet">Try your finishes</a>
          <a href="{rr}#portfolio" class="link">See our kitchens</a>
        </div>
      </div>
    </section>

    <section class="py-sec-s band-blush" aria-labelledby="faqTitle">
      <div class="container">
        <div class="head grid grid-cols-12 gap-x-col gap-y-lg"><h2 id="faqTitle" class="col-span-12 lg:col-span-8">Common questions</h2></div>
        <ul class="rows">
{faq}
        </ul>
        <p class="credit">Financing is subject to approval. Ask about it when we quote your project.</p>
      </div>
    </section>

    <section class="py-sec-s" aria-labelledby="relTitle">
      <div class="container">
        <div class="head grid grid-cols-12 gap-x-col gap-y-lg"><h2 id="relTitle" class="col-span-12 lg:col-span-8">More from Home Hero</h2></div>
        <ul class="rows rows--links">
{related}
        </ul>
      </div>
    </section>

    {est}
  </main>

  {f}

  {fix(sticky, rr).replace('href="#estimate"', 'href="#estimate"')}

  <script type="module" src="{rr}js/main.js"></script>
</body>
</html>
'''
    out = root / "services" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    return out

for s in ORDER: build(s)

today = datetime.date.today().isoformat()
urls = [(f"{SITE}/", "1.0")] + [(f"{SITE}/services/{s}/", "0.8") for s in ORDER]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, pr in urls:
    sm += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{pr}</priority>\n  </url>\n"
sm += "</urlset>\n"
(root / "sitemap.xml").write_text(sm)
print("built", len(ORDER), "service pages and sitemap.xml")
