// frontend/src/app/__tests__/page.test.tsx
import { render, screen } from '@testing-library/react';
import Home from '../page'; // Adjust the import path based on your actual file structure

// Mock environment variable
const mockApiUrl = 'http://mock-backend:8000';
process.env.NEXT_PUBLIC_API_URL = mockApiUrl;

// Mock global fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ status: 'healthy', version: '0.1.0-mock' }),
  } as Response)
);

describe('Home Page', () => {
  beforeEach(() => {
    // Clear mock usage history before each test
    (global.fetch as jest.Mock).mockClear();
    // Reset to a default successful mock implementation
    (global.fetch as jest.Mock).mockImplementation(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ status: 'healthy', version: '0.1.0-mock' }),
      } as Response)
    );
  });

  test('renders the main heading', () => {
    render(<Home />);
    const headingElement = screen.getByRole('heading', {
      name: /Mailchimp Trends Engine - Frontend/i,
    });
    expect(headingElement).toBeInTheDocument();
  });

  test('renders loading state initially', () => {
    // Temporarily make fetch take longer to simulate loading state
    (global.fetch as jest.Mock).mockImplementationOnce(
      () => new Promise(() => {}) // A promise that never resolves
    );
    render(<Home />);
    expect(screen.getByText(/Loading backend status.../i)).toBeInTheDocument();
  });

  test('displays backend status and version on successful fetch', async () => {
    render(<Home />);

    // Wait for the status and version to be displayed
    // We target the <p> elements and check their textContent
    await screen.findByText(
      (content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'),
      undefined,
      { timeout: 3000 } // Optional: extend timeout if needed
    );

    const statusParagraph = screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'));
    expect(statusParagraph).toHaveTextContent('Status: healthy');

    const versionParagraph = screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'));
    expect(versionParagraph).toHaveTextContent('Version: 0.1.0-mock');

    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith(`${mockApiUrl}/health`);
  });

  test('displays error message when API URL is not configured', () => {
    process.env.NEXT_PUBLIC_API_URL = ''; // Simulate undefined/empty API URL
    render(<Home />);
    expect(
      screen.getByText(/Backend API URL is not configured./i)
    ).toBeInTheDocument();
    process.env.NEXT_PUBLIC_API_URL = mockApiUrl; // Reset for other tests
  });

  test('displays error message on failed fetch', async () => {
    (global.fetch as jest.Mock).mockImplementationOnce(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: () => Promise.resolve({}), // Should not be called if not ok
      } as Response)
    );
    render(<Home />);
    expect(
      await screen.findByText(
        /Error connecting to backend: Failed to fetch status: 500 Internal Server Error/i
      )
    ).toBeInTheDocument();
  });

  test('displays generic error message on network error', async () => {
    (global.fetch as jest.Mock).mockImplementationOnce(() =>
      Promise.reject(new Error('Network failed'))
    );
    render(<Home />);
    expect(
      await screen.findByText(/Error connecting to backend: Network failed/i)
    ).toBeInTheDocument();
  });

  test('displays unknown error message on non-Error rejection', async () => {
    (global.fetch as jest.Mock).mockImplementationOnce(() =>
      Promise.reject('A string error, not an Error object')
    );
    render(<Home />);
    expect(
      await screen.findByText(
        /Error connecting to backend: An unknown error occurred while fetching backend status./i
      )
    ).toBeInTheDocument();
  });
});
