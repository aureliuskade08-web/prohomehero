/* ------------------------------------------------------------------
 * SITE SETTINGS. Replace these with Pro Home Hero's real details.
 * The phone and email below are PLACEHOLDERS.
 * Set FORM_ENDPOINT (Formspree, Supabase edge function, etc.) to receive leads;
 * with it empty, the forms open the visitor's email app addressed to `email`.
 * ------------------------------------------------------------------ */
const SITE = {
  phone: "+15555550123",
  phoneDisplay: "(555) 555-0123",
  email: "hello@prohomehero.com",
  FORM_ENDPOINT: "",
};
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* contact details */
$$("[data-tel]").forEach((a) => (a.href = `tel:${SITE.phone}`));
$$("[data-phone-text]").forEach((n) => (n.textContent = SITE.phoneDisplay));
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

/* ---------------- 3D designer (lazy: loads when scrolled near) ---------------- */
const host = $("#kitchen3d");
let designNote = "";
const swatch = (hex) => (hex ? `<i style="background:${hex}"></i>` : "");
async function bootKitchen() {
  try {
    const { mountKitchen } = await import("./kitchen3d.js");
    const k = mountKitchen(host, (_, summary) => {
      designNote = summary;
      $("#designSummary").textContent = summary;
      $$("#finishes .opt").forEach((b) => b.setAttribute("aria-pressed", String(k.state[b.dataset.g] === b.dataset.k)));
    });
    const groups = [
      ["cabinets", "Cabinets"], ["island", "Island"], ["hardware", "Hardware"], ["counter", "Countertop"],
    ];
    $("#finishes").innerHTML = groups.map(([g, label]) => `
      <fieldset class="opt-group"><legend>${label}</legend><div class="opt-row">
        ${Object.entries(k.FINISHES[g]).map(([key, v]) => `<button type="button" class="opt" data-g="${g}" data-k="${key}" aria-pressed="false">${swatch(v.hex)}${v.label}</button>`).join("")}
      </div></fieldset>`).join("");
    $("#finishes").addEventListener("click", (e) => {
      const b = e.target.closest(".opt"); if (b) k.set(b.dataset.g, b.dataset.k);
    });
    k.init();
  } catch (err) {
    console.error(err);
    host.innerHTML = `<p class="kitchen3d__hint">The 3D designer needs WebGL. You can still tell us what you have in mind below.</p>`;
  }
}
new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { o.disconnect(); bootKitchen(); } }, { rootMargin: "400px" }).observe(host);

$("#designCta").addEventListener("click", () => {
  const box = $("#messageBox");
  if (designNote && !box.value.includes("Kitchen designer picks")) {
    box.value = (box.value ? box.value + "\n\n" : "") + "Kitchen designer picks: " + designNote;
  }
  $("#serviceSel").value = "Full kitchen remodel";
});

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
  if (await send({ form: "estimate", ...d }, st, "Thanks, we got it. We'll be in touch to set up your free consultation.", "Free estimate request")) {
    if (SITE.FORM_ENDPOINT) f.reset();
  }
});
