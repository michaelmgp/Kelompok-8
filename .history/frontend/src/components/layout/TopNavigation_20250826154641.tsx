"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
// ...existing code...
import { Button } from '@/components/ui/button';
import { connectPlug, connectInternetIdentity, getMyProfile, updateProfile, createIdentityActor, setPasswordOnCanister } from '@/lib/icp';
import { AuthClient } from '@dfinity/auth-client';
import { hashPassword } from '@/lib/crypto';

export default function TopNavigation() {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState({
    name: '',
    email: '',
    bio: '',
    skills: '',
    portfolioUrl: '',
    location: '',
    experienceLevel: '',
    role: '',
    password: '',
    confirmPassword: ''
  });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [navName, setNavName] = useState('User');
  const [navUsername, setNavUsername] = useState('user');
  const [showCreatePassword, setShowCreatePassword] = useState(false);
  const [showCreateConfirm, setShowCreateConfirm] = useState(false);

  // createForm initialized with password fields above
  const [touched, setTouched] = useState<{ [k: string]: boolean }>({});
  const [isFormValid, setIsFormValid] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formErrors, setFormErrors] = useState<{ [k: string]: string }>({});
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    // validate whole form to enable/disable submit button
    const errors: { [k: string]: string } = {};
    ['name', 'email', 'bio'].forEach((k) => {
      const v = (createForm as any)[k] || '';
      const e = validateField(k, v);
      if (e) errors[k] = e;
    });
    // password validations
    const pw = (createForm as any).password || '';
    const cpw = (createForm as any).confirmPassword || '';
    const pwErr = validateField('password', pw);
    const cpwErr = validateField('confirmPassword', cpw);
    if (pwErr) errors.password = pwErr;
    if (cpwErr) errors.confirmPassword = cpwErr;
    setFormErrors((prev) => ({ ...prev, ...errors }));
    setIsFormValid(Object.keys(errors).length === 0);
  }, [createForm]);

  // restore authentication state from localStorage
  useEffect(() => {
    try {
      const v = localStorage.getItem('cv:isAuthenticated');
      if (v === '1') setIsAuthenticated(true);
    } catch (e) {}
    try {
      const raw = localStorage.getItem('cv:profile') || localStorage.getItem('cv:pendingProfile');
      if (raw) {
        const p = JSON.parse(raw);
        if (p) {
          setNavName(p.name || 'User');
          setNavUsername(p.username || (p.email ? String(p.email).split('@')[0] : 'user'));
        }
      }
    } catch (e) {}
  }, []);

  // Listen for messages from II popup to update main window auth state
  useEffect(() => {
    function onMessage(evt: MessageEvent) {
      try {
        const data = evt.data || {};
        if (data && data.type === 'ii-auth-success') {
          try { localStorage.setItem('cv:isAuthenticated', '1'); } catch (e) {}
          setIsAuthenticated(true);
          // optional: navigate to dashboard to surface the authenticated state
          try { window.location.href = '/dashboard'; } catch (e) { window.location.reload(); }
        }
      } catch (e) { /* ignore */ }
    }
    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, []);

  // persist auth state
  useEffect(() => {
    try {
      if (isAuthenticated) localStorage.setItem('cv:isAuthenticated', '1');
      else localStorage.removeItem('cv:isAuthenticated');
    } catch (e) {}
  }, [isAuthenticated]);

  // small helper to normalize emails for consistent storage
  function normalizeEmail(v: string) {
    try {
      return (v || '').trim().toLowerCase();
    } catch (e) {
      return v;
    }
  }

  function handleChange(field: string, raw: string) {
    const value = field === 'email' ? normalizeEmail(raw) : raw;
    setCreateForm((s) => ({ ...s, [field]: value }));
    setTouched((t) => ({ ...t, [field]: true }));
    // per-field immediate validation
    const err = validateField(field, value);
    setFormErrors((prev) => ({ ...prev, [field]: err }));
  }

  return (
  <nav className="fixed top-0 left-0 right-0 bg-white shadow-sm border-b border-gray-200 z-60" data-testid="top-navigation">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <img
                src="/careerverse-logo.png"
                alt="CareerVerse"
                className="w-8 h-8"
                onError={(e: React.SyntheticEvent<HTMLImageElement, Event>) => {
                  (e.currentTarget as HTMLElement).style.display = 'none';
                  ((e.currentTarget.nextElementSibling) as HTMLElement).style.display = 'flex';
                }}
              />
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center" style={{display: 'none'}}>
                <span className="text-white font-bold text-sm">CV</span>
              </div>
              <span className="text-xl font-bold text-gray-900">CareerVerse</span>
            </Link>
          </div>

          {/* Navigation Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/jobs" className="text-gray-700 hover:text-blue-600 font-medium transition-colors" data-testid="nav-jobs">
              Job Board
            </Link>
            <Link href="/analytics" className="text-gray-700 hover:text-blue-600 font-medium transition-colors" data-testid="nav-analytics">
              Analytics
            </Link>
            <Link href="/docs" className="text-gray-700 hover:text-blue-600 font-medium transition-colors" data-testid="nav-docs">
              Docs
            </Link>
          </div>

          {/* Login/Profile */}
                  <div className="flex items-center space-x-4">
                    <div className="relative">
                      {/* If authenticated, show Dashboard link instead of Login */}
                      {isAuthenticated ? (
                        <Link href="/dashboard" data-testid="button-dashboard" className="inline-flex items-center space-x-2 px-3 py-1 border rounded hover:bg-gray-50">
                          <span className="inline-flex w-6 h-6 rounded-full bg-gray-200 items-center justify-center text-sm text-gray-700">{(() => { const parts = (navName || 'U').split(' ').filter(Boolean); if (parts.length <= 1) return (parts[0]||'U').slice(0,1).toUpperCase(); return (parts[0].slice(0,1)+parts[1].slice(0,1)).toUpperCase(); })()}</span>
                          <span>{navUsername}</span>
                        </Link>
                      ) : (
                        <Button
                          variant="outline"
                          onClick={() => {
                            // Open the login modal only; II flow is started from the modal's II button.
                            console.debug('[Login] open modal');
                            setIsLoginOpen(!isLoginOpen);
                          }}
                          className="flex items-center space-x-2"
                          data-testid="button-login"
                          data-tid="login-button"
                        >
                          {/* simplified avatar to avoid typing conflicts with Radix Avatar props */}
                          <span className="inline-flex w-6 h-6 rounded-full bg-gray-200 items-center justify-center text-sm text-gray-700">{(() => { const parts = (navName || 'U').split(' ').filter(Boolean); if (parts.length <= 1) return (parts[0]||'U').slice(0,1).toUpperCase(); return (parts[0].slice(0,1)+parts[1].slice(0,1)).toUpperCase(); })()}</span>
                          <span>Login</span>
                        </Button>
                      )}
              
              {/* Login Dropdown */}
                {isLoginOpen && (
                <div className="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 p-4 z-70 pointer-events-auto" data-testid="login-dropdown">
                    <h3 className="text-lg font-semibold mb-4">Sign In</h3>
                    <div className="space-y-3">
                      <p className="text-sm text-gray-600">Sign in using Internet Identity (ICP).</p>
                      <div className="space-y-2">
                        <Button className="w-full" data-testid="button-ii-login-mainnet" onClick={async () => {
                          try {
                            const authClient = await AuthClient.create();
                            await authClient.login({
                              identityProvider: 'https://identity.ic0.app',
                              onSuccess: async () => {
                                try { localStorage.setItem('cv:isAuthenticated', '1'); } catch (e) {}
                                setIsAuthenticated(true);
                                try { window.location.href = '/dashboard'; } catch (e) { window.location.reload(); }
                              }
                            });
                          } catch (err) {
                            console.debug('AuthClient.login failed, fallback to opening hosted II', err);
                            try { window.open('https://identity.ic0.app/#authorize', 'icp_auth', 'width=600,height=800'); } catch (e) { window.open('https://identity.ic0.app/#authorize', '_blank'); }
                          }
                        }}>
                          Login (Mainnet II)
                        </Button>

                        <Button className="w-full" data-testid="button-ii-login-mainnet" onClick={async () => {
                          try {
                            const authClient = await AuthClient.create();
                            await authClient.login({
                              identityProvider: '.localhost:8000',
                              onSuccess: async () => {
                                try { localStorage.setItem('cv:isAuthenticated', '1'); } catch (e) {}
                                setIsAuthenticated(true);
                                try { window.location.href = '/dashboard'; } catch (e) { window.location.reload(); }
                              }
                            });
                          } catch (err) {
                            console.debug('AuthClient.login failed, fallback to opening hosted II', err);
                            try { window.open('.localhost:8000/#authorize', 'icp_auth', 'width=600,height=800'); } catch (e) { window.open('https://.localhost:8000/#authorize', '_blank'); }
                          }
                        }}>
                          Login (Local II)
                        </Button>
                      </div>
                    </div>
                  </div>
              )}
              {/* Registration moved to dashboard: Create Account modal removed from top navigation. */}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
const NAME_MAX = 40;
const BIO_MAX = 200;

function validateField(k: string, v: any) {
  if (k === 'name') {
    if (!v || typeof v !== 'string' || v.trim().length === 0) return 'Name is required';
    if (v.length > NAME_MAX) return `Name must be at most ${NAME_MAX} characters`;
    return '';
  }
  if (k === 'email') {
    if (!v || typeof v !== 'string' || v.trim().length === 0) return 'Email is required';
    // Simple email regex
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return 'Invalid email address';
    return '';
  }
  if (k === 'bio') {
    if (!v || typeof v !== 'string' || v.trim().length === 0) return 'Bio is required';
    if (v.length > BIO_MAX) return `Bio must be at most ${BIO_MAX} characters`;
    return '';
  }
  if (k === 'password') {
    if (!v || typeof v !== 'string' || v.length < 8) return 'Password must be at least 8 characters';
    // Optionally check for complexity
    // if (!/[A-Z]/.test(v) || !/[0-9]/.test(v)) return 'Password must contain a number and uppercase letter';
    return '';
  }
  if (k === 'confirmPassword') {
    // You may need access to the original password value for comparison
    // For this context, assume it's available via a closure or passed in
    // But here, just check for non-empty
    if (!v || typeof v !== 'string' || v.length < 8) return 'Confirm password must be at least 8 characters';
    // The actual comparison is handled in the submit handler
    return '';
  }
  return '';
}

