"use client";
import Link from "next/link";
import { MessageCircle, BookText, User, Briefcase, Users } from "lucide-react";

const sidebarLinks = [
	{
		href: "/docs/identity",
		label: "Identity CRUD",
		icon: <User className="w-5 h-5 mr-2" />,
	},
	{
		href: "/docs/job",
		label: "Job CRUD",
		icon: <Briefcase className="w-5 h-5 mr-2" />,
	},
	{
		href: "/docs/agent",
		label: "Agent CRUD",
		icon: <Users className="w-5 h-5 mr-2" />,
	},
	{
		href: "/docs/chat",
		label: "Chat CRUD",
		icon: <MessageCircle className="w-5 h-5 mr-2" />,
	},
];

export default function ChatDocs() {
	return (
		<div className="min-h-screen bg-gradient-to-br from-fuchsia-950 via-pink-950 to-gray-900 text-white flex items-center justify-center">
			<main className="max-w-5xl w-full mx-auto py-12 px-4 flex gap-8">
				<aside className="w-64 bg-white/10 rounded-xl shadow p-6 flex flex-col gap-2 h-fit sticky top-12 self-start">
					<div className="flex items-center gap-2 mb-4">
						<BookText className="w-6 h-6 text-pink-300" />
						<span className="font-bold text-lg text-pink-100">
							Docs CRUD ICP
						</span>
					</div>
					<Link
						href="/"
						className="flex items-center gap-2 px-3 py-2 rounded bg-pink-900/30 hover:bg-pink-900/50 text-pink-100 font-semibold mb-2 transition"
					>
						← Kembali ke Dashboard
					</Link>
					{sidebarLinks.map((link) => (
						<Link
							key={link.href}
							href={link.href}
							className={`flex items-center gap-2 px-3 py-2 rounded hover:bg-pink-900/30 transition text-pink-100 ${
								link.href === "/docs/chat"
									? "bg-pink-900/40 font-bold"
									: ""
							}`}
						>
							{link.icon}
							{link.label}
						</Link>
					))}
				</aside>
				<div className="flex-1 bg-white/5 rounded-xl shadow p-8 text-pink-50 text-base space-y-8">
					<div className="flex items-center gap-2 mb-6">
						<MessageCircle className="w-8 h-8 text-pink-300" />
						<h2 className="text-3xl font-bold text-pink-200">Chat CRUD</h2>
					</div>
					<section>
						<h3 className="font-bold text-pink-100 mb-2 text-xl">
							Fitur CRUD
						</h3>
						<ul className="list-disc ml-6 text-pink-50 space-y-1">
							<li>
								Kirim Chat:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									sendChat
								</code>
							</li>
							<li>
								Get Chat:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									getChat
								</code>
							</li>
							<li>
								List Semua Chat:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									listChats
								</code>
							</li>
							<li>
								Delete Chat:{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									deleteChat
								</code>
							</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-pink-100 mb-2 text-xl">
							Contoh Next.js ke Motoko
						</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`const actor = getChatActor();
await actor.sendChat(...);
const chats = await actor.listChats();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-pink-100 mb-2 text-xl">
							Contoh React.js ke Motoko
						</h3>
						<pre className="bg-black/30 p-3 rounded text-xs overflow-x-auto">{`import { actor } from './icpClient';
const chats = await actor.listChats();`}</pre>
					</section>
					<section>
						<h3 className="font-bold text-pink-100 mb-2 text-xl">Tips</h3>
						<ul className="list-disc ml-6 text-pink-50 space-y-1">
							<li>Pastikan field chat sesuai schema Motoko</li>
							<li>Cek log error di frontend</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-pink-100 mb-2 text-xl">
							Struktur Database Canister
						</h3>
						<div className="bg-black/20 p-4 rounded text-xs mb-4">
							<b>Chat:</b>
							<br />
							<pre className="whitespace-pre-wrap">{`type Chat = {
  id: Nat;
  sender: Text;
  receiver: Text;
  message: Text;
  timestamp: Text;
};`}</pre>
						</div>
						<ul className="list-disc ml-6 text-pink-50 space-y-1">
							<li>
								<b>Chat</b>: Data utama pesan, bisa dikirim, diambil, dihapus.
							</li>
							<li>
								<b>Sender/Receiver</b>: Principal pengirim dan penerima.
							</li>
							<li>
								<b>Timestamp</b>: Waktu pengiriman pesan.
							</li>
						</ul>
					</section>
					<section>
						<h3 className="font-bold text-pink-100 mb-2 text-xl">
							Cara Penggunaan Fitur
						</h3>
						<ul className="list-decimal ml-6 text-pink-50 space-y-1">
							<li>
								Kirim Chat: Panggil{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									sendChat
								</code>
								{" "}dengan data pesan.
							</li>
							<li>
								Ambil Chat: Panggil{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									getChat
								</code>
								{" "}dengan id chat.
							</li>
							<li>
								List Semua Chat: Panggil{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									listChats
								</code>
								.
							</li>
							<li>
								Delete Chat: Panggil{" "}
								<code className="bg-black/30 px-2 py-1 rounded">
									deleteChat
								</code>
								{" "}dengan id chat.
							</li>
						</ul>
					</section>
				</div>
			</main>
		</div>
	);
}
