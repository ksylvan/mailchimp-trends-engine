/* eslint-disable @typescript-eslint/no-var-requires */
// frontend/jest.config.cjs
const nextJest = require('next/jest');

// Providing the path to your Next.js app to load next.config.js and .env files in your test environment
const createJestConfig = nextJest({
  dir: './',
});

// Add any custom config to be passed to Jest
/** @type {import('jest').Config} */
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    // Handle CSS imports (e.g., if you use CSS Modules)
    '^.+\\.(css|sass|scss)$': 'identity-obj-proxy',
    // Handle module aliases (this will be automatically configured by nextJest)
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  // If you're using TypeScript with a baseUrl to set up directory aliases,
  // you need to configure moduleNameMapper to resolve those aliases.
  // Next.js automatically handles this for its own builds, but Jest needs it explicitly.
  // The `pathsToModuleNameMapper` utility from `ts-jest` can be used if you have complex paths in tsconfig.
  // For a simple `@/*` alias:
  // moduleNameMapper: {
  //   '^@/(.*)$': '<rootDir>/src/$1',
  //   // Handle CSS imports (e.g. if you use CSS Modules)
  //   '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  // },
  // preset: 'ts-jest', // Not needed when using next/jest
};

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(customJestConfig);
