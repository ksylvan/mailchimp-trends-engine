// frontend/jest.setup.ts

// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

let actError: Error | null = null;
const originalConsoleError = console.error;

beforeAll(() => {
  jest.spyOn(console, 'error').mockImplementation((message, ...args) => {
    if (
      typeof message === 'string' &&
      message.includes('An update to %s inside a test was not wrapped in act')
    ) {
      actError = new Error(message); // Store the error
    }
    // Still call the original console.error or a minimal version to see other errors
    // For act warnings, we might not want to pollute the console if we're throwing later.
    // However, for other console.errors, we do want to see them.
    if (!(typeof message === 'string' && message.includes('An update to %s inside a test was not wrapped in act'))) {
      originalConsoleError(message, ...args);
    }
  });
});

beforeEach(() => {
  actError = null; // Reset before each test
});

afterEach(() => {
  if (actError) {
    const errorToThrow = actError;
    actError = null; // Clear it before throwing for the next test
    throw errorToThrow; // Fail the test if an actError was recorded
  }
});

afterAll(() => {
  (console.error as jest.Mock).mockRestore();
});
