import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

type Props = {
  open: boolean;
  onClose: () => void;
  onSubmit?: (payload: Record<string,string>) => Promise<void> | void;
};

const LoginModal: React.FC<Props> = ({ open, onClose, onSubmit }) => {
  const router = useRouter();
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.currentTarget) as any) as Record<string,string>;
    try {
      setLoading(true);
      setStatus('Logging in...');
      if (onSubmit) {
        await onSubmit(data);
      } else {
        await new Promise(r => setTimeout(r,600));
      }
      setStatus('✅ Logged in as ' + data.email);
      setTimeout(() => {
        router.push('/');
      }, 800);
    } catch (err:any){
      setStatus('❌ ' + (err?.message||'Login failed'));
    } finally {
      setLoading(false);
    }
  };

  if (!open) return null;
  return (
    <div className="auth-overlay" role="dialog" aria-modal="true">
      <div className="auth-modal">
        <button className="close" onClick={onClose} aria-label="Close">×</button>
        <div className="left">
          <img src="/job_seeker.svg" alt="Job seeker illustration" />
          <h3>Welcome back</h3>
          <p>Continue your career journey.</p>
        </div>
        <div className="right">
          <h2>Log in</h2>
          <form onSubmit={handleSubmit}>
            <label>Email
              <input name="email" type="email" placeholder="you@example.com" required />
            </label>
            <label>Password
              <div className="passfield">
                <input name="password" type={showPass?'text':'password'} placeholder="••••••••" required />
                <button type="button" className="eye" onClick={()=>setShowPass(v=>!v)} aria-label="Toggle password">👁</button>
              </div>
            </label>
            <div className="row">
              <label className="checkbox">
                <input type="checkbox" name="remember"/> Remember me
              </label>
              <a href="#" className="muted">Forgot Password?</a>
            </div>
            <div className="actions">
              <button className="primary" type="submit" disabled={loading}>
                {loading ? 'Processing…' : 'Login'}
              </button>
            </div>
          </form>
          <p className="muted small">New user? <a href="/register">Sign up</a></p>
          <div className="divider"><span></span><p>or</p><span></span></div>
          <div className="oauth">
            <button className="oauth-btn">Google</button>
            <button className="oauth-btn">Facebook</button>
            <button className="oauth-btn">GitHub</button>
          </div>
          <pre className="status" aria-live="polite">{status}</pre>
        </div>
      </div>

      <style jsx>{`
        .auth-overlay{position:fixed;inset:0;z-index:50;display:grid;place-items:center;background:rgba(15,23,42,.55);backdrop-filter:blur(2px);}
        .auth-modal{width:min(980px,96vw);display:grid;grid-template-columns:1fr 1fr;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.25);border:1px solid #e5e7eb;position:relative;}
        .close{position:absolute;top:8px;right:12px;border:none;background:transparent;font-size:28px;cursor:pointer;line-height:1;}
        .left{background:#2e2f3a;color:#e5fde7;display:grid;place-items:center;text-align:center;padding:28px;gap:10px;}
        .left img{width:80%;max-width:360px;height:auto;filter:drop-shadow(0 8px 16px rgba(0,0,0,.35));}
        .right{padding:34px 44px;}
        h2{margin:0 0 10px;font-size:28px;}
        label{display:block;font-weight:600;font-size:14px;margin:12px 0 6px;color:#111827;}
        input{width:100%;padding:12px 14px;font-size:16px;border:2px solid #7bc5a4;border-radius:10px;outline:none;}
        .passfield{position:relative;}
        .eye{position:absolute;right:8px;top:50%;transform:translateY(-50%);border:none;background:transparent;cursor:pointer;font-size:18px;}
        .row{display:flex;justify-content:space-between;align-items:center;margin-top:8px;}
        .checkbox{display:inline-flex;align-items:center;gap:6px;font-weight:500;}
        .muted{color:#6b7280;text-decoration:none;}
        .small{font-size:14px;}
        .actions{margin-top:12px;}
        .primary{background:#2ecc71;color:white;border:none;padding:12px 16px;border-radius:10px;font-weight:700;cursor:pointer;}
        .divider{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:12px;margin:16px 0;}
        .divider span{height:1px;background:#e5e7eb;display:block;}
        .oauth{display:flex;gap:12px;flex-wrap:wrap;}
        .oauth-btn{border:1px solid #e5e7eb;background:#fff;border-radius:10px;padding:10px 16px;cursor:pointer;font-weight:700;}
        .status{background:#0b1020;color:#a7f3d0;padding:10px;border-radius:10px;font-size:12px;margin-top:12px;max-height:110px;overflow:auto;}
        @media(max-width:860px){.auth-modal{grid-template-columns:1fr;}.left{display:none;}}
      `}</style>
    </div>
  );
};

export default LoginModal;
