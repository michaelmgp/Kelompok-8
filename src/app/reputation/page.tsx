"use client";
import { useState } from "react";

export default function ReputationPage() {
  const [reputations, setReputations] = useState<any[]>([]);
  const [form, setForm] = useState({
    userPrincipal: "",
    jobId: "",
    rating: 5.0,
    review: ""
  });
  const [message, setMessage] = useState("");
  const [logs, setLogs] = useState<string[]>([]);

  function log(msg: string) {
    setLogs(l => [...l, msg]);
  }

  async function addReputation() {
    log("Add Reputation...");
    const res = await fetch(`/api/icp/reputation`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    setMessage(data.message || "Reputation added!");
    log("Reputation added!");
    fetchReputations();
  }

  async function fetchReputations() {
    log("Get User Reputations...");
    // Replace with actual ICP endpoint and principal
    const principal = form.userPrincipal;
    const res = await fetch(`/api/icp/reputation?principal=${principal}`);
    const data = await res.json();
    setReputations(data);
    log(`Fetched reputations for ${principal}`);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-indigo-950 to-gray-900 flex items-center justify-center py-12">
      <div className="max-w-2xl w-full mx-auto p-8 bg-white/10 rounded-2xl shadow-xl backdrop-blur-lg">
        <h1 className="text-4xl font-extrabold mb-8 text-blue-200 text-center tracking-tight drop-shadow">Reputation CRUD</h1>
        <form className="grid grid-cols-2 gap-4 mb-6" onSubmit={e => { e.preventDefault(); addReputation(); }}>
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2" placeholder="User Principal" value={form.userPrincipal} onChange={e => setForm({ ...form, userPrincipal: e.target.value })} />
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 col-span-2" placeholder="Job ID" value={form.jobId} onChange={e => setForm({ ...form, jobId: e.target.value })} />
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" type="number" min="1" max="5" step="0.1" placeholder="Rating" value={form.rating} onChange={e => setForm({ ...form, rating: parseFloat(e.target.value) })} />
          <input className="border border-blue-700/30 bg-white/20 text-blue-100 placeholder-blue-300 p-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Review" value={form.review} onChange={e => setForm({ ...form, review: e.target.value })} />
          <button className="bg-blue-700 hover:bg-blue-800 text-white font-bold rounded py-3 px-6 col-span-2 transition shadow-lg" type="submit">Add Reputation</button>
        </form>
        {message && <div className="mt-2 text-green-400 font-semibold text-center">{message}</div>}
        <div className="flex gap-2 mt-4 justify-center">
          <button className="bg-gray-800 hover:bg-gray-900 text-white rounded py-2 px-5 font-semibold transition shadow" onClick={fetchReputations}>Get User Reputations</button>
        </div>
        {reputations.length > 0 && (
          <div className="mt-8 bg-white/5 p-5 rounded-xl border border-blue-900/30 text-blue-100">
            <h2 className="font-bold mb-2 text-blue-200">Reputations Data</h2>
            <pre className="text-xs overflow-x-auto whitespace-pre-wrap">{JSON.stringify(reputations, null, 2)}</pre>
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
