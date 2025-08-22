"use client";
import Link from "next/link";
import { Briefcase, BookText, User, Users, MessageCircle } from "lucide-react";

const sidebarLinks = [
	{ href: "/docs/identity", label: "Identity CRUD", icon: <User className="w-5 h-5 mr-2" /> },
	{ href: "/docs/job", label: "Job CRUD", icon: <Briefcase className="w-5 h-5 mr-2" /> },
	{ href: "/docs/agent", label: "Agent CRUD", icon: <Users className="w-5 h-5 mr-2" /> },
	{ href: "/docs/chat", label: "Chat CRUD", icon: <MessageCircle className="w-5 h-5 mr-2" /> },
];

export default function JobDocs() {
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
						<Link key={link.href} href={link.href} className={`flex items-center gap-2 px-3 py-2 rounded hover:bg-blue-900/30 transition text-blue-100 ${link.href === '/docs/job' ? 'bg-blue-900/40 font-bold' : ''}`}>
							{link.icon}
							{link.label}
						</Link>
					))}
				</aside>
				<div className="flex-1 bg-white/5 rounded-xl shadow p-8 text-yellow-50 text-base space-y-8">
					<div className="flex items-center gap-2 mb-6">
						<Briefcase className="w-8 h-8 text-yellow-300" />
						<h2 className="text-3xl font-bold text-yellow-200">Job CRUD</h2>
					</div>
					<section>
						<h3 className="font-bold text-yellow-100 mb-2 text-xl">Fitur CRUD</h3>
						<ul className="list-disc ml-6 text-yellow-50 space-y-1">
							<li>Buat Job: <code className="bg-black/30 px-2 py-1 rounded">addJob</code></li>
							<li>Get Job: <code className="bg-black/30 px-2 py-1 rounded">getJob</code></li>
							<li>List Semua Job: <code className="bg-black/30 px-2 py-1 rounded">listJobs</code></li>
							<li>Update Job: <code className="bg-black/30 px-2 py-1 rounded">updateJob</code></li>
							<li>Delete Job: <code className="bg-black/30 px-2 py-1 rounded">deleteJob</code></li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-yellow-100 mb-2 text-xl">Contoh Next.js ke Motoko</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`const actor = getJobActor();
await actor.addJob(...);
const jobs = await actor.listJobs();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-yellow-100 mb-2 text-xl">Contoh React.js ke Motoko</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`import { actor } from './icpClient';
const jobs = await actor.listJobs();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-yellow-100 mb-2 text-xl">Tips</h3>
						<ul className="list-disc ml-6 text-yellow-50 space-y-1">
							<li>Pastikan field job sesuai schema Motoko</li>
							<li>Cek log error di frontend</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-yellow-100 mb-2 text-xl">Struktur Database Canister</h3>
						<div className="bg-black/20 p-4 rounded text-xs mb-4">
							<b>Job:</b><br />
							<pre className="whitespace-pre-wrap">{`type Job = {
  id: Nat;
  title: Text;
  description: Text;
  skills: [Text];
  budget: Nat;
  deadline: Text;
  client: Text;
  status: Text; // e.g. "open", "in_progress", "done"
};`}</pre>
						</div>
						<ul className="list-disc ml-6 text-yellow-50 space-y-1">
							<li><b>Job</b>: Data utama pekerjaan, bisa dibuat, diupdate, dihapus, dan diambil.</li>
							<li><b>Status</b>: Menandakan progress job.</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-yellow-100 mb-2 text-xl">Cara Penggunaan Fitur</h3>
						<ul className="list-decimal ml-6 text-yellow-50 space-y-1">
							<li>Buat Job: Panggil <code>addJob</code> dengan data lengkap.</li>
							<li>Ambil Job: Panggil <code>getJob</code> dengan id job.</li>
							<li>List Semua Job: Panggil <code>listJobs</code>.</li>
							<li>Update Job: Panggil <code>updateJob</code> dengan id dan data baru.</li>
							<li>Delete Job: Panggil <code>deleteJob</code> dengan id job.</li>
						</ul>
					</section>
				</div>
			</div>
		</main>
	);
}
