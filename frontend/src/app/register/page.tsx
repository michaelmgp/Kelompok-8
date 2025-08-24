import type { Metadata } from "next";
import RegisterForm from "@/components/auth/RegisterForm";

export const metadata: Metadata = {
  title: "Register | CareerVerse",
  description: "Create a new CareerVerse account",
};

export default function RegisterPage() {
  return (
    <main className="min-h-[calc(100dvh-0px)] grid place-items-center bg-[radial-gradient(80%_80%_at_10%_10%,#0ea5e966_0%,transparent_60%),radial-gradient(70%_70%_at_90%_20%,#a855f766_0%,transparent_60%),linear-gradient(180deg,#0b1020_0%,#0b0f1a_100%)]">
      <div className="w-full max-w-5xl mx-auto p-4 sm:p-6">
        <div className="grid md:grid-cols-[1.1fr_1fr] gap-0 overflow-hidden rounded-2xl shadow-2xl border border-white/10 bg-white/5 backdrop-blur-xl">
          <div className="relative hidden md:block">
            <RegisterIllustration />
          </div>
          <div className="bg-white/70 dark:bg-white/5 p-6 sm:p-8">
            <RegisterForm />
          </div>
        </div>
      </div>
    </main>
  );
}

function RegisterIllustration() {
  return (
    <div className="h-full w-full grid place-items-center p-8 bg-gradient-to-br from-cyan-500/10 via-fuchsia-500/10 to-emerald-500/10">
      <div className="relative w-full max-w-sm aspect-[4/5]">
        <div className="absolute inset-0 rounded-3xl bg-white/5 border border-white/15 backdrop-blur-xl" />
        <Aura />
        <Badge />
      </div>
    </div>
  );
}

function Aura() {
  return (
    <svg className="absolute inset-0" viewBox="0 0 400 500" aria-hidden>
      <defs>
        <radialGradient id="g1" cx="20%" cy="20%" r="60%">
          <stop offset="0%" stopColor="#22d3ee" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#22d3ee" stopOpacity="0" />
        </radialGradient>
        <radialGradient id="g2" cx="85%" cy="15%" r="60%">
          <stop offset="0%" stopColor="#a78bfa" stopOpacity="0.8" />
          <stop offset="100%" stopColor="#a78bfa" stopOpacity="0" />
        </radialGradient>
      </defs>
      <rect width="400" height="500" fill="url(#g1)" />
      <rect width="400" height="500" fill="url(#g2)" />
      <circle cx="120" cy="380" r="60" className="fill-cyan-400/20" />
      <circle cx="300" cy="420" r="40" className="fill-emerald-400/20" />
    </svg>
  );
}

function Badge() {
  return (
    <div className="absolute bottom-12 left-1/2 -translate-x-1/2 w-56">
      <div className="mx-auto h-32 w-56 rounded-2xl bg-gradient-to-br from-white/30 to-white/0 border border-white/20" />
      <div className="mt-4 h-2 w-28 mx-auto rounded-full bg-black/10 dark:bg-white/10" />
    </div>
  );
}
