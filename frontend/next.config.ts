import type { NextConfig } from "next";
import fs from "node:fs";
import path from "node:path";

const packageJsonPath = path.resolve("./package.json");
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));

const nextConfig: NextConfig = {
  output: "standalone",
  /* other config options here */
  env: {
    NEXT_PUBLIC_APP_VERSION: packageJson.version,
  },
};

export default nextConfig;
