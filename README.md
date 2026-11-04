# Pro Home Hero website

Open `index.html` through any static server (e.g. `python3 -m http.server`) — the 3D designer uses ES modules, so double-clicking the file won't load it. Deploys as-is to Vercel/Netlify.

Before launch, edit the SITE block at the top of `js/main.js`:
- `phone`, `phoneDisplay`, `email` are PLACEHOLDERS. Also update the `tel:` / `mailto:` defaults in `src/index.src.html`.
- `FORM_ENDPOINT`: your Formspree / Supabase function URL. While empty, forms open the visitor's email app.

Editing: change `src/index.src.html`, then `python3 build.py` (injects the gallery) and
`npx tailwindcss -c tailwind.config.js -i src/input.css -o css/tailwind.css --minify`.
Gallery captions/order live in `build.py`. Palette tokens live in `tailwind.config.js`.
