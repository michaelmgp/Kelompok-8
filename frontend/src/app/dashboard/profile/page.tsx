"use client";

import React, { useState, useEffect } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AuthClient } from '@dfinity/auth-client';
import { HttpAgent } from '@dfinity/agent';
import { createIdentityActor, getMyProfile, updateProfile } from '@/lib/icp';

export default function ProfilePage() {
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  const [profile, setProfile] = useState({
    name: 'User Name',
    username: 'username',
    // title removed; use `role` instead
    location: 'Jakarta, ID',
    email: 'user@example.com',
    portfolioUrl: '',
    skills: 'React,TypeScript,Next.js',
  about: 'This is a short bio about the user. Write something that highlights your background and strengths.',
  role: 'Frontend Engineer'
  });

  // whether the client is authenticated via Internet Identity / Plug
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Add log function
  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [`[${timestamp}] ${message}`, ...prev.slice(0, 19)]); // Keep last 20 logs
  };

  useEffect(() => {
    (async () => {
      // Load any local profile first (pending or stored)
      try {
        const raw = localStorage.getItem('cv:profile') || localStorage.getItem('cv:pendingProfile');
        if (raw) {
          const p = JSON.parse(raw);
            if (p) {
            setProfile((prev) => ({
              ...prev,
              name: p.name || prev.name,
              // prefer stored username, otherwise derive from email local value
              username: p.username || (p.email ? String(p.email).split('@')[0] : prev.username),
              location: p.location || prev.location,
              email: p.email || prev.email,
              portfolioUrl: p.portfolioUrl || prev.portfolioUrl,
                skills: Array.isArray(p.skills) ? p.skills.join(',') : (p.skills || prev.skills),
                about: p.bio || prev.about,
                role: p.role || prev.role,
            }));
          }
        }
      } catch (e) {
        // ignore
      }

      // If the user completed Internet Identity (AuthClient), fetch profile from canister
      try {
        const authClient = await AuthClient.create();
        const auth = await authClient.isAuthenticated();
        setIsAuthenticated(!!auth);
        if (!auth) return;

        const identity = authClient.getIdentity();
        const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
        const agent = new HttpAgent({ identity, host });
        try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) { /* ignore */ }

        const actor = await createIdentityActor({ agent });
        const p = await actor.getMyProfile();
        if (p) {
          // Motoko UserProfile fields: name, email, bio, skills (array), portfolio_url, location, experience_level
          setProfile(prev => ({
            ...prev,
            name: p.name || prev.name,
            // derive username from canister email if username not present
            username: p.username || (p.email ? String(p.email).split('@')[0] : prev.username),
            email: p.email || prev.email,
            portfolioUrl: p.portfolio_url || prev.portfolioUrl,
            skills: Array.isArray(p.skills) ? p.skills.join(',') : prev.skills,
            about: p.bio || prev.about,
            location: p.location || prev.location,
            // map canister experience_level or role into local role
            role: p.role || p.experience_level || prev.role,
          }));
          // persist locally for quicker UI display
          try { localStorage.setItem('cv:profile', JSON.stringify({
            name: p.name,
            email: p.email,
            bio: p.bio,
            skills: p.skills,
            portfolioUrl: p.portfolio_url,
            location: p.location,
            experienceLevel: p.role || p.experience_level,
            role: p.role || ''
          })); } catch (e) {}
        }
      } catch (err) {
        // not authenticated or fetch failed — keep local data
        console.debug('profile: not authenticated or fetch failed', err);
      }
    })();
  }, []);

  const NAME_MAX = 100;
  const BIO_MAX = 300;

  function validate() {
    const errs: string[] = [];
    if (!profile.name || profile.name.trim().length < 2) errs.push('Name is required');
    if (profile.name.length > NAME_MAX) errs.push(`Name must be ≤ ${NAME_MAX} characters`);
    if (profile.about.length > BIO_MAX) errs.push(`Bio must be ≤ ${BIO_MAX} characters`);
    return errs;
  }

  async function save() {
    const errs = validate();
    if (errs.length > 0) {
      setMessage(errs.join('; '));
      return;
    }
    setSaving(true);
    setMessage(null);
    
    try {
      // Always try to authenticate first
      const authClient = await AuthClient.create();
      const auth = await authClient.isAuthenticated();
      
      if (auth) {
        // User is authenticated, save to canister
        try {
                  const identity = authClient.getIdentity();
        const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
        const agent = new HttpAgent({ identity, host });
        try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) {}
        
        const actor = await createIdentityActor({ agent });
          const skillsArr = profile.skills.split(',').map(s => s.trim()).filter(Boolean);
          
          addLog('🔍 Preparing profile data for canister...');
          
          // Ensure all parameters are properly formatted
          const name = profile.name || '';
          const email = profile.email || '';
          const bio = profile.about || '';
          const skills = skillsArr;
          const portfolioUrl = profile.portfolioUrl || '';
          const location = profile.location || '';
          const experienceLevel = profile.role || '';
          
          // Log each parameter individually for debugging
          addLog(`📝 Name: "${name}"`);
          addLog(`📝 Email: "${email}"`);
          addLog(`📝 Bio: "${bio}"`);
          addLog(`📝 Skills: [${skills.join(', ')}]`);
          addLog(`📝 Portfolio URL: "${portfolioUrl}"`);
          addLog(`📝 Location: "${location}"`);
          addLog(`📝 Experience Level: "${experienceLevel}"`);
          
          // Log actor method details
          addLog('🔍 Actor details:');
          addLog(`  - Actor type: ${typeof actor}`);
          addLog(`  - Actor methods: ${Object.keys(actor || {}).join(', ')}`);
          addLog(`  - updateProfile method: ${typeof actor?.updateProfile}`);
          
          console.log('🔍 Saving profile to canister with data:', {
            name,
            email,
            bio,
            skills,
            portfolioUrl,
            location,
            experienceLevel
          });
          
          // Log the exact method call
          addLog('🔍 Calling actor.updateProfile with 7 parameters...');
          addLog(`  - Parameter 1 (name): ${typeof name} = "${name}"`);
          addLog(`  - Parameter 2 (email): ${typeof email} = "${email}"`);
          addLog(`  - Parameter 3 (bio): ${typeof bio} = "${bio}"`);
          addLog(`  - Parameter 4 (skills): ${typeof skills} = [${skills.join(', ')}]`);
          addLog(`  - Parameter 5 (portfolioUrl): ${typeof portfolioUrl} = "${portfolioUrl}"`);
          addLog(`  - Parameter 6 (location): ${typeof location} = "${location}"`);
          addLog(`  - Parameter 7 (experienceLevel): ${typeof experienceLevel} = "${experienceLevel}"`);
          
          const result = await updateProfile({
            name,
            email,
            bio,
            skills,
            portfolioUrl,
            location,
            experienceLevel
          }, actor);
          
          console.log('✅ Profile save result:', result);
          
          setMessage('✅ Profile successfully saved to canister!');
          setIsAuthenticated(true);
          
          // Update local copy for faster UI
          try { localStorage.setItem('cv:profile', JSON.stringify({
            name: profile.name,
            email: profile.email,
            bio: profile.about,
            skills: skillsArr,
            portfolioUrl: profile.portfolioUrl,
            location: profile.location,
            experienceLevel: profile.role,
            role: profile.role || ''
          })); } catch (e) {}
          
        } catch (err: any) {
          console.error('save: canister update failed', err);
          setMessage('❌ Failed to save to canister: ' + (err?.message || String(err)));
          
          // Fallback: save locally as pending
          try { localStorage.setItem('cv:pendingProfile', JSON.stringify({
            name: profile.name,
            email: profile.email,
            bio: profile.about,
            skills: profile.skills.split(',').map(s=>s.trim()).filter(Boolean),
            portfolioUrl: profile.portfolioUrl,
            location: profile.location,
            experienceLevel: profile.role,
            role: profile.role || ''
          })); } catch (e) {}
        }
      } else {
        // User not authenticated, redirect to login
        setMessage('🔐 Please sign in with Internet Identity to save your profile to the canister');
        
        // Save locally as pending profile
        try { localStorage.setItem('cv:pendingProfile', JSON.stringify({
          name: profile.name,
          email: profile.email,
          bio: profile.about,
          skills: profile.skills.split(',').map(s=>s.trim()).filter(Boolean),
          portfolioUrl: profile.portfolioUrl,
          location: profile.location,
          experienceLevel: profile.role,
          role: profile.role || ''
        })); } catch (e) {}
        
        // Redirect to login after a short delay
        setTimeout(() => {
          window.location.href = '/api/ii?redirect=/dashboard/profile';
        }, 2000);
      }
    } catch (err: any) {
      console.error('save: unexpected error', err);
      setMessage('❌ Unexpected error: ' + (err?.message || String(err)));
    } finally {
      setSaving(false);
      setEditing(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <Sidebar />

      <div className="max-w-8xl ml-0 lg:ml-80 px-4 sm:px-6 lg:px-8">
        <div className="py-6">
          <Card className="p-6 border border-gray-200 bg-white">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center text-2xl font-bold">
                  {(() => {
                    const parts = (profile.name || 'U').split(' ').filter(Boolean);
                    if (parts.length === 0) return 'U';
                    if (parts.length === 1) return parts[0].slice(0,1).toUpperCase();
                    return (parts[0].slice(0,1) + parts[1].slice(0,1)).toUpperCase();
                  })()}
                </div>
                <div>
                  <h2 className="text-2xl font-semibold" data-testid="profile-name">{profile.name}</h2>
                  <div className="text-sm text-gray-500" data-testid="profile-username">@{profile.username}</div>
                  <div className="text-sm text-gray-700 mt-1" data-testid="profile-role">{(profile as any).role} — {profile.location}</div>
                  <div className="mt-2">
                    {isAuthenticated ? (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        ✅ Connected to Canister
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        ⚠️ Not Connected (Local Storage Only)
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2">
                {!isAuthenticated && (
                  <Button 
                    onClick={() => window.location.href = '/api/ii?redirect=/dashboard/profile'} 
                    variant="outline" 
                    className="bg-green-50 text-green-700 border-green-200 hover:bg-green-100"
                  >
                    🔐 Sign In to Save
                  </Button>
                )}
                <Button onClick={() => { setEditing((s) => !s); setMessage(null); }} data-testid="button-edit-profile">
                  {editing ? 'Close' : 'Edit Profile'}
                </Button>
              </div>
            </div>

            {!editing && (
              <div>
                <p className="text-gray-700 mb-4" data-testid="profile-about">{profile.about}</p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <div className="text-xs text-gray-500">Email</div>
                    <div className="text-sm text-gray-800" data-testid="profile-email">{profile.email}</div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500">Portfolio</div>
                    <div className="text-sm text-blue-600" data-testid="profile-portfolio">{profile.portfolioUrl || '—'}</div>
                  </div>
                </div>

                <div className="mt-4">
                  <div className="text-xs text-gray-500">Skills</div>
                  <div className="flex flex-wrap gap-2 mt-2" data-testid="profile-skills">
                    {profile.skills.split(',').filter(Boolean).map((s, i) => (
                      <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">{s.trim()}</span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {editing && (
              <div className="mt-4 space-y-3" data-testid="profile-edit-form">
                <div>
                  <label className="text-sm text-gray-600">Full name</label>
                  <input value={profile.name} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProfile(p => ({ ...p, name: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" />
                </div>

                <div>
                  <label className="text-sm text-gray-600">Role</label>
                  <input value={(profile as any).role || ''} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProfile(p => ({ ...p, role: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" placeholder="Frontend Engineer / UI UX" />
                </div>

                <div>
                  <label className="text-sm text-gray-600">Location</label>
                  <input value={profile.location} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProfile(p => ({ ...p, location: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" />
                </div>

                <div>
                  <label className="text-sm text-gray-600">Email</label>
                  <input value={profile.email} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProfile(p => ({ ...p, email: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" />
                </div>

                <div>
                  <label className="text-sm text-gray-600">Portfolio URL</label>
                  <input value={profile.portfolioUrl} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProfile(p => ({ ...p, portfolioUrl: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" />
                </div>

                <div>
                  <label className="text-sm text-gray-600">Skills (comma separated)</label>
                  <input value={profile.skills} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setProfile(p => ({ ...p, skills: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" />
                </div>

                <div>
                  <label className="text-sm text-gray-600">About / Bio</label>
                  <textarea value={profile.about} onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setProfile(p => ({ ...p, about: e.target.value }))} className="w-full px-3 py-2 border rounded mt-1" rows={5} />
                  <div className="text-xs text-gray-500 mt-1">{profile.about.length}/{BIO_MAX}</div>
                </div>

                {message && <div className="text-sm text-red-600">{message}</div>}

                <div className="flex space-x-2">
                  <Button onClick={save} disabled={saving} data-testid="button-save-profile">{saving ? 'Saving...' : 'Save'}</Button>
                  <Button variant="ghost" onClick={() => { setEditing(false); setMessage(null); }} data-testid="button-cancel-edit">Cancel</Button>
                </div>
              </div>
            )}
          </Card>

          
        </div>
      </div>
    </div>
  );
}
