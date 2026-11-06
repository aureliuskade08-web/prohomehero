# Home Hero website: handoff for SEO

Static site (HTML, CSS, plain JavaScript). No CMS, no database. Open `index.html` through any web server
(`python3 -m http.server`) or upload the folder to any static host. Double-clicking the file will not load the scripts.

## Where things are
- `index.html` : the home page. `services/<name>/index.html` : six service pages, generated from `pages.py` by `python3 build_pages.py`. All headings, text, image alt text and links are in the HTML. `src/index.src.html` is the editable source of the same page (see README for the one build step that fills the portfolio list).
- `css/` : styles. Colors and fonts are variables in `css/tokens.css`.
- `js/main.js` : site settings at the top (phone, email, form endpoint, analytics id, license number).
- `images/` : photos. `images/hero-kitchen.jpg` is the hero and social-sharing image.
- `sitemap.xml`, `robots.txt` : set for https://www.prohomehero.com/.
- `embed/kitchen-designer.html` : the finishes designer on its own, for embedding elsewhere.

## Already in place
- One H1, section ids, descriptive alt text, page title and description, canonical URL, Open Graph tags.
- Business structured data (HomeAndConstructionBusiness JSON-LD) with name, phone, description and services.
- Phone number is plain text plus a tel: link, so call-tracking scripts can swap it (elements marked data-call-tracked are never rewritten).
- Google Tag Manager or GA4: set `gtmId` or `ga4Id` in `js/main.js`. Nothing loads until an id is set.
- Events pushed to dataLayer: click_to_call, click_financing, designer_change, designer_quote, generate_lead (form posted), lead_email_opened.
- UTM parameters and ad click ids (gclid etc.) are saved for the visit and sent with each lead.

## Still needed from the business
- Street address or service area, hours, license number, Instagram/Facebook/Google Business Profile links (add to the JSON-LD block and the footer).
- Google Analytics / Tag Manager id, and a form endpoint (the form currently opens the visitor's email app, addressed to info@prohomehero.com).
- Confirm the business name: the Google listing says "Home Heroes", the site says "Home Hero". Make them match.

## Likely next steps for SEO
- Pages for each service area once the cities served are confirmed (the six service pages already exist; see README, Adding pages).
- Local landing content, project pages, reviews.
- Add the real domain DNS, then verify in Google Search Console.
