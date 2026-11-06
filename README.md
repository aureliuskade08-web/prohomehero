# Home Hero website

Static site: HTML, CSS, Tailwind (layout only) and vanilla ES modules. Serve the folder with any static host
(`python3 -m http.server`, Vercel, Netlify). Opening `index.html` by double-click will not load the modules.
`prohomehero.html` (built by `build_single.py`) is the same site as one self-contained file.

## Before launch

Edit the `SITE` block at the top of `js/main.js`:

| Setting | What it does |
| --- | --- |
| `phone`, `phoneDisplay`, `email` | Contact details. Phone is `+14705735890`. The email is a placeholder. |
| `FORM_ENDPOINT` | Formspree / Supabase edge function URL. Empty = the form opens the visitor's email app. |
| `gtmId` or `ga4Id` | Google Tag Manager or GA4 id. Empty = no analytics script is loaded. |
| `licenseNo` | Contractor license number. Shown in the footer only when set. |

Also set the real domain in `src/index.src.html` (`canonical`, `og:url`, JSON-LD `url`), `robots.txt` and `sitemap.xml`
(they use `https://www.prohomehero.com/`), and add the street address, service area and `sameAs` links (Google Business Profile, Instagram)
to the JSON-LD block, which currently has name, phone, description and services only.

## Using it with Pure Home and the SEO reporting

The October Pure Home SEO report tracks organic landing pages, Search Console, Google Business Profile, GA4 key events and call tracking.
The site is set up so those tools keep working:

- **Static HTML first.** Every heading, caption, number and link is in the HTML, not injected by script, so crawlers and Search Console see it. One `h1`, sections have ids, images carry descriptive alt text and sizes.
- **Call tracking.** The phone number is in the static HTML as text and as a `tel:` link. Script only rewrites it when `SITE.phone` differs, and never inside an element marked `data-call-tracked`.
- **GA4 / GTM events** pushed to `dataLayer`: `click_to_call` (with placement), `click_financing`, `designer_change`, `designer_quote`, and the form: `generate_lead` when `FORM_ENDPOINT` is set and the post succeeds, `lead_email_opened` when it falls back to the visitor's email app. Mark `generate_lead` as the GA4 key event.
- **Attribution.** `utm_*`, `gclid`, `gbraid`, `wbraid`, `msclkid`, `fbclid`, landing page and referrer are kept for the visit and sent with every lead (the Google Business Profile `?utm_source=google&utm_medium=gbp` link works as is).
- **Structured data.** `HomeAndConstructionBusiness` JSON-LD, plus `sitemap.xml` and `robots.txt`.
- **Design tokens.** Every color and font is a CSS variable in `css/tokens.css`, so the same components can be re-themed for Pure Home by changing that one file.

### Dropping the kitchen designer into purehomeus.com

`embed/kitchen-designer.html` is the finishes designer on its own, in one file (about 2 MB). Upload it to the Pure Home host and place it on a page such as the bathroom or kitchen remodeling page:

```html
<iframe src="/kitchen-designer.html?cta=https://purehomeus.com/contact-pure-home&label=Get%20a%20quote&accent=%23667658"
        title="Kitchen finishes designer" width="100%" height="760" loading="lazy" style="border:0"></iframe>
```

Options: `cta` (https link for the button; the chosen finishes are appended as `?finishes=`), `label`, `accent` and `bg` (hex colors).
On every choice the iframe also posts `{ type: "kitchen-designer", state, summary }` to the parent page, so a form on the host page can prefill itself.

## Editing

Change `src/index.src.html`, then:

```
python3 build.py                                  # injects the portfolio list into index.html
npx tailwindcss -c tailwind.config.js -i src/input.css -o css/tailwind.css --minify
python3 build_single.py && python3 build_embed.py  # optional single-file builds
```

Portfolio captions and order are in `build.py`. The tailwind config maps spacing to the tokens and turns Preflight off.

## The rendered kitchen

`render/kitchen.py` builds the kitchen procedurally in Blender (`pip install bpy`) and renders it with Cycles.
`render/run_all.sh` produces the two colour masks and six renders (two views, three counter stones) into `render/out/`; copy them to
`images/designer/` as `A_quartz.jpg`, `B_granite.jpg`, `mask_A.png` and so on. The page recolors cabinets, island and hardware in the browser using the masks.
This replaced the earlier real-time three.js scene: it looks much closer to a photograph, but you choose between two fixed camera views instead of dragging the room.

## Photos

`images/kitchen-*.jpg` are the client's own project photos. Nine of the newer ones (`kitchen-18` to `kitchen-26`, and the hero) came from the Pure Home Instagram folder.
