// frontend/app/layout.tsx  (atau frontend/src/app/layout.tsx)
import React from "react";

export const metadata = {
  title: "CareerVerse",
  description: "Decentralized job agent platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
