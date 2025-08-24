
'use client';
import React, { useState } from "react";

export default function LoginPage() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [status, setStatus] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("Logging in...");
    setTimeout(() => setStatus("✅ Logged in!"), 1000);
  };

  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "#f5faff" }}>
      <form onSubmit={handleSubmit} style={{ background: "#fff", padding: 32, borderRadius: 16, boxShadow: "0 4px 24px rgba(37,99,235,0.08)", minWidth: 340, maxWidth: 400 }}>
        <h2 style={{ fontWeight: 700, fontSize: 28, marginBottom: 18, color: "#2563eb" }}>Login</h2>
        <label style={{ display: "block", marginBottom: 10 }}>
          Email
          <input name="email" type="email" value={form.email} onChange={handleChange} required style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #c7d2fe", marginTop: 4 }} />
        </label>
        <label style={{ display: "block", marginBottom: 18 }}>
          Password
          <input name="password" type="password" value={form.password} onChange={handleChange} required style={{ width: "100%", padding: 10, borderRadius: 8, border: "1px solid #c7d2fe", marginTop: 4 }} />
        </label>
        <button type="submit" style={{ width: "100%", background: "#2563eb", color: "#fff", fontWeight: 700, border: "none", borderRadius: 8, padding: 12, fontSize: 16, marginBottom: 10 }}>Login</button>
        <div style={{ color: "#2563eb", fontWeight: 500, minHeight: 24 }}>{status}</div>
        <div style={{ margin: "18px 0 8px 0", textAlign: "center", color: "#888" }}>or login with</div>
        <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
          <button type="button" style={{ background: "#fff", border: "1px solid #c7d2fe", borderRadius: 8, padding: "10px 18px", fontWeight: 600, color: "#2563eb", cursor: "pointer" }}>Google</button>
          <button type="button" style={{ background: "#fff", border: "1px solid #c7d2fe", borderRadius: 8, padding: "10px 18px", fontWeight: 600, color: "#2563eb", cursor: "pointer" }}>GitHub</button>
          <button type="button" style={{ background: "#fff", border: "1px solid #c7d2fe", borderRadius: 8, padding: "10px 18px", fontWeight: 600, color: "#2563eb", cursor: "pointer" }}>LinkedIn</button>
        </div>
      </form>
    </main>
  );
}
