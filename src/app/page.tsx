"use client";
import Link from "next/link";
import { User, ShieldCheck, Star, Briefcase, Users, BookText } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-950 via-indigo-950 to-gray-900 text-white flex items-center justify-center">
      <div className="max-w-3xl w-full mx-auto py-12 px-4">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-extrabold mb-2 text-blue-200 tracking-tight">
            Motoko ICP Dashboard
          </h1>
          <p className="mb-6 text-base text-blue-100">
            Test & Manage all CRUD features for ICP canisters in one place
          </p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
          <Link
            href="/profile"
            className="flex items-center gap-4 bg-white/5 hover:bg-blue-900/30 transition rounded-xl shadow p-5"
          >
            <User className="w-8 h-8 text-blue-400" />
            <span className="font-semibold text-lg">Profile CRUD</span>
          </Link>
          <Link
            href="/verification"
            className="flex items-center gap-4 bg-white/5 hover:bg-purple-900/30 transition rounded-xl shadow p-5"
          >
            <ShieldCheck className="w-8 h-8 text-purple-400" />
            <span className="font-semibold text-lg">Verification CRUD</span>
          </Link>
          <Link
            href="/reputation"
            className="flex items-center gap-4 bg-white/5 hover:bg-green-900/30 transition rounded-xl shadow p-5"
          >
            <Star className="w-8 h-8 text-green-400" />
            <span className="font-semibold text-lg">Reputation CRUD</span>
          </Link>
          <Link
            href="/jobs"
            className="flex items-center gap-4 bg-white/5 hover:bg-yellow-900/30 transition rounded-xl shadow p-5"
          >
            <Briefcase className="w-8 h-8 text-yellow-400" />
            <span className="font-semibold text-lg">Jobs CRUD</span>
          </Link>
          <Link
            href="/agent"
            className="flex items-center gap-4 bg-white/5 hover:bg-gray-900/30 transition rounded-xl shadow p-5"
          >
            <Users className="w-8 h-8 text-gray-400" />
            <span className="font-semibold text-lg">Agent CRUD</span>
          </Link>
          <Link
            href="/docs"
            className="flex items-center gap-4 bg-white/5 hover:bg-blue-900/30 transition rounded-xl shadow p-5"
          >
            <BookText className="w-8 h-8 text-blue-300" />
            <span className="font-semibold text-lg">Dokumentasi</span>
          </Link>
        </div>
        <div className="mt-10 text-center text-blue-100 text-xs">
          <b>ICP Canister integration demo.</b> Edit endpoints in{" "}
          <code className="bg-black/30 px-2 py-1 rounded">/api/icp/</code> for
          real canister calls.
          <br />
          UI styled for easy testing and dashboard experience.
        </div>
      </div>
    </main>
  );
}
