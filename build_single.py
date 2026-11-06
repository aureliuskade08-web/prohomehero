"""Builds one self-contained prohomehero.html (CSS, JS, rendered kitchen and all photos inlined)."""
import base64, re, pathlib
r = pathlib.Path(__file__).parent
html = (r/"index.html").read_text()

# photos: embed each once, point <img>/buttons at them by id
imgs = {f"{n:02d}": "data:image/jpeg;base64," + base64.b64encode((r/f"images/kitchen-{n:02d}.jpg").read_bytes()).decode() for n in range(1,27)}
html = re.sub(r'<meta property="og:image"[^>]*>\n?', '', html)
html = re.sub(r'<link rel="preload"[^>]*>\n?', '', html)
html = re.sub(r'(?<![-\w])src="images/kitchen-(\d+)\.jpg"', r'data-img="\1"', html)
html = re.sub(r'\bdata-src="images/kitchen-(\d+)\.jpg"', r'data-img="\1"', html)

_chk = "document.querySelectorAll('[data-slot] img').forEach((i) => { if (i.complete && !i.naturalWidth) i.remove(); else i.addEventListener('error', () => i.remove(), { once: true }); });"
assert _chk in html
html = html.replace(_chk, "")  # photos get their data URI from the script below; this empty-slot check would remove them first
html = re.sub(r'<li><a href="services/[^"]+/">', '<li><a href="#estimate">', html)  # the review copy is one file; service pages exist only in the folder build
import re as _re
def inline_css(path):
    c = (r/path).read_text()
    c = _re.sub(r'@import url\("\./[^"]+"\);\n?', '', c)
    return c
def font(n): return "data:font/woff2;base64," + base64.b64encode((r/f"fonts/{n}.woff2").read_bytes()).decode()
tokens = (r/"css/tokens.css").read_text()
for n in ("caslon-400","hanken-400","hanken-500"): tokens = tokens.replace(f"../fonts/{n}.woff2", font(n))
for _n in ('mark','logo'):
    html = html.replace(f'src="images/{_n}.png"', 'src="data:image/png;base64,' + base64.b64encode((r/f'images/{_n}.png').read_bytes()).decode() + '"')
hero = "data:image/jpeg;base64," + base64.b64encode((r/"images/hero-kitchen.jpg").read_bytes()).decode()
styles = (r/"css/styles.css").read_text()
stamp = "\n".join(l for l in styles.splitlines() if l.startswith("/*") or l.startswith(" *"))
css = stamp + "\n" + tokens + "\n" + (r/"css/base.css").read_text() + "\n" + inline_css("css/styles.css") + "\n" + (r/"css/tailwind.css").read_text()
html = html.replace('src="images/hero-kitchen.jpg"', f'src="{hero}"')
html = html.replace('<link rel="stylesheet" href="css/styles.css" />', f"<style>{css}</style>").replace('<link rel="stylesheet" href="css/tailwind.css" />', "")

des = (r/"js/designer.js").read_text().replace("export const", "const").replace("export function", "function")
main = (r/"js/main.js").read_text()
main = main.replace('const { mountDesigner } = await import("./designer.js");', '')
assert 'await import("./designer.js")' not in main
assets = {}
for v in "AB":
    assets[f"mask_{v}.png"] = "data:image/png;base64," + base64.b64encode((r/f"images/designer/mask_{v}.png").read_bytes()).decode()
    for c in ("quartz", "granite", "slate"):
        assets[f"{v}_{c}.jpg"] = "data:image/jpeg;base64," + base64.b64encode((r/f"images/designer/{v}_{c}.jpg").read_bytes()).decode()
# resolve data-img attributes before anything reads them
prelude = '''const IMG = %s;
document.querySelectorAll("[data-img]").forEach((el) => {
  const u = IMG[el.dataset.img];
  if (el.tagName === "IMG") el.src = u; else el.dataset.src = u;
});
''' % __import__("json").dumps(imgs)

script = f'<script type="module">\nwindow.__HH_ASSETS = {__import__("json").dumps(assets)};\n{prelude}\n{des}\n{main}\n</script>'
html = html.replace('<script type="module" src="js/main.js"></script>', "")
html = html.replace('</body>', script + '\n</body>')
out = pathlib.Path("/mnt/user-data/outputs/prohomehero.html"); out.write_text(html)
print(out, round(out.stat().st_size/1e6,2), "MB")
