import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  // Global ignores
  {
    ignores: ["jest.config.cjs"],
  },
  // Existing configurations
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

export default eslintConfig;
