import type { Metadata } from "next";
// Removed Geist font imports, as we are using Helvetica Neue via globals.css
import "./globals.css";

export const metadata: Metadata = {
  title: "Mailchimp Trends Engine",
  description: "Discover the latest marketing trends.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* The font-sans class from Tailwind will apply Helvetica Neue via globals.css */}
      {/* The antialiased class improves font rendering. */}
      <body className="antialiased">{children}</body>
    </html>
  );
}
