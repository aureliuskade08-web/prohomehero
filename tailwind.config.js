/** Pro Home Hero — design tokens pulled from the supplied palette (espresso → linen). */
module.exports = {
  content: ["./index.html", "./src/**/*.html", "./js/**/*.js"],
  theme: {
    extend: {
      colors: {
        espresso: "#241713",
        bark: "#2E1F19",
        walnut: "#4A2C20",
        rust: "#6B3426",
        camel: "#8A6A45",
        olive: "#4F5A3C",
        moss: "#3F4932",
        taupe: "#A89C8F",
        linen: "#DDD0BE",
        bone: "#F4EEE4",
      },
      fontFamily: {
        display: ['"Instrument Serif"', "Georgia", "serif"],
        sans: ['"Hanken Grotesk"', "system-ui", "sans-serif"],
      },
      letterSpacing: { tightest: "-0.035em" },
    },
  },
  plugins: [],
};
