"use client";
import { useEffect, useMemo, useState } from "react";

function score(password: string) {
  let s = 0;
  if (password.length >= 8) s++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) s++;
  if (/[0-9]/.test(password)) s++;
  if (/[^A-Za-z0-9]/.test(password)) s++;
  return s; // 0..4
}

export default function PasswordStrength({ passwordRefId }: { passwordRefId: string }) {
  const [value, setValue] = useState("");
  useEffect(() => {
    const el = document.getElementById(passwordRefId) as HTMLInputElement | null;
    if (!el) return;
    const on = () => setValue(el.value);
    el.addEventListener("input", on);
    on();
    return () => el.removeEventListener("input", on);
  }, [passwordRefId]);

  const s = useMemo(() => score(value), [value]);
  const labels = ["Very weak","Weak","Fair","Good","Strong"];
  return (
    <div className="mt-1">
      <div className="h-2 w-full bg-slate-200/60 dark:bg-white/10 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all"
          style={{ width: `${(s/4)*100}%`, background: s<2 ? "#f43f5e" : s<3 ? "#f59e0b" : s<4 ? "#22c55e" : "#10b981" }} />
      </div>
      <p className="mt-1 text-xs text-slate-500">{labels[s]}</p>
    </div>
  );
}
