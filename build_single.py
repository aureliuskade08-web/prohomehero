"""Builds one self-contained prohomehero.html (CSS, JS, three.js and all photos inlined)."""
import base64, re, pathlib
r = pathlib.Path(__file__).parent
html = (r/"index.html").read_text()

# photos: embed each once, point <img>/buttons at them by id
imgs = {f"{n:02d}": "data:image/jpeg;base64," + base64.b64encode((r/f"images/kitchen-{n:02d}.jpg").read_bytes()).decode() for n in range(1,18)}
html = re.sub(r'<meta property="og:image"[^>]*>\n?', '', html)
html = re.sub(r'<link rel="preload"[^>]*>\n?', '', html)
html = re.sub(r'(?<![-\w])src="images/kitchen-(\d+)\.jpg"', r'data-img="\1"', html)
html = re.sub(r'\bdata-src="images/kitchen-(\d+)\.jpg"', r'data-img="\1"', html)

import re as _re
def inline_css(path):
    c = (r/path).read_text()
    c = _re.sub(r'@import url\("\./[^"]+"\);\n?', '', c)
    return c
def font(n): return "data:font/woff2;base64," + base64.b64encode((r/f"fonts/{n}.woff2").read_bytes()).decode()
tokens = (r/"css/tokens.css").read_text()
for n in ("caslon-400","hanken-400","hanken-500"): tokens = tokens.replace(f"../fonts/{n}.woff2", font(n))
hero = "data:image/jpeg;base64," + base64.b64encode((r/"images/hero-island.jpg").read_bytes()).decode()
styles = (r/"css/styles.css").read_text()
stamp = "\n".join(l for l in styles.splitlines() if l.startswith("/*") or l.startswith(" *"))
css = stamp + "\n" + tokens + "\n" + (r/"css/base.css").read_text() + "\n" + inline_css("css/styles.css") + "\n" + (r/"css/tailwind.css").read_text()
html = html.replace('src="images/hero-island.jpg"', f'src="{hero}"')
html = html.replace('<link rel="stylesheet" href="css/styles.css" />', f"<style>{css}</style>").replace('<link rel="stylesheet" href="css/tailwind.css" />', "")

kit = (r/"js/kitchen3d.js").read_text()
kit = kit.replace('import * as THREE from "../vendor/three.module.min.js";', '')
kit = kit.replace('export function mountKitchen(canvasHost, onChange)', 'function mountKitchen(THREE, canvasHost, onChange)')
main = (r/"js/main.js").read_text()
main = main.replace('const { mountKitchen } = await import("./kitchen3d.js");\n    const k = mountKitchen(host,',
  'const THREE = await import(URL.createObjectURL(new Blob([atob(document.getElementById("three-src").textContent.trim())], { type: "text/javascript" })));\n    const k = mountKitchen(THREE, host,')
assert 'mountKitchen(THREE' in main
# resolve data-img attributes before anything reads them
prelude = '''const IMG = %s;
document.querySelectorAll("[data-img]").forEach((el) => {
  const u = IMG[el.dataset.img];
  if (el.tagName === "IMG") el.src = u; else el.dataset.src = u;
});
''' % __import__("json").dumps(imgs)

three = base64.b64encode((r/"vendor/three.module.min.js").read_bytes()).decode()
script = f'<script type="text/plain" id="three-src">{three}</script>\n<script type="module">\n{prelude}\n{kit}\n{main}\n</script>'
html = html.replace('<script type="module" src="js/main.js"></script>', "")
html = html.replace('</body>', script + '\n</body>')
out = pathlib.Path("/mnt/user-data/outputs/prohomehero.html"); out.write_text(html)
print(out, round(out.stat().st_size/1e6,2), "MB")
