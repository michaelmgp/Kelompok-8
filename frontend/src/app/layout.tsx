import type { Metadata } from "next";
import "./globals.css";
import FloatingAIAssistant from "@/components/ai/FloatingAIAssistant";

export const metadata: Metadata = {
  title: "CareerVerse - Decentralized Autonomous Job Marketplace",
  description: "A decentralized marketplace where AI agents handle matching & negotiation, while ICP secures employer/employee data for fast, trusted hiring.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
      </head>
      <body className="font-inter bg-career-gray min-h-screen">
        {children}
        <FloatingAIAssistant />
      </body>
    </html>
  );
}
