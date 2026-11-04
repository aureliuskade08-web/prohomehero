import * as THREE from "../vendor/three.module.min.js";

/**
 * Interactive 3D kitchen designer. A procedural kitchen is built from boxes so it loads instantly
 * (no model files), and cabinet / island / hardware / countertop choices recolor it live.
 */
const FINISHES = {
  cabinets: {
    white: { label: "Bright white", hex: "#F1EEE8" },
    navy: { label: "Navy", hex: "#1F2A3C" },
    sage: { label: "Sage", hex: "#6F7A5B" },
    greige: { label: "Warm gray", hex: "#B3ABA0" },
    walnut: { label: "Walnut", hex: "#5A3626" },
  },
  island: {
    match: { label: "Match cabinets" },
    espresso: { label: "Espresso", hex: "#2E1F19" },
    navy: { label: "Navy", hex: "#1F2A3C" },
    walnut: { label: "Walnut", hex: "#6B4330" },
  },
  hardware: {
    brass: { label: "Brushed brass", hex: "#B58B4A", metal: 0.9, rough: 0.35 },
    black: { label: "Matte black", hex: "#15130F", metal: 0.3, rough: 0.55 },
  },
  counter: {
    quartz: { label: "White quartz", hex: "#EFEBE4" },
    granite: { label: "Gray granite", hex: "#8C8C8A" },
    slate: { label: "Charcoal", hex: "#38363A" },
  },
};

export function mountKitchen(canvasHost, onChange) {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const state = { cabinets: "white", island: "espresso", hardware: "brass", counter: "quartz" };

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  canvasHost.appendChild(renderer.domElement);
  renderer.domElement.setAttribute("aria-label", "Interactive 3D kitchen. Drag to rotate.");
  renderer.domElement.style.touchAction = "pan-y";
  renderer.domElement.style.cursor = "grab";

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 60);
  const target = new THREE.Vector3(0, 1.05, -0.2);

  // ---- materials (color is animated toward the chosen finish) ----
  const mats = {
    cab: new THREE.MeshStandardMaterial({ color: FINISHES.cabinets.white.hex, roughness: 0.55 }),
    isl: new THREE.MeshStandardMaterial({ color: FINISHES.island.espresso.hex, roughness: 0.55 }),
    hw: new THREE.MeshStandardMaterial({ color: FINISHES.hardware.brass.hex, metalness: 0.9, roughness: 0.35 }),
    top: new THREE.MeshStandardMaterial({ color: FINISHES.counter.quartz.hex, roughness: 0.25 }),
    wall: new THREE.MeshStandardMaterial({ color: "#E8DFD0", roughness: 0.95 }),
    floor: new THREE.MeshStandardMaterial({ color: "#C9B08C", roughness: 0.75 }),
    steel: new THREE.MeshStandardMaterial({ color: "#9A9A9A", metalness: 0.85, roughness: 0.3 }),
    dark: new THREE.MeshStandardMaterial({ color: "#1b1b1b", roughness: 0.4 }),
    leather: new THREE.MeshStandardMaterial({ color: "#4A2C20", roughness: 0.6 }),
    glow: new THREE.MeshBasicMaterial({ color: "#FFE9B8" }),
  };
  const goal = {
    cab: new THREE.Color(mats.cab.color), isl: new THREE.Color(mats.isl.color),
    hw: new THREE.Color(mats.hw.color), top: new THREE.Color(mats.top.color),
  };

  const box = (w, h, d, m, x, y, z, parent = scene, shadow = true) => {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
    mesh.position.set(x, y, z);
    mesh.castShadow = shadow; mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
  };
  const hardwareMeshes = [];
  const pull = (x, y, z, vertical = false) => {
    const g = new THREE.CylinderGeometry(0.011, 0.011, 0.14, 10);
    const m = new THREE.Mesh(g, mats.hw);
    m.position.set(x, y, z);
    if (!vertical) m.rotation.z = Math.PI / 2;
    m.castShadow = true;
    scene.add(m);
    hardwareMeshes.push(m);
  };

  // ---- room ----
  const W = 6, D = 5;
  box(W, 0.1, D, mats.floor, 0, -0.05, 0.4, scene, false);
  box(W, 3, 0.1, mats.wall, 0, 1.5, -2.1, scene, false); // back wall
  box(0.1, 3, D, mats.wall, -W / 2, 1.5, 0.4, scene, false); // left wall

  // ---- back run: base cabinets, counter, backsplash, uppers ----
  const runZ = -1.75, baseD = 0.6, baseH = 0.88;
  const bays = 5, bayW = 0.92, x0 = -(bays - 1) * bayW / 2 - 0.2;
  for (let i = 0; i < bays; i++) {
    const x = x0 + i * bayW;
    box(bayW - 0.012, baseH, baseD, mats.cab, x, baseH / 2, runZ);
    // shaker door panel (raised frame illusion via slightly proud slab + recessed inner)
    box(bayW - 0.07, baseH - 0.1, 0.02, mats.cab, x, baseH / 2, runZ + baseD / 2 + 0.008);
    box(bayW - 0.2, baseH - 0.24, 0.012, mats.cab, x, baseH / 2, runZ + baseD / 2 + 0.022).material = mats.cab;
    pull(x + bayW / 2 - 0.1, baseH - 0.12, runZ + baseD / 2 + 0.05, true);
  }
  const runW = bays * bayW;
  box(runW + 0.04, 0.04, baseD + 0.04, mats.top, x0 + (bays - 1) * bayW / 2, baseH + 0.02, runZ + 0.01);
  box(runW + 0.04, 0.62, 0.02, mats.top, x0 + (bays - 1) * bayW / 2, baseH + 0.04 + 0.31, -2.04, scene, false); // slab backsplash
  // sink + faucet
  const sinkX = x0 + 2 * bayW;
  box(0.7, 0.012, 0.42, mats.steel, sinkX, baseH + 0.045, runZ + 0.04, scene, false);
  const tap = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.012, 8, 20, Math.PI), mats.hw);
  tap.position.set(sinkX, baseH + 0.3, runZ - 0.2); tap.castShadow = true; scene.add(tap); hardwareMeshes.push(tap);
  const tapBase = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.24, 10), mats.hw);
  tapBase.position.set(sinkX - 0.1, baseH + 0.17, runZ - 0.2); scene.add(tapBase); hardwareMeshes.push(tapBase);
  // range
  const rangeX = x0 + 4 * bayW - 0.0;
  box(bayW - 0.03, 0.04, baseD - 0.05, mats.dark, rangeX, baseH + 0.05, runZ, scene, false);
  for (let k = 0; k < 4; k++) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.02, 16), mats.dark);
    b.position.set(rangeX + (k % 2 ? 0.14 : -0.14), baseH + 0.075, runZ + (k < 2 ? 0.1 : -0.1));
    scene.add(b);
  }
  // uppers
  const upY = 1.95, upH = 0.9, upD = 0.35;
  for (let i = 0; i < bays; i++) {
    if (i === 4) continue; // open space above range for a hood
    const x = x0 + i * bayW;
    box(bayW - 0.012, upH, upD, mats.cab, x, upY, -2.04 + upD / 2 + 0.02);
    box(bayW - 0.07, upH - 0.1, 0.02, mats.cab, x, upY, -2.04 + upD + 0.03);
    pull(x + bayW / 2 - 0.1, upY - 0.3, -2.04 + upD + 0.07, true);
  }
  // hood
  box(0.8, 0.4, 0.45, mats.steel, rangeX, 2.15, -1.8);
  // floating shelf
  box(1.2, 0.04, 0.24, new THREE.MeshStandardMaterial({ color: "#7A4A32", roughness: 0.7 }), x0 - 1.4, 1.7, -1.95, scene, false);

  // ---- island ----
  const iz = 0.55, iw = 2.5, id = 0.95, ih = 0.9;
  box(iw, ih, id, mats.isl, 0, ih / 2, iz);
  for (let i = 0; i < 3; i++) {
    const x = -iw / 2 + (i + 0.5) * (iw / 3);
    box(iw / 3 - 0.06, ih - 0.14, 0.02, mats.isl, x, ih / 2, iz + id / 2 + 0.01);
    pull(x, ih - 0.14, iz + id / 2 + 0.05);
  }
  box(iw + 0.12, 0.05, id + 0.28, mats.top, 0, ih + 0.025, iz + 0.14); // overhang toward the stools
  // stools
  for (let i = 0; i < 3; i++) {
    const x = -0.75 + i * 0.75, z = iz + id / 2 + 0.55;
    const seat = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.19, 0.07, 24), mats.leather);
    seat.position.set(x, 0.66, z); seat.castShadow = true; scene.add(seat);
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.63, 8), mats.hw);
    leg.position.set(x, 0.32, z); scene.add(leg); hardwareMeshes.push(leg);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.14, 0.01, 6, 20), mats.hw);
    ring.rotation.x = Math.PI / 2; ring.position.set(x, 0.22, z); scene.add(ring); hardwareMeshes.push(ring);
  }
  // pendants
  for (const x of [-0.6, 0.6]) {
    const cord = new THREE.Mesh(new THREE.CylinderGeometry(0.004, 0.004, 1.1, 6), mats.dark);
    cord.position.set(x, 2.45, iz); scene.add(cord);
    const shade = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.2, 24, 1, true), mats.dark);
    shade.material.side = THREE.DoubleSide;
    shade.position.set(x, 1.82, iz); shade.castShadow = true; scene.add(shade);
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.06, 12, 12), mats.glow);
    bulb.position.set(x, 1.76, iz); scene.add(bulb);
    const pl = new THREE.PointLight("#FFD9A0", 0.9, 4, 2); pl.position.set(x, 1.7, iz); scene.add(pl);
  }
  // fridge
  box(0.95, 2.0, 0.75, mats.steel, x0 - 1.35 - 0.05, 1.0, -1.65);

  // ---- light ----
  scene.add(new THREE.HemisphereLight("#FFF4E3", "#8A6A45", 0.85));
  const sun = new THREE.DirectionalLight("#FFF1DA", 2.2);
  sun.position.set(3.5, 5, 4);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 0.5, far: 18 });
  sun.shadow.bias = -0.0004;
  scene.add(sun);

  // ---- orbit (drag / touch) ----
  let theta = 0.5, phi = 1.2, radius = 9.4;
  let tTheta = theta, tPhi = phi, dragging = false, lastX = 0, lastY = 0, idle = 0;
  const el = renderer.domElement;
  el.addEventListener("pointerdown", (e) => { dragging = true; lastX = e.clientX; lastY = e.clientY; el.setPointerCapture(e.pointerId); el.style.cursor = "grabbing"; });
  el.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    tTheta -= (e.clientX - lastX) * 0.006;
    tPhi = Math.min(1.45, Math.max(0.75, tPhi - (e.clientY - lastY) * 0.004));
    tTheta = Math.min(1.15, Math.max(-0.6, tTheta));
    lastX = e.clientX; lastY = e.clientY; idle = 0;
  });
  const end = () => { dragging = false; el.style.cursor = "grab"; };
  el.addEventListener("pointerup", end); el.addEventListener("pointercancel", end);
  el.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") tTheta = Math.max(-0.6, tTheta - 0.1);
    if (e.key === "ArrowRight") tTheta = Math.min(1.15, tTheta + 0.1);
  });
  el.tabIndex = 0;

  function resize() {
    const { clientWidth: w, clientHeight: h } = canvasHost;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; radius = w / h < 1 ? 13 : 9.4;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(canvasHost); resize();

  // ---- loop (only while visible) ----
  let visible = true, raf = 0, t0 = performance.now();
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; if (visible) loop(); }, { threshold: 0.05 }).observe(canvasHost);
  function loop() {
    cancelAnimationFrame(raf);
    if (!visible) return;
    const now = performance.now(), dt = Math.min(0.05, (now - t0) / 1000); t0 = now;
    idle += dt;
    if (!reduce && !dragging && idle > 2.5) tTheta = 0.5 + Math.sin(now / 4200) * 0.35;
    theta += (tTheta - theta) * 0.07; phi += (tPhi - phi) * 0.07;
    camera.position.set(
      target.x + radius * Math.sin(phi) * Math.sin(theta),
      target.y + radius * Math.cos(phi),
      target.z + radius * Math.sin(phi) * Math.cos(theta)
    );
    camera.lookAt(target);
    const k = 1 - Math.pow(0.0005, dt); // ease finishes
    mats.cab.color.lerp(goal.cab, k); mats.isl.color.lerp(goal.isl, k);
    mats.hw.color.lerp(goal.hw, k); mats.top.color.lerp(goal.top, k);
    renderer.render(scene, camera);
    raf = requestAnimationFrame(loop);
  }
  loop();

  function apply() {
    goal.cab.set(FINISHES.cabinets[state.cabinets].hex);
    goal.isl.set(state.island === "match" ? FINISHES.cabinets[state.cabinets].hex : FINISHES.island[state.island].hex);
    const hw = FINISHES.hardware[state.hardware];
    goal.hw.set(hw.hex); mats.hw.metalness = hw.metal; mats.hw.roughness = hw.rough;
    goal.top.set(FINISHES.counter[state.counter].hex);
    if (reduce) { mats.cab.color.copy(goal.cab); mats.isl.color.copy(goal.isl); mats.hw.color.copy(goal.hw); mats.top.color.copy(goal.top); }
    onChange && onChange({ ...state }, summary());
  }
  const summary = () =>
    `Cabinets: ${FINISHES.cabinets[state.cabinets].label}. Island: ${FINISHES.island[state.island].label}. ` +
    `Hardware: ${FINISHES.hardware[state.hardware].label}. Countertop: ${FINISHES.counter[state.counter].label}.`;

  return {
    FINISHES, state,
    set(group, key) { state[group] = key; apply(); },
    summary,
    init: apply,
  };
}
