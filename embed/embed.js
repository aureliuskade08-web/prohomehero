import { mountDesigner } from "./designer.js";
/* Query options: ?cta=https://example.com/contact  ?label=Get a quote  ?accent=%23293E35  ?bg=%23E7DFD0 */
const q = new URLSearchParams(location.search);
const $ = (s) => document.querySelector(s);
const okColor = (c) => /^#[0-9a-f]{6}$/i.test(c || "");
if (okColor(q.get("accent"))) document.documentElement.style.setProperty("--color-accent", q.get("accent"));
if (okColor(q.get("bg"))) document.documentElement.style.setProperty("--color-blush", q.get("bg"));
const cta = $("#designCta");
const to = q.get("cta");
if (to && /^https:\/\//i.test(to)) cta.href = to; else cta.removeAttribute("target");
if (q.get("label")) cta.textContent = q.get("label").slice(0, 40);
const assetUrl = (n) => (window.__HH_ASSETS && window.__HH_ASSETS[n]) || `../images/designer/${n}`;
const swatch = (hex) => (hex ? `<i style="background:${hex}"></i>` : "");
const k = mountDesigner({
  canvas: $("#kitchenCv"), viewsHost: $("#kitchenViews"), assetUrl,
  onChange: (group, summary) => {
    $("#designSummary").textContent = summary;
    document.querySelectorAll("#finishes .opt").forEach((b) => b.setAttribute("aria-pressed", String(k.state[b.dataset.g] === b.dataset.k)));
    if (group !== "init") {
      // lets the host page (for example a quote form) pick up the choices
      parent.postMessage({ type: "kitchen-designer", state: { ...k.state }, summary }, "*");
      (window.dataLayer = window.dataLayer || []).push({ event: "designer_change", finish_group: group, finish_choice: k.state[group] });
    }
    if (to && /^https:\/\//i.test(to)) { try { const u = new URL(to); u.searchParams.set("finishes", summary); cta.href = u.toString(); } catch {} }
  },
});
const groups = [["cabinets", "Cabinets"], ["island", "Island"], ["hardware", "Hardware"], ["counter", "Countertop"]];
$("#finishes").innerHTML = groups.map(([g, label]) => `
  <fieldset class="opt-group"><legend>${label}</legend><div class="opt-row">
    ${Object.entries(k.FINISHES[g]).map(([key, v]) => `<button type="button" class="opt" data-g="${g}" data-k="${key}" aria-pressed="false">${swatch(v.hex)}${v.label}</button>`).join("")}
  </div></fieldset>`).join("");
$("#finishes").addEventListener("click", (e) => { const b = e.target.closest(".opt"); if (b) k.set(b.dataset.g, b.dataset.k); });
k.init();
