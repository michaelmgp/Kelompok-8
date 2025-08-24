"use client";
import { useState } from "react";

export default function TagInput({ value, onChange, placeholder }: { value: string[]; onChange: (v: string[]) => void; placeholder?: string }) {
  const [input, setInput] = useState("");

  function add(tag: string) {
    const t = tag.trim();
    if (!t) return;
    if (value.includes(t)) return;
    onChange([...value, t].slice(0, 15));
    setInput("");
  }

  return (
    <div className="rounded-xl border border-slate-300/60 dark:border-white/15 bg-white/70 dark:bg-white/5 px-2 py-2">
      <div className="flex flex-wrap gap-2">
        {value.map((t, idx) => (
          <span key={idx} className="inline-flex items-center gap-1 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-300 px-2 py-1 text-xs">
            {t}
            <button type="button" className="ml-1" onClick={() => onChange(value.filter((_, i) => i !== idx))}>×</button>
          </span>
        ))}
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") { e.preventDefault(); add(input); }
            if (e.key === "Backspace" && input === "" && value.length) {
              onChange(value.slice(0, -1));
            }
          }}
          placeholder={placeholder}
          className="flex-1 min-w-[8ch] bg-transparent outline-none text-sm px-2 py-1"
        />
      </div>
    </div>
  );
}
