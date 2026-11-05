/**
 * Image stream hero — vanilla port of the 21st.dev <ImageStreamHero /> component.
 *
 * Two rails of photo cards ride from far behind the screen toward the viewer.
 * Perspective alone does the work: as a card's z grows it gets bigger AND its screen x
 * sweeps outward, because projection scales position and size by the same factor.
 * Every length is in `cqw` (percent of the container's width) so the corridor keeps
 * its proportions at any size. See the original component for the geometry notes.
 */
const DEFAULT_PATH = {
  perspective: 30,
  cardWidth: 18,
  cardHeight: 25,
  cardRadius: 0.4,
  birthHeight: 2.6,
  exitHeight: 46,
  railBirth: -11,
  railExit: 44,
  fan: 3.3,
  turnBirth: 6,
  turnExit: 28,
  stops: 24,
};

function keyframes(dir, name, p) {
  const steps = [];
  for (let s = 0; s <= p.stops; s++) {
    const u = s / p.stops;
    // geometric in apparent size → consecutive cards keep a constant size ratio
    const scale = (p.birthHeight / p.cardHeight) * Math.pow(p.exitHeight / p.birthHeight, u);
    const z = p.perspective * (1 - 1 / scale);
    const rail = p.railExit - (p.railExit - p.railBirth) * Math.pow(1 - u, p.fan);
    const turn = p.turnBirth + (p.turnExit - p.turnBirth) * u;
    steps.push(
      `${(u * 100).toFixed(2)}%{transform:translate3d(${(dir * rail).toFixed(2)}cqw,0,${z.toFixed(2)}cqw) rotateY(${(-dir * turn).toFixed(2)}deg)}`
    );
  }
  return `@keyframes ${name}{${steps.join("")}}`;
}

/**
 * @param {HTMLElement} root   element that becomes the container (needs position + size from CSS)
 * @param {{src:string, alt?:string}[]} images
 * @param {{cards?:number, speed?:number, axis?:number, path?:object}} [opts]
 */
export function mountImageStream(root, images, opts = {}) {
  const cards = opts.cards ?? 9;
  const speed = opts.speed ?? 18;
  const axis = opts.axis ?? 55;
  const p = { ...DEFAULT_PATH, ...(opts.path || {}) };
  const id = Math.random().toString(36).slice(2, 8);
  const right = `ish-r-${id}`;
  const left = `ish-l-${id}`;
  const cardCls = `ish-c-${id}`;

  const style = document.createElement("style");
  style.textContent =
    keyframes(1, right, p) +
    keyframes(-1, left, p) +
    // Pausing (not disabling) keeps the corridor whole for reduced-motion users:
    // every card is dropped mid-flight by its negative delay, so it freezes as a finished still.
    `@media(prefers-reduced-motion:reduce){.${cardCls}{animation-play-state:paused!important}}`;
  root.appendChild(style);
  root.style.containerType = "inline-size";

  const stage = document.createElement("div");
  stage.setAttribute("aria-hidden", "true");
  stage.className = "pointer-events-none absolute inset-0";
  stage.style.perspective = `${p.perspective}cqw`;
  stage.style.perspectiveOrigin = `50% ${axis}%`;

  const inner = document.createElement("div");
  inner.className = "absolute inset-0";
  inner.style.transformStyle = "preserve-3d";
  stage.appendChild(inner);

  // The original walks both rails through the same sequence. With 17 photos we offset the
  // left rail so the two sides show different kitchens while still mirroring the geometry.
  const n = Math.max(images.length, 1);
  [[right, 0], [left, Math.floor(n / 2)]].forEach(([name, offset]) => {
    for (let i = 0; i < cards; i++) {
      const img = images[(i + offset) % n];
      const el = document.createElement("div");
      el.className = `${cardCls} absolute overflow-hidden`;
      Object.assign(el.style, {
        left: "50%",
        top: `${axis}%`,
        width: `${p.cardWidth}cqw`,
        height: `${p.cardHeight}cqw`,
        marginLeft: `${-p.cardWidth / 2}cqw`,
        marginTop: `${-p.cardHeight / 2}cqw`,
        borderRadius: `${p.cardRadius}cqw`,
        animation: `${name} ${speed}s linear infinite`,
        animationDelay: `${-(i * speed) / cards}s`,
        backfaceVisibility: "hidden",
        willChange: "transform",
      });
      if (img) {
        const im = document.createElement("img");
        im.src = img.src;
        im.alt = "";
        im.decoding = "async";
        im.draggable = false;
        im.className = "h-full w-full object-cover";
        el.appendChild(im);
      }
      inner.appendChild(el);
    }
  });

  root.prepend(stage);
  return {
    pause: () => root.querySelectorAll(`.${cardCls}`).forEach((c) => (c.style.animationPlayState = "paused")),
    play: () => root.querySelectorAll(`.${cardCls}`).forEach((c) => (c.style.animationPlayState = "running")),
  };
}
