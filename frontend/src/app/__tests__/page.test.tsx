// frontend/src/app/__tests__/page.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
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

  test('renders the main heading', async () => {
    render(<Home />);
    const headingElement = screen.getByRole('heading', {
      name: /Mailchimp Trends Engine - Frontend/i,
    });
    expect(headingElement).toBeInTheDocument();

    // Wait for the useEffect to settle
    await waitFor(() => {
      // Check for an element that appears after the fetch
      expect(screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).toBeInTheDocument();
    });
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
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ status: mockStatus, version: mockVersion }),
    } as Response);

    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).toHaveTextContent(`Status: ${mockStatus}`);
      expect(screen.getByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).toHaveTextContent(`Version: ${mockVersion}`);
      expect(screen.queryByText(/Error connecting to backend/i)).not.toBeInTheDocument();
    });

    expect(screen.queryByText(/Loading backend status.../i)).not.toBeInTheDocument();

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
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    } as Response);

    render(<Home />);
    await waitFor(() => {
      expect(screen.getByText(/Error connecting to backend: Failed to fetch status: 500 Internal Server Error/i)).toBeInTheDocument();
    });
    expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).not.toBeInTheDocument();
    expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).not.toBeInTheDocument();
  });

  test('displays generic error message on network error', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network failed'));

    render(<Home />);
    await waitFor(() => {
      expect(screen.getByText(/Error connecting to backend: Network failed/i)).toBeInTheDocument();
    });
    expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).not.toBeInTheDocument();
    expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).not.toBeInTheDocument();
  });

  test('displays unknown error message on non-Error rejection', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce('A string error, not an Error object');

    render(<Home />);
    await waitFor(() => {
      expect(screen.getByText(/Error connecting to backend: An unknown error occurred while fetching backend status./i)).toBeInTheDocument();
    });
    expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Status:'))).not.toBeInTheDocument();
    expect(screen.queryByText((content, element) => element?.tagName.toLowerCase() === 'p' && content.startsWith('Version:'))).not.toBeInTheDocument();
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
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ status: mockStatus, version: mockVersion }),
      } as Response);

      render(<Home />);

      await waitFor(() => {
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
        expect(screen.queryByText(/Error connecting to backend/i)).not.toBeInTheDocument();
      });
      expect(screen.queryByText(/Loading backend status.../i)).not.toBeInTheDocument();

      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(global.fetch).toHaveBeenCalledWith(`${mockApiUrl}/health`);
    });

    test('displays error message on failed fetch in non-test environment', async () => {
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error in prod environment'));

      render(<Home />);
      await waitFor(() => {
        expect(screen.getByText(/Error connecting to backend: Network error in prod environment/i)).toBeInTheDocument();
      });
      // Check that status and version elements are not present - using more specific text patterns
      expect(screen.queryByText('Status:')).not.toBeInTheDocument();
      expect(screen.queryByText('Version:')).not.toBeInTheDocument();
    });

    test('displays unknown error message on non-Error rejection in non-test environment', async () => {
      (global.fetch as jest.Mock).mockRejectedValueOnce('A string error in prod environment');

      render(<Home />);
      await waitFor(() => {
        expect(screen.getByText(/Error connecting to backend: An unknown error occurred while fetching backend status./i)).toBeInTheDocument();
      });
      // Check that status and version elements are not present - using more specific text patterns
      expect(screen.queryByText('Status:')).not.toBeInTheDocument();
      expect(screen.queryByText('Version:')).not.toBeInTheDocument();
    });
  });
});
