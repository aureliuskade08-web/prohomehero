"""Injects the portfolio markup into src/index.src.html -> index.html (static HTML for SEO)."""
import html, pathlib
root = pathlib.Path(__file__).parent

CAPTIONS = {
 1: "White shaker kitchen opening to a sunroom, walnut island, slate tile floor",
 2: "Quartz slab backsplash, brass pull-down faucet and navy uppers with under-cabinet light",
 3: "Navy base cabinets with brass pulls and floating wood shelves",
 4: "White shaker cabinets, granite counters, farmhouse sink and gas range",
 5: "Farmhouse sink under the window with black hardware and subway tile",
 6: "Farmhouse workstation sink with a black pull-down faucet and granite",
 7: "Cream cabinets with glass-front uppers, brass pulls and slab backsplash",
 8: "Brass pot filler over a gas cooktop with a quartz slab backsplash",
 9: "Quartz island with brass and leather stools and glass-front cabinets",
 10: "Two-tone kitchen: white uppers, navy base cabinets and brass pulls",
 11: "Workstation sink set into quartz with a black faucet and subway tile",
 12: "Full-height white pantry cabinets beside a black refrigerator",
 13: "Two-tone cabinets with black appliances and plank flooring",
 14: "Quartz island with a pendant light, open to the living area",
 15: "Gray shaker cabinets with stacked glass-front uppers and a gas range",
 16: "Stainless farmhouse sink with a matte black pull-down faucet",
 17: "Quartz island with a pendant light and stainless refrigerator",
}
SHORT = {1:"White shaker, walnut island",2:"Quartz slab, brass faucet",3:"Navy cabinets, floating shelves",4:"Granite, farmhouse sink",5:"Farmhouse sink, black hardware",6:"Workstation sink, granite",7:"Cream cabinets, glass fronts",8:"Brass pot filler, slab backsplash",9:"Quartz island, brass and leather",10:"Two-tone, white and navy",11:"Sink set into quartz",12:"Full-height pantry cabinets",13:"Two-tone, plank flooring",14:"Island with pendant light",15:"Gray shaker, glass uppers",16:"Stainless farmhouse sink",17:"Island, stainless refrigerator"}
# Photos shown before "See more projects" (best 8), rest are revealed on click.
ORDER = [9, 2, 10, 7, 4, 8, 3, 14, 1, 11, 15, 5, 6, 12, 13, 16, 17]
FIRST = 8

items = []
for pos, n in enumerate(ORDER):
    cap = html.escape(CAPTIONS[n], quote=True)
    extra = ' data-extra hidden' if pos >= FIRST else ''
    items.append(
        f'        <li class="g-item"{extra}>\n'
        f'          <button type="button" class="g-btn" data-i="{pos}" data-src="images/kitchen-{n:02d}.jpg" data-cap="{cap}" aria-label="View photo: {cap}">\n'
        f'            <img src="images/kitchen-{n:02d}.jpg" alt="{cap}" loading="lazy" width="900" height="1600" />\n'
        f'          </button>\n'
        f'          <p class="g-cap">{html.escape(SHORT[n])}</p>\n'
        f'        </li>'
    )

src = (root / "src/index.src.html").read_text()
(root / "index.html").write_text(src.replace("<!--GALLERY-->", "\n".join(items)))
print("built", len(items), "gallery items")
