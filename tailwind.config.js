/**
 * Home Hero: Tailwind is used for layout only. Spacing and colour resolve to the
 * design tokens in css/tokens.css, and Preflight is off because css/base.css is the reset.
 */
const sp = (n) => `var(--space-${n})`;
module.exports = {
  content: ["./index.html", "./src/**/*.html", "./js/**/*.js", "./*.py", "./services/**/*.html"],
  corePlugins: {
    preflight: false,
    // layout utilities only; nothing that writes --tw-* defaults
    display: true, position: true, inset: true, zIndex: true, flex: true, flexDirection: true, flexWrap: true,
    flexGrow: true, flexShrink: true, alignItems: true, alignSelf: true, justifyContent: true, justifyItems: true,
    gridTemplateColumns: true, gridTemplateRows: true, gridColumn: true, gridColumnStart: true, gridRow: true,
    gap: true, padding: true, margin: true, width: true, height: true, minHeight: true, maxWidth: true,
    overflow: true, order: true, visibility: true, textAlign: true, whiteSpace: true,
    aspectRatio: true, objectFit: true, objectPosition: true,
    // switch the rest off explicitly so no base defaults are emitted
    ringColor: false, ringWidth: false, ringOffsetColor: false, ringOffsetWidth: false, boxShadow: false,
    boxShadowColor: false, dropShadow: false, blur: false, brightness: false, contrast: false, grayscale: false,
    hueRotate: false, invert: false, saturate: false, sepia: false, backdropBlur: false, backdropBrightness: false,
    backdropContrast: false, backdropGrayscale: false, backdropHueRotate: false, backdropInvert: false,
    backdropOpacity: false, backdropSaturate: false, backdropSepia: false, transform: false, translate: false,
    rotate: false, skew: false, scale: false, touchAction: false, scrollSnapType: false, borderColor: false,
    borderOpacity: false, textOpacity: false, backgroundOpacity: false, placeholderColor: false,
    gradientColorStops: false, fontVariantNumeric: false, space: false, divideColor: false, divideWidth: false,
  },
  theme: {
    spacing: {
      0: "0", px: "1px",
      "3xs": sp("3xs"), "2xs": sp("2xs"), xs: sp("xs"), sm: sp("sm"), md: sp("md"), lg: sp("lg"),
      xl: sp("xl"), "2xl": sp("2xl"), "3xl": sp("3xl"), "4xl": sp("4xl"),
      col: "var(--gap-columns)", "sec-s": "var(--section-gap-s)", sec: "var(--section-gap)", "sec-l": "var(--section-gap-l)",
      nav: "var(--nav-h)",
    },
    extend: {},
  },
  plugins: [],
};
