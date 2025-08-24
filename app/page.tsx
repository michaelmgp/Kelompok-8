


import React from "react";
import Link from "next/link";

export default function Home() {
  return (
    <main style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "linear-gradient(180deg, #f5faff 0%, #e6eeff 100%)"
    }}>
      <div style={{ display: "flex", flexDirection: "column", gap: 24, alignItems: "center" }}>
        <Link href="/register" style={{
          background: "#2563eb",
          color: "#fff",
          fontWeight: 700,
          fontSize: "1.2rem",
          borderRadius: 10,
          padding: "16px 48px",
          textDecoration: "none",
          boxShadow: "0 2px 8px rgba(37,99,235,0.08)",
          border: "none",
          marginBottom: 8
        }}>Register</Link>
        <Link href="/login" style={{
          background: "#fff",
          color: "#2563eb",
          fontWeight: 700,
          fontSize: "1.2rem",
          borderRadius: 10,
          padding: "16px 48px",
          textDecoration: "none",
          border: "2px solid #2563eb"
        }}>Login</Link>
      </div>
    </main>
  );
}
