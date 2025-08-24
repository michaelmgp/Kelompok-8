"use client";
import { useMemo, useState } from "react";
import Link from "next/link";
import PasswordStrength from "./PasswordStrength";
import TagInput from "./TagInput";
import CaptchaPlaceholder from "./CaptchaPlaceholder";
import { countries } from "@/lib/countries";

type Role = "candidate" | "employer";

export default function RegisterForm() {
  const [show, setShow] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);
  const [skills, setSkills] = useState<string[]>([]);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    setOk(null);

    const fd = new FormData(e.currentTarget);
    const payload = {
      fullName: String(fd.get("fullName") || ""),
      username: String(fd.get("username") || ""),
      email: String(fd.get("email") || ""),
      password: String(fd.get("password") || ""),
      confirmPassword: String(fd.get("confirmPassword") || ""),
      role: String(fd.get("role") || "candidate") as Role,
      skills,
      country: String(fd.get("country") || ""),
      referralCode: String(fd.get("referralCode") || ""),
      consent: fd.get("consent") === "on",
    };

    // Simple client validation
    if (!payload.email || !payload.password) {
      setError("Email dan password wajib diisi.");
      setBusy(false);
      return;
    }
    if (payload.password !== payload.confirmPassword) {
      setError("Konfirmasi password tidak cocok.");
      setBusy(false);
      return;
    }
    if (!payload.consent) {
      setError("Anda harus menyetujui Terms & Privacy.");
      setBusy(false);
      return;
    }

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok || !data.ok) {
        setError(data?.message || "Registrasi gagal");
        setBusy(false);
        return;
      }
      setOk("Registrasi berhasil. Mengalihkan...");
      window.location.href = `/verify-email?email=${encodeURIComponent(payload.email)}`;
    } catch (err) {
      setError("Terjadi kesalahan jaringan.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">Create Account</h1>
      <form onSubmit={onSubmit} className="mt-6 space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <LabeledInput id="fullName" label="Full Name" placeholder="Satoshi Nakamoto" />
          <LabeledInput id="username" label="Username" placeholder="satoshi" />
        </div>

        <LabeledInput id="email" type="email" label="Email" placeholder="you@domain.com" />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <PasswordInput id="password" label="Password" show={show} setShow={setShow} />
          <LabeledInput id="confirmPassword" type={show ? "text" : "password"} label="Confirm Password" placeholder="••••••••" />
        </div>

        <PasswordStrength passwordRefId="password" />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-200">Role</label>
            <div className="flex gap-3">
              <label className="inline-flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                <input type="radio" name="role" value="candidate" defaultChecked className="text-cyan-600" /> Candidate
              </label>
              <label className="inline-flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300">
                <input type="radio" name="role" value="employer" className="text-cyan-600" /> Employer
              </label>
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="country" className="text-sm font-medium text-slate-700 dark:text-slate-200">Country</label>
            <select id="country" name="country" className="w-full rounded-xl border border-slate-300/60 dark:border-white/15 bg-white/70 dark:bg-white/5 px-3 py-2 outline-none focus:border-cyan-400">
              {countries.map(c => <option key={c.code} value={c.code}>{c.label}</option>)}
            </select>
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-slate-700 dark:text-slate-200">Skills</label>
          <TagInput value={skills} onChange={setSkills} placeholder="e.g. Next.js, TailwindCSS, Solidity" />
        </div>

        <LabeledInput id="referralCode" label="Referral Code (optional)" placeholder="Optional" />

        <CaptchaPlaceholder />

        <div className="flex items-start gap-2">
          <input id="consent" name="consent" type="checkbox" className="mt-1 h-4 w-4 rounded border-slate-300 text-cyan-600" />
          <label htmlFor="consent" className="text-sm text-slate-600 dark:text-slate-300">
            I agree to the <a className="text-cyan-500 hover:underline" href="#">Terms</a> and <a className="text-cyan-500 hover:underline" href="#">Privacy</a>.
          </label>
        </div>

        {error && <p className="text-sm text-rose-500 bg-rose-500/10 border border-rose-500/30 px-3 py-2 rounded-lg">{error}</p>}
        {ok && <p className="text-sm text-emerald-600 bg-emerald-500/10 border border-emerald-500/30 px-3 py-2 rounded-lg">{ok}</p>}

        <div className="flex items-center gap-3">
          <button disabled={busy} type="submit" className="inline-flex items-center justify-center rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white px-5 py-2.5 font-medium shadow-lg shadow-emerald-500/20 disabled:opacity-60">
            {busy ? "Creating..." : "Create account"}
          </button>

          <span className="text-sm text-slate-600 dark:text-slate-300">
            Already have an account?{" "}
            <Link href="/login" className="text-emerald-500 hover:underline">Login</Link>
          </span>
        </div>
      </form>
    </div>
  );
}

function LabeledInput(props: { id: string; label: string; type?: string; placeholder?: string }) {
  return (
    <div className="space-y-2">
      <label htmlFor={props.id} className="text-sm font-medium text-slate-700 dark:text-slate-200">{props.label}</label>
      <input id={props.id} name={props.id} type={props.type || "text"} placeholder={props.placeholder}
        className="w-full rounded-xl border border-slate-300/60 dark:border-white/15 bg-white/70 dark:bg-white/5 px-3 py-2 outline-none ring-0 focus:border-cyan-400 focus:bg-white/90 dark:focus:bg-white/10 transition" />
    </div>
  );
}

function PasswordInput(props: { id: string; label: string; show: boolean; setShow: (v: boolean) => void }) {
  return (
    <div className="space-y-2">
      <label htmlFor={props.id} className="text-sm font-medium text-slate-700 dark:text-slate-200">{props.label}</label>
      <div className="relative">
        <input id={props.id} name={props.id} type={props.show ? "text" : "password"} placeholder="••••••••"
          className="w-full rounded-xl border border-slate-300/60 dark:border-white/15 bg-white/70 dark:bg-white/5 px-3 py-2 pr-10 outline-none focus:border-cyan-400 transition" />
        <button type="button" onClick={() => props.setShow(!props.show)} className="absolute inset-y-0 right-2 grid place-items-center px-1 text-slate-500 hover:text-slate-700 dark:text-slate-300">
          {props.show ? "🙈" : "👁️"}
        </button>
      </div>
    </div>
  );
}
