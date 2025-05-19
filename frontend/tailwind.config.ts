import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "cavendish-yellow": "#FFD400", // Example, replace with actual from UI spec
        peppercorn: "#333333", // Example, replace with actual from UI spec
        "light-grey-bg": "#F6F6F6", // Example, replace with actual from UI spec
        // Add other Mailchimp brand colors as needed
      },
      fontFamily: {
        sans: ['"Helvetica Neue"', "Arial", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
