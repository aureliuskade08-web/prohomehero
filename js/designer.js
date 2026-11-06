/**
 * Finishes designer. A kitchen rendered once in Blender (Cycles: real shadows, sunlight and materials)
 * is recoloured live in the browser. Per view there is one colour mask where red marks cabinets, green the
 * island and blue the hardware, and three renders that differ only in the countertop stone.
 * Nothing here is brand specific: the page supplies the host element, the option groups and the asset URLs.
 */
export const FINISHES = {
  cabinets: {
    white: { label: "Warm white", hex: "#EFE9DF" },
    blush: { label: "Blush", hex: "#E3C9BE" },
    sage: { label: "Sage", hex: "#93A184" },
    blue: { label: "Dusty blue", hex: "#8EA3B6" },
    greige: { label: "Greige", hex: "#C6BAAA" },
    navy: { label: "Navy", hex: "#33445C" },
  },
  island: {
    match: { label: "Match cabinets" },
    sage: { label: "Sage", hex: "#93A184" },
    blue: { label: "Dusty blue", hex: "#8EA3B6" },
    navy: { label: "Navy", hex: "#33445C" },
    blush: { label: "Blush", hex: "#E3C9BE" },
  },
  hardware: {
    brass: { label: "Brushed brass", hex: "#C79A55" },
    black: { label: "Matte black", hex: "#1F1E1D" },
    nickel: { label: "Polished nickel", hex: "#C8CCD1" },
  },
  counter: {
    quartz: { label: "White quartz", hex: "#EFEDE8" },
    granite: { label: "Warm granite", hex: "#B9A58A" },
    slate: { label: "Charcoal soapstone", hex: "#3B3C3E" },
  },
};
export const VIEWS = { A: "Island", B: "Range wall" };

const hexToRgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));

export function mountDesigner({ canvas, viewsHost, assetUrl, onChange }) {
  const ctx = canvas.getContext("2d", { willReadFrequently: true });
  const state = { cabinets: "white", island: "match", hardware: "brass", counter: "quartz", view: "A" };
  const cache = new Map(); // url -> Promise<ImageData>
  const W = canvas.width, H = canvas.height;
  const off = document.createElement("canvas"); off.width = W; off.height = H;
  const octx = off.getContext("2d", { willReadFrequently: true });

  const load = (name) => {
    if (!cache.has(name)) {
      cache.set(name, new Promise((res, rej) => {
        const im = new Image(); im.decoding = "async";
        im.onload = () => { octx.clearRect(0, 0, W, H); octx.drawImage(im, 0, 0, W, H); res(octx.getImageData(0, 0, W, H)); };
        im.onerror = rej; im.src = assetUrl(name);
      }));
    }
    return cache.get(name);
  };

  const refCache = new Map();
  function reference(view, base, mask) {
    const key = view;
    if (refCache.has(key)) return refCache.get(key);
    let r = 0, g = 0, b = 0, n = 0;
    for (let i = 0; i < base.data.length; i += 4) {
      if (mask.data[i] > 235 && mask.data[i + 1] < 20) { r += base.data[i]; g += base.data[i + 1]; b += base.data[i + 2]; n++; }
    }
    const ref = n ? [r / n, g / n, b / n] : [225, 224, 222];
    refCache.set(key, ref);
    return ref;
  }

  let token = 0;
  async function draw() {
    const mine = ++token;
    const [base, mask] = await Promise.all([load(`${state.view}_${state.counter}.jpg`), load(`mask_${state.view}.png`)]);
    if (mine !== token) return;
    const ref = reference(state.view, base, mask);
    const cab = hexToRgb(FINISHES.cabinets[state.cabinets].hex);
    const isl = state.island === "match" ? cab : hexToRgb(FINISHES.island[state.island].hex);
    const hw = state.hardware;
    const out = ctx.createImageData(W, H);
    const bd = base.data, md = mask.data, od = out.data;
    const kc = [cab[0] / ref[0], cab[1] / ref[1], cab[2] / ref[2]];
    const ki = [isl[0] / ref[0], isl[1] / ref[1], isl[2] / ref[2]];
    for (let i = 0; i < bd.length; i += 4) {
      const r = bd[i], g = bd[i + 1], b = bd[i + 2];
      const wc = md[i] / 255, wi = md[i + 1] / 255, wh = md[i + 2] / 255;
      const w = wc + wi + wh;
      if (w < 0.004) { od[i] = r; od[i + 1] = g; od[i + 2] = b; od[i + 3] = 255; continue; }
      const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
      let R = r * (1 - w), G = g * (1 - w), B = b * (1 - w);
      if (wc > 0 || wi > 0) {
        // paint: scale the lit surface by target / reference and keep the highlights the render added
        const spec = Math.max(0, lum - ref[1] * 1.12) * 0.9;
        if (wc > 0) { R += Math.min(255, r * kc[0] + spec) * wc; G += Math.min(255, g * kc[1] + spec) * wc; B += Math.min(255, b * kc[2] + spec) * wc; }
        if (wi > 0) { R += Math.min(255, r * ki[0] + spec) * wi; G += Math.min(255, g * ki[1] + spec) * wi; B += Math.min(255, b * ki[2] + spec) * wi; }
      }
      if (wh > 0) {
        if (hw === "brass") { R += r * wh; G += g * wh; B += b * wh; }
        else if (hw === "black") { const v = lum * 0.2 + Math.max(0, lum - 170) * 0.8; R += v * wh; G += v * wh; B += v * 1.03 * wh; }
        else { const v = Math.min(255, lum * 1.3 + 22); R += v * 0.95 * wh; G += v * 0.97 * wh; B += v * wh; }
      }
      od[i] = R; od[i + 1] = G; od[i + 2] = B; od[i + 3] = 255;
    }
    ctx.putImageData(out, 0, 0);
  }

  const labelOf = (g, k) => FINISHES[g][k].label;
  const summary = () =>
    `Cabinets: ${labelOf("cabinets", state.cabinets)}. Island: ${labelOf("island", state.island)}. Hardware: ${labelOf("hardware", state.hardware)}. Countertop: ${labelOf("counter", state.counter)}.`;

  let raf = 0;
  const schedule = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => draw().catch(console.error)); };

  if (viewsHost) {
    viewsHost.innerHTML = Object.entries(VIEWS).map(([k, v]) => `<button type="button" class="opt" data-view="${k}" aria-pressed="${k === state.view}">${v}</button>`).join("");
    viewsHost.addEventListener("click", (e) => {
      const b = e.target.closest("[data-view]"); if (!b) return;
      state.view = b.dataset.view;
      viewsHost.querySelectorAll("[data-view]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      schedule();
    });
  }

  const api = {
    state, FINISHES, summary,
    set(group, key) { state[group] = key; onChange?.(group, summary()); schedule(); },
    init() { onChange?.("init", summary()); schedule(); },
  };
  return api;
}
