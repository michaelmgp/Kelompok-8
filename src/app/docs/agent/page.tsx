"use client";
import Link from "next/link";
import { Users, BookText, User, Briefcase, MessageCircle } from "lucide-react";

const sidebarLinks = [
	{ href: "/docs/identity", label: "Identity CRUD", icon: <User className="w-5 h-5 mr-2" /> },
	{ href: "/docs/job", label: "Job CRUD", icon: <Briefcase className="w-5 h-5 mr-2" /> },
	{ href: "/docs/agent", label: "Agent CRUD", icon: <Users className="w-5 h-5 mr-2" /> },
	{ href: "/docs/chat", label: "Chat CRUD", icon: <MessageCircle className="w-5 h-5 mr-2" /> },
];

export default function AgentDocs() {
	return (
		<main className="min-h-screen bg-gradient-to-br from-blue-950 via-indigo-950 to-gray-900 text-white flex items-center justify-center">
			<div className="max-w-5xl w-full mx-auto py-12 px-4 flex gap-8">
				<aside className="w-64 bg-white/10 rounded-xl shadow p-6 flex flex-col gap-2 h-fit sticky top-12 self-start">
					<div className="flex items-center gap-2 mb-4">
						<BookText className="w-6 h-6 text-blue-300" />
						<span className="font-bold text-lg text-blue-100">Docs CRUD ICP</span>
					</div>
					<Link href="/" className="flex items-center gap-2 px-3 py-2 rounded bg-blue-900/30 hover:bg-blue-900/50 text-blue-100 font-semibold mb-2 transition">
						← Kembali ke Dashboard
					</Link>
					{sidebarLinks.map(link => (
						<Link key={link.href} href={link.href} className={`flex items-center gap-2 px-3 py-2 rounded hover:bg-blue-900/30 transition text-blue-100 ${link.href === '/docs/agent' ? 'bg-blue-900/40 font-bold' : ''}`}>
							{link.icon}
							{link.label}
						</Link>
					))}
				</aside>
				<div className="flex-1 bg-white/5 rounded-xl shadow p-8 text-green-50 text-base space-y-8">
					<div className="flex items-center gap-2 mb-6">
						<Users className="w-8 h-8 text-green-300" />
						<h2 className="text-3xl font-bold text-green-200">Agent CRUD</h2>
					</div>
					<section>
						<h3 className="font-bold text-green-100 mb-2 text-xl">Fitur CRUD</h3>
						<ul className="list-disc ml-6 text-green-50 space-y-1">
							<li>Register Agent: <code className="bg-black/30 px-2 py-1 rounded">addAgent</code></li>
							<li>Get Agent: <code className="bg-black/30 px-2 py-1 rounded">getAgent</code></li>
							<li>List Semua Agent: <code className="bg-black/30 px-2 py-1 rounded">listAgents</code></li>
							<li>Update Agent: <code className="bg-black/30 px-2 py-1 rounded">updateAgent</code></li>
							<li>Delete Agent: <code className="bg-black/30 px-2 py-1 rounded">deleteAgent</code></li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-green-100 mb-2 text-xl">Contoh Next.js ke Motoko</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`const actor = getAgentActor();
await actor.addAgent(...);
const agents = await actor.listAgents();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-green-100 mb-2 text-xl">Contoh React.js ke Motoko</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`import { actor } from './icpClient';
const agents = await actor.listAgents();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-green-100 mb-2 text-xl">Tips</h3>
						<ul className="list-disc ml-6 text-green-50 space-y-1">
							<li>Pastikan field agent sesuai schema Motoko</li>
							<li>Cek log error di frontend</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-green-100 mb-2 text-xl">Struktur Database Canister</h3>
						<div className="bg-black/20 p-4 rounded text-xs mb-4">
							<b>Agent:</b><br />
							<pre className="whitespace-pre-wrap">{`type Agent = {
  id: Nat;
  principal: Text;
  name: Text;
  skills: [Text];
  reputation: Nat;
  status: Text; // e.g. "active", "inactive"
};`}</pre>
						</div>
						<ul className="list-disc ml-6 text-green-50 space-y-1">
							<li><b>Agent</b>: Data utama agent, bisa dibuat, diupdate, dihapus, dan diambil.</li>
							<li><b>Status</b>: Menandakan agent aktif/tidak.</li>
							<li><b>Reputation</b>: Skor reputasi agent.</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-green-100 mb-2 text-xl">Cara Penggunaan Fitur</h3>
						<ul className="list-decimal ml-6 text-green-50 space-y-1">
							<li>Register Agent: Panggil <code>addAgent</code> dengan data lengkap.</li>
							<li>Ambil Agent: Panggil <code>getAgent</code> dengan id agent.</li>
							<li>List Semua Agent: Panggil <code>listAgents</code>.</li>
							<li>Update Agent: Panggil <code>updateAgent</code> dengan id dan data baru.</li>
							<li>Delete Agent: Panggil <code>deleteAgent</code> dengan id agent.</li>
						</ul>
					</section>
				</div>
			</div>
		</main>
	);
}
