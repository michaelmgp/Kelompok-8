"use client";

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthClient } from '@dfinity/auth-client';
import { HttpAgent } from '@dfinity/agent';
import { createIdentityActor, updateProfile, setPasswordOnCanister, flushPendingApplications, createHttpAgent } from '@/lib/icp';

export default function IiCallbackPage() {
  const router = useRouter();

  useEffect(() => {
    (async () => {
      try {
        const authClient = await AuthClient.create();

        // AuthClient.create() processes the redirect/delegation automatically if present.
        const isAuth = await authClient.isAuthenticated();
        console.debug('ii-callback: isAuthenticated=', isAuth);

        if (!isAuth) {
          // Not authenticated — send user to home
          router.replace('/');
          return;
        }

        const identity = authClient.getIdentity();
        const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
        
        // Use utility function to create HttpAgent with proper configuration
        const agent = createHttpAgent({ identity, host });
        
        try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) { console.warn('fetchRootKey failed', e); }

        // Create actor using authenticated identity
        const actor = await createIdentityActor({ agent });

        // Optionally fetch profile to ensure actor works
        try { await actor.getMyProfile(); } catch (err) { console.debug('ii-callback: getMyProfile failed', err); }

        // If there is a pending profile/password saved by the Create Account flow,
        // finalize the canister writes now that we have an authenticated actor.
        try {
          const pendingJson = typeof window !== 'undefined' ? localStorage.getItem('cv:pendingProfile') : null;
          const pendingPw = typeof window !== 'undefined' ? localStorage.getItem('cv:pendingPasswordHash') : null;
          if (pendingJson) {
            const pending = JSON.parse(pendingJson);
            try {
              // ensure skills is an array
              const skills = Array.isArray(pending.skills) ? pending.skills : (typeof pending.skills === 'string' ? pending.skills.split(',').map((s:string)=>s.trim()).filter(Boolean) : []);
              await updateProfile({
                name: pending.name || 'Unnamed',
                email: pending.email || '',
                bio: pending.bio || '',
                skills,
                portfolioUrl: pending.portfolioUrl || '',
                location: pending.location || '',
                experienceLevel: pending.experienceLevel || '',
                role: pending.role || ''
              }, actor);
              console.debug('ii-callback: updateProfile succeeded');
            } catch (upErr) {
              console.error('ii-callback: updateProfile failed', upErr);
            }
          }

          if (pendingPw) {
            try {
              await setPasswordOnCanister(pendingPw, actor);
              console.debug('ii-callback: setPasswordOnCanister succeeded');
            } catch (pwErr) {
              console.error('ii-callback: setPasswordOnCanister failed', pwErr);
            }
          }

          // Clear pending keys and mark local session authenticated
          try {
            localStorage.removeItem('cv:pendingProfile');
            localStorage.removeItem('cv:pendingPasswordHash');
            localStorage.setItem('cv:isAuthenticated', '1');
          } catch (e) { /* ignore */ }
        } catch (e) {
          console.debug('ii-callback: no pending profile to finalize', e);
        }

        // Attempt to flush any pending job applications saved while unauthenticated.
        try {
          const flushResults = await flushPendingApplications({ agent });
          const anyOk = Array.isArray(flushResults) && flushResults.some((r: any) => r && r.ok);
          if (anyOk) {
            console.debug('ii-callback: flushed pending applications', flushResults);
            router.replace('/dashboard/applications');
            return;
          }
        } catch (e) {
          console.debug('ii-callback: flushPendingApplications failed', e);
        }

        // Redirect to dashboard after finalization (default)
        router.replace('/dashboard');
      } catch (err) {
        console.error('ii-callback error', err);
        router.replace('/');
      }
    })();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h2 className="text-lg font-semibold">Processing Internet Identity sign-in…</h2>
        <p className="mt-2 text-sm text-gray-600">If you’re not redirected automatically, please wait or return to the app.</p>
      </div>
    </div>
  );
}
