"use client";
import Link from "next/link";
import { User, BookText, Briefcase, Users, MessageCircle } from "lucide-react";

const sidebarLinks = [
	{ href: "/docs/identity", label: "Identity CRUD", icon: <User className="w-5 h-5 mr-2" /> },
	{ href: "/docs/job", label: "Job CRUD", icon: <Briefcase className="w-5 h-5 mr-2" /> },
	{ href: "/docs/agent", label: "Agent CRUD", icon: <Users className="w-5 h-5 mr-2" /> },
	{ href: "/docs/chat", label: "Chat CRUD", icon: <MessageCircle className="w-5 h-5 mr-2" /> },
];

export default function IdentityDocs() {
	return (
		<main className="min-h-screen bg-gradient-to-br from-blue-950 via-indigo-950 to-gray-900 text-white flex items-center justify-center">
			<div className="max-w-5xl w-full mx-auto py-12 px-4 flex gap-8">
				<aside className="w-64 bg-white/10 rounded-xl shadow p-6 flex flex-col gap-2 h-fit sticky top-12 self-start">
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
							className={`flex items-center gap-2 px-3 py-2 rounded hover:bg-blue-900/30 transition text-blue-100 ${
								link.href === "/docs/identity" ? "bg-blue-900/40 font-bold" : ""
							}`}
						>
							{link.icon}
							{link.label}
						</Link>
					))}
				</aside>
				<div className="flex-1 bg-white/5 rounded-xl shadow p-8 text-blue-50 text-base space-y-8">
					<div className="flex items-center gap-2 mb-6">
						<User className="w-8 h-8 text-blue-300" />
						<h2 className="text-3xl font-bold text-blue-200">Identity CRUD</h2>
					</div>
					<section>
						<h3 className="font-bold text-blue-100 mb-2 text-xl">Fitur CRUD</h3>
						<ul className="list-disc ml-6 text-blue-50 space-y-1">
							<li>
								Buat/Update Profile:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">updateProfile</code>
							</li>
							<li>
								Get Profile:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">getUserProfile</code>
							</li>
							<li>
								Get Semua Profile:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">getAllProfiles</code>
							</li>
							<li>
								Verifikasi:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">submitVerification</code>,{" "}
								<code className="bg-black/30 px-2 py-1 rounded">processVerification</code>
							</li>
							<li>
								Reputasi:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">addReputation</code>,{" "}
								<code className="bg-black/30 px-2 py-1 rounded">getUserReputations</code>
							</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-blue-100 mb-2 text-xl">Contoh Next.js ke Motoko</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`const actor = getIdentityActor();
await actor.updateProfile(name, email, bio, skills, portfolioUrl, location, experienceLevel);
const profile = await actor.getUserProfile(principal);
const allProfiles = await actor.getAllProfiles();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-blue-100 mb-2 text-xl">Contoh React.js ke Motoko</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`import { actor } from './icpClient';
const profile = await actor.getUserProfile(principal);`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-blue-100 mb-2 text-xl">Tips</h3>
						<ul className="list-disc ml-6 text-blue-50 space-y-1">
							<li>Gunakan principal ICP yang valid</li>
							<li>Perhatikan tipe data sesuai candid</li>
							<li>Cek log di frontend untuk error detail</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-blue-100 mb-2 text-xl">Struktur Database Canister</h3>
						<div className="bg-black/20 p-4 rounded text-xs mb-4">
							<b>Profile:</b>
							<br />
							<pre className="whitespace-pre-wrap">{`type Profile = {
  principal: Text;
  name: Text;
  email: Text;
  bio: Text;
  skills: [Text];
  portfolioUrl: Text;
  location: Text;
  experienceLevel: Text;
};

Verifikasi:
  type Verification = {
    principal: Text;
    status: Text; // e.g. "pending", "approved", "rejected"
    documents: [Text];
  };

Reputasi:
  type Reputation = {
    principal: Text;
    score: Nat;
    feedback: Text;
  };`}</pre>
						</div>
						<ul className="list-disc ml-6 text-blue-50 space-y-1">
							<li>
								<b>Profile</b>: Data utama user, bisa diupdate dan diambil.
							</li>
							<li>
								<b>Verification</b>: Status dan dokumen verifikasi user.
							</li>
							<li>
								<b>Reputation</b>: Skor dan feedback reputasi user.
							</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-blue-100 mb-2 text-xl">Cara Penggunaan Fitur</h3>
						<ul className="list-decimal ml-6 text-blue-50 space-y-1">
							<li>
								Buat/Update Profile: Panggil <code>updateProfile</code> dengan data lengkap.
							</li>
							<li>
								Ambil Profile: Panggil <code>getUserProfile</code> dengan principal user.
							</li>
							<li>
								List Semua Profile: Panggil <code>getAllProfiles</code>.
							</li>
							<li>
								Verifikasi: Submit dokumen dengan <code>submitVerification</code>, proses dengan{" "}
								<code>processVerification</code>.
							</li>
							<li>
								Reputasi: Tambah reputasi dengan <code>addReputation</code>, ambil dengan{" "}
								<code>getUserReputations</code>.
							</li>
						</ul>
					</section>
				</div>
			</div>
		</main>
	);
}
