"use client";
import Link from "next/link";
import { BookText, User, ShieldCheck, Star, Briefcase, Users, MessageCircle } from "lucide-react";

const sidebarLinks = [
	{ href: "/docs/identity", label: "Identity CRUD", icon: <User className="w-5 h-5 mr-2" /> },
	{ href: "/docs/job", label: "Job CRUD", icon: <Briefcase className="w-5 h-5 mr-2" /> },
	{ href: "/docs/agent", label: "Agent CRUD", icon: <Users className="w-5 h-5 mr-2" /> },
	{ href: "/docs/chat", label: "Chat CRUD", icon: <MessageCircle className="w-5 h-5 mr-2" /> },
];

export default function DocsPage() {
	return (
		<main className="min-h-screen bg-gradient-to-br from-blue-950 via-indigo-950 to-gray-900 text-white flex items-center justify-center">
			<div className="max-w-5xl w-full mx-auto py-12 px-4 flex gap-8">
				<aside className="w-64 bg-white/10 rounded-xl shadow p-6 flex flex-col gap-2 h-fit">
					<div className="flex items-center gap-2 mb-4">
						<BookText className="w-6 h-6 text-blue-300" />
						<span className="font-bold text-lg text-blue-100">Docs CRUD ICP</span>
					</div>
					<Link
						href="/"
						className="flex items-center gap-2 px-3 py-2 rounded bg-blue-900/30 hover:bg-blue-900/50 text-blue-100 font-semibold mb-2 transition"
					>
						← Kembali ke Dashboard
					</Link>
					{sidebarLinks.map((link) => (
						<Link
							key={link.href}
							href={link.href}
							className="flex items-center gap-2 px-3 py-2 rounded hover:bg-blue-900/30 transition text-blue-100"
						>
							{link.icon}
							{link.label}
						</Link>
					))}
				</aside>
				<div className="flex-1 bg-white/5 rounded-xl shadow p-8 text-blue-50 text-sm space-y-8">
					<div className="mb-8 text-center">
						<h1 className="text-3xl font-extrabold mb-2 text-blue-200 tracking-tight">
							Dokumentasi CRUD ICP Canister
						</h1>
						<p className="mb-6 text-base text-blue-100">
							Pilih menu di sidebar untuk melihat cara CRUD masing-masing canister (Identity, Job, Agent, Chat)
						</p>
					</div>
				</div>
			</div>
		</main>
	);
}

// Sidebar sudah otomatis menampilkan link ke semua canister docs
// Konten utama docs ada di masing-masing subfolder: identity, job, agent, chat
