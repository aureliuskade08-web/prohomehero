/* ------------------------------------------------------------------
 * SITE SETTINGS. Everything the site owner or the SEO agency may need to change lives here.
 *  - phone / phoneDisplay / email: contact details used across the page (static HTML carries the same values,
 *    so call-tracking scripts that swap the number in the DOM keep working)
 *  - FORM_ENDPOINT: Formspree, Supabase edge function, etc. Empty = the form opens the visitor's email app.
 *  - gtmId / ga4Id: Google Tag Manager or GA4 measurement id. Empty = no analytics are loaded.
 *  - licenseNo: the contractor licence number, shown in the footer only when set.
 * ------------------------------------------------------------------ */
const SITE = {
  phone: "+14705735890",
  phoneDisplay: "(470) 573-5890",
  email: "info@prohomehero.com",
  FORM_ENDPOINT: "",
  gtmId: "",
  ga4Id: "",
  licenseNo: "",
  source: "home-hero",
};
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* analytics: loaded only when an id is set, and every key action is pushed to dataLayer */
window.dataLayer = window.dataLayer || [];
const track = (event, params = {}) => window.dataLayer.push({ event, site: SITE.source, ...params });
if (SITE.gtmId) {
  dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
  const g = document.createElement("script"); g.async = true; g.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(SITE.gtmId)}`; document.head.append(g);
} else if (SITE.ga4Id) {
  window.gtag = function () { dataLayer.push(arguments); };
  gtag("js", new Date()); gtag("config", SITE.ga4Id);
  const g = document.createElement("script"); g.async = true; g.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(SITE.ga4Id)}`; document.head.append(g);
}

/* campaign attribution: keep utm_* and click ids for the whole visit so the lead carries its source */
const ATTR_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "msclkid", "fbclid"];
const attribution = (() => {
  let saved = {};
  try { saved = JSON.parse(sessionStorage.getItem("hh_attr") || "{}"); } catch {}
  const q = new URLSearchParams(location.search);
  ATTR_KEYS.forEach((k) => { if (q.get(k)) saved[k] = q.get(k); });
  if (!saved.landing) saved.landing = location.pathname;
  if (!saved.referrer && document.referrer) saved.referrer = document.referrer;
  try { sessionStorage.setItem("hh_attr", JSON.stringify(saved)); } catch {}
  return saved;
})();

/* contact details: only rewrite when the settings differ from the static HTML (call tracking may have swapped it) */
$$("[data-tel]").forEach((a) => { if (a.getAttribute("href") !== `tel:${SITE.phone}`) a.href = `tel:${SITE.phone}`; });
$$("[data-phone-text]").forEach((n) => { if (n.textContent !== SITE.phoneDisplay && !n.closest("[data-call-tracked]")) n.textContent = SITE.phoneDisplay; });
$$("[data-license-text]").forEach((n) => { if (SITE.licenseNo) { n.textContent = `, license no. ${SITE.licenseNo}`; n.hidden = false; } });
$$("[data-tel]").forEach((a) => a.addEventListener("click", () => track("click_to_call", { placement: a.closest("footer") ? "footer" : a.closest("#stickyCta") ? "mobile_bar" : a.closest("header") ? "nav" : "page" })));
$$("[data-mail]").forEach((a) => (a.href = `mailto:${SITE.email}`));
$$("[data-email-text]").forEach((n) => (n.textContent = SITE.email));
$("#yr").textContent = new Date().getFullYear();

/* mobile menu */
const menu = $("#mobileMenu"), burger = $("#menuBtn");
const toggleMenu = (open) => {
  menu.hidden = !open;
  burger.setAttribute("aria-expanded", String(open));
  document.body.style.overflow = open ? "hidden" : "";
  if (open) $("#menuClose").focus(); else burger.focus();
};
burger.addEventListener("click", () => toggleMenu(true));
$("#menuClose").addEventListener("click", () => toggleMenu(false));
$$("a", menu).forEach((a) => a.addEventListener("click", () => toggleMenu(false)));
addEventListener("keydown", (e) => { if (e.key === "Escape" && !menu.hidden) toggleMenu(false); });

/* ---------------- portfolio: reveal + lightbox ---------------- */
const moreBtn = $("#moreBtn");
const extras = $$("#gallery [data-extra]");
moreBtn.addEventListener("click", () => {
  const open = moreBtn.getAttribute("aria-expanded") === "true";
  extras.forEach((li) => (li.hidden = open));
  moreBtn.setAttribute("aria-expanded", String(!open));
  moreBtn.textContent = open ? "See more projects" : "Show fewer projects";
  if (open) $("#portfolio").scrollIntoView({ behavior: "smooth" });
});

const lb = $("#lightbox"), lbImg = $("#lbImg"), lbCap = $("#lbCap");
const shots = $$("#gallery .g-btn");
const viewImg = $("#viewImg");
const preview = (b) => {
  if (!viewImg) return;
  viewImg.src = b.dataset.src; viewImg.alt = b.dataset.cap;
  $$("#gallery .g-item").forEach((li) => li.classList.toggle("is-active", li === b.parentElement));
  viewImg.closest("button").dataset.i = b.dataset.i;
};
shots.forEach((b) => { b.addEventListener("mouseenter", () => preview(b)); b.addEventListener("focus", () => preview(b)); });
if (shots[0]) preview(shots[0]);
$("#viewBtn")?.addEventListener("click", (e) => { const i = Number(e.currentTarget.dataset.i || 0); show(i); lb.showModal(); });
let cur = 0;
const show = (i) => {
  cur = (i + shots.length) % shots.length;
  const b = shots[cur];
  lbImg.src = b.dataset.src; lbImg.alt = b.dataset.cap; lbCap.textContent = b.dataset.cap;
};
shots.forEach((b, i) => b.addEventListener("click", () => { show(i); lb.showModal(); }));
$("#lbClose").addEventListener("click", () => lb.close());
$("#lbPrev").addEventListener("click", () => show(cur - 1));
$("#lbNext").addEventListener("click", () => show(cur + 1));
$("#lbCta").addEventListener("click", () => lb.close());
lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
lb.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft") show(cur - 1);
  if (e.key === "ArrowRight") show(cur + 1);
});

/* ---------------- services → prefill the form ---------------- */
$$("[data-service]").forEach((a) =>
  a.addEventListener("click", () => { $("#serviceSel").value = a.dataset.service; })
);

/* ---------------- finishes designer (a rendered kitchen, recoloured live; loads when scrolled near) ---------------- */
const host = $("#kitchen3d");
let designNote = "";
const swatch = (hex) => (hex ? `<i style="background:${hex}"></i>` : "");
async function bootKitchen() {
  try {
    const { mountDesigner } = await import("./designer.js");
    const assetUrl = (n) => (window.__HH_ASSETS && window.__HH_ASSETS[n]) || `images/designer/${n}`;
    const k = mountDesigner({
      canvas: $("#kitchenCv"), viewsHost: $("#kitchenViews"), assetUrl,
      onChange: (group, summary) => {
        designNote = summary;
        $("#designSummary").textContent = summary;
        $$("#finishes .opt").forEach((b) => b.setAttribute("aria-pressed", String(k.state[b.dataset.g] === b.dataset.k)));
        if (group !== "init") track("designer_change", { finish_group: group, finish_choice: k.state[group] });
      },
    });
    const groups = [["cabinets", "Cabinets"], ["island", "Island"], ["hardware", "Hardware"], ["counter", "Countertop"]];
    $("#finishes").innerHTML = groups.map(([g, label]) => `
      <fieldset class="opt-group"><legend>${label}</legend><div class="opt-row">
        ${Object.entries(k.FINISHES[g]).map(([key, v]) => `<button type="button" class="opt" data-g="${g}" data-k="${key}" aria-pressed="false">${swatch(v.hex)}${v.label}</button>`).join("")}
      </div></fieldset>`).join("");
    $("#finishes").addEventListener("click", (e) => { const b = e.target.closest(".opt"); if (b) k.set(b.dataset.g, b.dataset.k); });
    k.init();
  } catch (err) {
    console.error(err);
    $("#kitchen3d").insertAdjacentHTML("beforeend", `<p class="kitchen3d__note">The preview could not load. You can still tell us what you have in mind below.</p>`);
  }
}
new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { o.disconnect(); bootKitchen(); } }, { rootMargin: "400px" }).observe(host);

$("#designCta").addEventListener("click", () => {
  const box = $("#messageBox");
  if (designNote && !box.value.includes("Kitchen designer picks")) {
    box.value = (box.value ? box.value + "\n\n" : "") + "Kitchen designer picks: " + designNote;
  }
  $("#serviceSel").value = "Full kitchen remodel";
  track("designer_quote");
});

/* financing: prefill the form's topic */
$$("[data-financing]").forEach((a) => a.addEventListener("click", () => { $("#serviceSel").value = "Financing question"; track("click_financing"); }));

/* ---------------- forms ---------------- */
async function send(payload, statusEl, okMsg, subject) {
  statusEl.textContent = "Sending…";
  try {
    if (SITE.FORM_ENDPOINT) {
      const r = await fetch(SITE.FORM_ENDPOINT, {
        method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) throw new Error(r.status);
      statusEl.textContent = okMsg; return true;
    }
    const body = Object.entries(payload).map(([k, v]) => `${k}: ${v}`).join("\n");
    location.href = `mailto:${SITE.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    statusEl.textContent = "Your email app should open with the details filled in. Nothing is sent until you press send there.";
    return true;
  } catch {
    statusEl.textContent = `Something went wrong sending that. Please call ${SITE.phoneDisplay} or try again.`;
    return false;
  }
}
$("#estimateForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = e.target, st = $("#formStatus");
  const d = Object.fromEntries(new FormData(f));
  if (!d.name?.trim() || !d.phone?.trim() || !/^\S+@\S+\.\S+$/.test(d.email || "")) {
    st.textContent = "Please add your name, phone number and a valid email so we can reach you."; return;
  }
  const payload = { form: "estimate", site: SITE.source, ...d, ...attribution, page: location.href };
  if (await send(payload, st, "Thanks, we got it. We'll be in touch to set up your free consultation.", "Free estimate request")) {
    track(SITE.FORM_ENDPOINT ? "generate_lead" : "lead_email_opened", { form: "estimate", service: d.service });
    if (SITE.FORM_ENDPOINT) f.reset();
  }
});
