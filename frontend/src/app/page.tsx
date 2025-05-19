"use client";

import { useEffect, useState } from "react";

interface HealthResponse {
  status: string;
  version: string;
}

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string | null>(null);
  const [backendVersion, setBackendVersion] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBackendStatus = async () => {
      // The NEXT_PUBLIC_API_URL is set in the Kubernetes deployment
      // It should point to the backend service, e.g., http://mailchimp-trends-backend-svc:8000
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        setError("Backend API URL is not configured.");
        return;
      }

      try {
        // The /health endpoint is typically at the root of the API service
        const response = await fetch(`${apiUrl}/health`);
        if (!response.ok) {
          throw new Error(
            `Failed to fetch status: ${response.status} ${response.statusText}`
          );
        }
        const data = (await response.json()) as HealthResponse;
        setBackendStatus(data.status);
        setBackendVersion(data.version);
        setError(null);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred while fetching backend status.");
        }
        setBackendStatus(null);
        setBackendVersion(null);
      }
    };

    fetchBackendStatus();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold">
          Mailchimp Trends Engine - Frontend
        </h1>
        <p className="mt-4 text-lg">
          The frontend application is running.
        </p>
        <div className="mt-8 p-6 border rounded-lg shadow-md bg-gray-50">
          <h2 className="text-2xl font-semibold mb-3">Backend Status:</h2>
          {error && (
            <p className="text-red-500">
              Error connecting to backend: {error}
            </p>
          )}
          {backendStatus && (
            <p className="text-green-600">
              Status: <span className="font-semibold">{backendStatus}</span>
            </p>
          )}
          {backendVersion && (
            <p className="text-blue-600">
              Version: <span className="font-semibold">{backendVersion}</span>
            </p>
          )}
          {!error && !backendStatus && (
            <p className="text-gray-500">Loading backend status...</p>
          )}
        </div>
      </div>
    </main>
  );
}
