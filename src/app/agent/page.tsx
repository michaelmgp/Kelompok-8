"use client";
import { useState } from "react";

export default function AgentPage() {
  const [agents, setAgents] = useState<any[]>([]);
  const [form, setForm] = useState({
    nama: "",
    email: "",
    role: ""
  });
  const [message, setMessage] = useState("");
  const [logs, setLogs] = useState<string[]>([]);

  function log(msg: string) {
    setLogs(l => [...l, msg]);
  }

  async function addAgent() {
    log("Add Agent...");
    // Replace with actual ICP endpoint
    const res = await fetch(`/api/icp/agent`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    setMessage(data.message || "Agent added!");
    log("Agent added!");
    fetchAgents();
  }

  async function fetchAgents() {
    log("Get Agents...");
    const res = await fetch(`/api/icp/agent`);
    const data = await res.json();
    setAgents(data);
    log("Agents fetched!");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-indigo-950 to-gray-900 flex items-center justify-center py-12">
      <div className="max-w-2xl w-full mx-auto p-8 bg-white/10 rounded-2xl shadow-xl backdrop-blur-lg">
        <h1 className="text-4xl font-extrabold mb-8 text-blue-200 text-center tracking-tight drop-shadow">Agent CRUD</h1>
        <form className="grid grid-cols-2 gap-4 mb-6" onSubmit={e => { e.preventDefault(); addAgent(); }}>
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2" placeholder="Nama" value={form.nama} onChange={e => setForm({ ...form, nama: e.target.value })} />
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2" placeholder="Email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2" placeholder="Role" value={form.role} onChange={e => setForm({ ...form, role: e.target.value })} />
          <button className="bg-blue-700 hover:bg-blue-800 text-white font-bold rounded py-3 px-6 col-span-2 transition shadow-lg" type="submit">Add Agent</button>
        </form>
        {message && <div className="mt-2 text-green-400 font-semibold text-center">{message}</div>}
        <div className="flex gap-2 mt-4 justify-center">
          <button className="bg-gray-800 hover:bg-gray-900 text-white rounded py-2 px-5 font-semibold transition shadow" onClick={fetchAgents}>Get Agents</button>
        </div>
        {agents.length > 0 && (
          <div className="mt-8 bg-white/5 p-5 rounded-xl border border-blue-900/30 text-blue-100">
            <h2 className="font-bold mb-2 text-blue-200">Agents Data</h2>
            <pre className="text-xs overflow-x-auto whitespace-pre-wrap">{JSON.stringify(agents, null, 2)}</pre>
          </div>
        )}
        {logs.length > 0 && (
          <div className="mt-8">
            <h2 className="font-bold text-yellow-200 mb-2">LOGS</h2>
            <ul className="bg-yellow-900/30 p-3 rounded text-xs text-yellow-100">
              {logs.map((l, i) => <li key={i}>{l}</li>)}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
