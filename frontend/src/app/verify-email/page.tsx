import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Verify Email | CareerVerse",
};

export default function VerifyEmailPage({ searchParams }: { searchParams: { email?: string } }) {
  const email = searchParams?.email || "";
  const obf = email.replace(/(.{2}).+(@.+)/, (_, a, b) => a + "***" + b);
  return (
    <main className="min-h-[calc(100dvh-0px)] grid place-items-center bg-[radial-gradient(80%_80%_at_10%_10%,#0ea5e966_0%,transparent_60%),radial-gradient(70%_70%_at_90%_20%,#a855f766_0%,transparent_60%),linear-gradient(180deg,#0b1020_0%,#0b0f1a_100%)]">
      <div className="w-full max-w-lg mx-auto p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl text-center">
        <h1 className="text-2xl font-semibold text-white">Check your inbox</h1>
        <p className="mt-2 text-slate-200">We sent a verification link to <b>{obf}</b>.</p>
        <button className="mt-6 inline-flex items-center justify-center rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white px-5 py-2.5 font-medium shadow-lg shadow-emerald-500/20">
          Resend Email
        </button>
      </div>
    </main>
  );
}
