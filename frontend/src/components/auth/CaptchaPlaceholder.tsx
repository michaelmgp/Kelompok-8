"use client";
export default function CaptchaPlaceholder() {
  const enabled = process.env.NEXT_PUBLIC_ENABLE_HCAPTCHA;
  if (!enabled) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300/60 dark:border-white/15 bg-white/30 dark:bg-white/5 p-3 text-xs text-slate-500">
        hCaptcha disabled in development (set NEXT_PUBLIC_ENABLE_HCAPTCHA=1 to enable)
      </div>
    );
  }
  return (
    <div className="rounded-xl border border-slate-300/60 dark:border-white/15 bg-white/30 dark:bg-white/5 p-6 text-sm text-slate-600">
      {/* TODO: mount real hCaptcha here */}
      hCaptcha goes here
    </div>
  );
}
