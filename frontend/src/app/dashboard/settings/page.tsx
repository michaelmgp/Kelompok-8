"use client";

import React, { useState } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AuthClient } from '@dfinity/auth-client';
import { HttpAgent } from '@dfinity/agent';
import { hashPassword } from '@/lib/crypto';
import { setPasswordOnCanister, createHttpAgent } from '@/lib/icp';

export default function SettingsPage() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  function validate() {
    setError(null);
    if (!currentPassword) return 'Current password is required';
    if (newPassword.length < 8) return 'New password must be at least 8 characters';
    if (newPassword !== confirmPassword) return 'New password and confirm do not match';
    return null;
  }

  async function resetPassword() {
    const e = validate();
    if (e) {
      setError(e);
      setMessage(null);
      return;
    }
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      // Hash the new password client-side
      const pwRes = await hashPassword(newPassword);
      const hashed = (pwRes && (pwRes.hash || pwRes.encoded)) || '';

      // If the user is authenticated via Internet Identity, write the hashed
      // password to the identity canister. Otherwise, store it locally to be
      // flushed on sign-in.
      const authClient = await AuthClient.create();
      const isAuth = await authClient.isAuthenticated();
      if (isAuth) {
        try {
          const identity = authClient.getIdentity();
          const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
          const agent = createHttpAgent({ identity, host });
          try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) {}
          // setPasswordOnCanister will use the provided actor if available; pass
          // an actor would be more explicit but setPasswordOnCanister accepts
          // an actor argument if the caller supplies one. We'll call it with
          // no actor here because it will create the actor using env config.
          await setPasswordOnCanister(hashed);
          setMessage('Password saved to canister. Use your new password next time you sign in.');
          setCurrentPassword('');
          setNewPassword('');
          setConfirmPassword('');
        } catch (e: any) {
          console.error('Failed to save password to canister', e);
          // fallback: save locally so it can be finalized after II sign-in
          try { localStorage.setItem('cv:pendingPasswordHash', hashed); } catch (er) {}
          setMessage('Saved locally. Complete sign-in to persist to canister.');
        }
      } else {
        // Persist pending password hash to be written after authentication.
        try { localStorage.setItem('cv:pendingPasswordHash', hashed); } catch (e) {}
        setMessage('Password saved locally. Sign in to persist to canister.');
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to reset password');
    } finally {
      setSaving(false);
    }
  }

  async function sendResetEmail() {
    setSaving(true);
    setError(null);
    setMessage(null);
    await new Promise((r) => setTimeout(r, 600));
    setSaving(false);
    setMessage('Password reset email sent (simulated). Check your inbox.');
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <Sidebar />

      <div className="max-w-8xl ml-0 lg:ml-80 px-4 sm:px-6 lg:px-8">
        <div className="py-6">
          <Card className="p-6 border border-gray-200 bg-white max-w-8xl">
            <div className="mb-4">
              <h1 className="text-2xl font-bold">Settings</h1>
              <p className="text-sm text-gray-500">Manage account settings and security.</p>
            </div>

            <section className="mt-4">
              <h2 className="text-lg font-medium">Change password</h2>
              <p className="text-sm text-gray-500 mb-4">Update your password or send a reset email.</p>

              <div className="space-y-3">
                <div>
                  <label className="text-sm text-gray-600">Current password</label>
                  <input
                    type="password"
                    value={currentPassword}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setCurrentPassword(e.target.value)}
                    className="w-full px-3 py-2 border rounded mt-1"
                    data-testid="input-current-password"
                  />
                </div>

                <div>
                  <label className="text-sm text-gray-600">New password</label>
                  <input
                    type="password"
                    value={newPassword}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewPassword(e.target.value)}
                    className="w-full px-3 py-2 border rounded mt-1"
                    data-testid="input-new-password"
                  />
                  <div className="text-xs text-gray-500 mt-1">Minimum 8 characters</div>
                </div>

                <div>
                  <label className="text-sm text-gray-600">Confirm new password</label>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setConfirmPassword(e.target.value)}
                    className="w-full px-3 py-2 border rounded mt-1"
                    data-testid="input-confirm-password"
                  />
                </div>

                {error && <div className="text-sm text-red-600" data-testid="settings-error">{error}</div>}
                {message && <div className="text-sm text-green-600" data-testid="settings-message">{message}</div>}

                <div className="flex items-center gap-2">
                  <Button onClick={resetPassword} disabled={saving} data-testid="button-reset-password">{saving ? 'Saving...' : 'Reset password'}</Button>
                  <Button variant="outline" onClick={sendResetEmail} disabled={saving} data-testid="button-send-reset-email">Send reset email</Button>
                </div>
              </div>
            </section>
          </Card>
        </div>
      </div>
    </div>
  );
}
