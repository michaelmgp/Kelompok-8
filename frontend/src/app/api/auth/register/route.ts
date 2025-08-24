import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { fullName, username, email, password, confirmPassword } = body || {};

    if (!email || !password) {
      return NextResponse.json({ ok: false, code: "VALIDATION", message: "Email and password required" }, { status: 400 });
    }
    if (password !== confirmPassword) {
      return NextResponse.json({ ok: false, code: "VALIDATION", message: "Passwords do not match" }, { status: 400 });
    }
    const token = Math.random().toString(36).slice(2) + Math.random().toString(36).slice(2);
    return NextResponse.json({ ok: true, verificationToken: token });
  } catch (e) {
    return NextResponse.json({ ok: false, code: "BAD_REQUEST", message: "Invalid request" }, { status: 400 });
  }
}
