// frontend/src/app/__tests__/page.test.tsx
import { render, screen, waitFor, act } from '@testing-library/react';
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
    const mockStatus = 'healthy';
    const mockVersion = '0.1.0-mock';
    // Promise for the response.json() call
    const jsonPromise = Promise.resolve({ status: mockStatus, version: mockVersion });
    // Promise for the fetch() call
    const fetchPromise = Promise.resolve({
      ok: true,
      json: () => jsonPromise, // The json() method returns our jsonPromise
    } as Response);

    (global.fetch as jest.Mock).mockImplementationOnce(() => fetchPromise);

    await act(async () => {
      render(<Home />);
      // Wait for the main fetch promise to resolve
      await fetchPromise;
      // Wait for the .json() promise to resolve
      await jsonPromise;
      // All synchronous state updates after these promises should now be flushed by act
    });

    await waitFor(() => {
      expect(screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).toHaveTextContent('Status: healthy');
      expect(screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).toHaveTextContent('Version: 0.1.0-mock');
      expect(screen.queryByText(/Loading backend status.../i)).not.toBeInTheDocument();
    });

    // Assertions for fetch calls can remain outside if they don't depend on further state changes.
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
    let fetchPromise: Promise<Response>;
    (global.fetch as jest.Mock).mockImplementationOnce(() => {
      fetchPromise = Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: () => Promise.resolve({}), // Should not be called if not ok
      } as Response);
      return fetchPromise;
    });

    await act(async () => {
      render(<Home />);
      await fetchPromise; // Ensure fetch promise resolves
    });

    await waitFor(() => {
      expect(screen.getByText(/Error connecting to backend: Failed to fetch status: 500 Internal Server Error/i)).toBeInTheDocument();
      expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).not.toBeInTheDocument();
      expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).not.toBeInTheDocument();
    });
  });

  test('displays generic error message on network error', async () => {
    let fetchPromise: Promise<unknown>;
    (global.fetch as jest.Mock).mockImplementationOnce(() => {
      fetchPromise = Promise.reject(new Error('Network failed'));
      return fetchPromise;
    });

    await act(async () => {
      render(<Home />);
      try {
        await fetchPromise; // Ensure fetch promise rejects
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (_e) {
        // Expected rejection, do nothing
      }
    });

    await waitFor(() => {
      expect(screen.getByText(/Error connecting to backend: Network failed/i)).toBeInTheDocument();
      expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).not.toBeInTheDocument();
      expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).not.toBeInTheDocument();
    });
  });

  test('displays unknown error message on non-Error rejection', async () => {
    let fetchPromise: Promise<unknown>;
    (global.fetch as jest.Mock).mockImplementationOnce(() => {
      fetchPromise = Promise.reject('A string error, not an Error object');
      return fetchPromise;
    });

    await act(async () => {
      render(<Home />);
      try {
        await fetchPromise; // Ensure fetch promise rejects
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (_e) {
        // Expected rejection, do nothing
      }
    });

    await waitFor(() => {
      expect(screen.getByText(/Error connecting to backend: An unknown error occurred while fetching backend status./i)).toBeInTheDocument();
      expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).not.toBeInTheDocument();
      expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).not.toBeInTheDocument();
    });
  });
});
