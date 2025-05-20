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

  // Add tests for non-test environment paths to improve coverage using forceNonTestEnv prop
  describe('Non-test environment paths (using forceNonTestEnv)', () => {
    beforeEach(() => {
      // Clear mock usage history before each test
      (global.fetch as jest.Mock).mockClear();
    });

    test('displays backend status and version on successful fetch in non-test environment', async () => {
      const mockStatus = 'healthy-prod';
      const mockVersion = '0.1.0-prod';
      // Promise for the response.json() call
      const jsonPromise = Promise.resolve({ status: mockStatus, version: mockVersion });
      // Promise for the fetch() call
      const fetchPromise = Promise.resolve({
        ok: true,
        json: () => jsonPromise,
      } as Response);

      (global.fetch as jest.Mock).mockImplementationOnce(() => fetchPromise);

      // Use the forceNonTestEnv prop instead of modifying NODE_ENV
      render(<Home forceNonTestEnv={true} />);

      // Wait for all promises to resolve and state updates to occur
      await waitFor(() => {
        // Use more specific selectors to target the right elements
        const statusElement = screen.getByText((content, element) =>
          element?.tagName.toLowerCase() === 'p' &&
          element?.className.includes('text-green-600') &&
          content.includes('Status:')
        );
        expect(statusElement.textContent).toContain(mockStatus);

        const versionElement = screen.getByText((content, element) =>
          element?.tagName.toLowerCase() === 'p' &&
          element?.className.includes('text-blue-600') &&
          content.includes('Version:')
        );
        expect(versionElement.textContent).toContain(mockVersion);

        expect(screen.queryByText(/Loading backend status.../i)).not.toBeInTheDocument();
      });

      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(global.fetch).toHaveBeenCalledWith(`${mockApiUrl}/health`);
    });

    test('displays error message on failed fetch in non-test environment', async () => {
      // Mock a network error
      (global.fetch as jest.Mock).mockImplementationOnce(() =>
        Promise.reject(new Error('Network error in prod environment'))
      );

      // Use the forceNonTestEnv prop instead of modifying NODE_ENV
      render(<Home forceNonTestEnv={true} />);

      await waitFor(() => {
        expect(screen.getByText(/Error connecting to backend: Network error in prod environment/i)).toBeInTheDocument();
        // Check that status and version elements are not present - using more specific text patterns
        expect(screen.queryByText('Status:')).not.toBeInTheDocument();
        expect(screen.queryByText('Version:')).not.toBeInTheDocument();
      });
    });

    test('displays unknown error message on non-Error rejection in non-test environment', async () => {
      // Mock a rejection with a non-Error value
      (global.fetch as jest.Mock).mockImplementationOnce(() =>
        Promise.reject('A string error in prod environment')
      );

      // Use the forceNonTestEnv prop instead of modifying NODE_ENV
      render(<Home forceNonTestEnv={true} />);

      await waitFor(() => {
        expect(screen.getByText(/Error connecting to backend: An unknown error occurred while fetching backend status./i)).toBeInTheDocument();
        // Check that status and version elements are not present - using more specific text patterns
        expect(screen.queryByText('Status:')).not.toBeInTheDocument();
        expect(screen.queryByText('Version:')).not.toBeInTheDocument();
      });
    });
  });
});
