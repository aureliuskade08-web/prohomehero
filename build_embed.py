"""Builds embed/kitchen-designer.html: the finishes designer on its own, one file, for an iframe on another site."""
import base64, re, json, pathlib
r = pathlib.Path(__file__).parent
def font(n): return "data:font/woff2;base64," + base64.b64encode((r/f"fonts/{n}.woff2").read_bytes()).decode()
tokens = (r/"css/tokens.css").read_text()
for n in ("caslon-400", "hanken-400", "hanken-500"): tokens = tokens.replace(f"../fonts/{n}.woff2", font(n))
base = (r/"css/base.css").read_text()
styles = re.sub(r'@import url\("\./[^"]+"\);\n?', "", (r/"css/styles.css").read_text())
extra = """
body.embed { background: var(--color-blush); min-height: 0; }
.embed__wrap { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--space-lg); padding: var(--space-md); max-width: 1200px; margin: 0 auto; }
@media (min-width: 60rem) { .embed__wrap { grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: var(--gap-columns); padding: var(--space-lg); } }
.embed__panel .finishes { margin-top: 0; }
"""
assets = {}
for v in "AB":
    assets[f"mask_{v}.png"] = "data:image/png;base64," + base64.b64encode((r/f"images/designer/mask_{v}.png").read_bytes()).decode()
    for c in ("quartz", "granite", "slate"):
        assets[f"{v}_{c}.jpg"] = "data:image/jpeg;base64," + base64.b64encode((r/f"images/designer/{v}_{c}.jpg").read_bytes()).decode()
js = (r/"js/designer.js").read_text().replace("export const", "const").replace("export function", "function")
js += "\n" + (r/"embed/embed.js").read_text().replace('import { mountDesigner } from "./designer.js";', "")
js = "window.__HH_ASSETS = " + json.dumps(assets) + ";\n" + js
html = (r/"embed/designer.src.html").read_text()
html = html.replace("<!--STYLE-->", f"<style>{tokens}\n{base}\n{styles}\n{extra}</style>").replace("/*EMBED_JS*/", js)
out = r/"embed/kitchen-designer.html"; out.write_text(html)
print(out, round(out.stat().st_size/1e6, 2), "MB")
