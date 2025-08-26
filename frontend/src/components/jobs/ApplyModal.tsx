"use client";

import React, { useState } from 'react';
import { X, Send } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { savePendingApplication, createJobActor, createIdentityActor, createHttpAgent } from '@/lib/icp';
import { AuthClient } from '@dfinity/auth-client';

type Props = {
  open: boolean;
  job: any;
  onClose: () => void;
};

export default function ApplyModal({ open, job, onClose }: Props) {
  const [cover, setCover] = useState(`Hi, I'm interested in ${job?.title || ''} at ${job?.company || ''}.`);
  const [budget, setBudget] = useState('');
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  async function submit() {
    if (!open) return null;
    setLoading(true);
    
    try {
      // Always try to authenticate first
      const authClient = await AuthClient.create();
      const isAuth = await authClient.isAuthenticated();
      
      if (isAuth) {
        // User is authenticated, submit to canister
        try {
          const envHost = process.env.NEXT_PUBLIC_DFX_HOST || '';
          const jobGatewayUrl = process.env.NEXT_PUBLIC_JOB_GATEWAY_URL || '';
          const isMainnet = !envHost || envHost.includes('ic0.app');
          let host = isMainnet ? 'https://ic0.app' : envHost;
          
          // If a gateway-style URL is provided for jobs, prefer it on local/dev
          if (!isMainnet && jobGatewayUrl) host = jobGatewayUrl;
          
          const identity = authClient.getIdentity();
          const agent = createHttpAgent({ identity, host });
          try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) {}
          
          const actor = await createJobActor({ agent });
          
          const safeJobId = String(job.id || '');
          const safeCover = String(cover || '');
          const safeBudget = String(budget || '');
          
          // Validate required fields
          if (!safeJobId || safeJobId.trim() === '') {
            throw new Error('Job ID is required');
          }
          if (!safeCover || safeCover.trim() === '') {
            throw new Error('Cover letter is required');
          }
          if (!safeBudget || safeBudget.trim() === '') {
            throw new Error('Budget is required');
          }
          
          console.log('Submitting application with:', { safeJobId, safeCover, safeBudget });
          
          // Use the correct method from job_contract.mo
          await actor.submitApplication(safeJobId, safeCover, safeBudget);
          
          // Success! Redirect to applications page
          window.alert('✅ Application submitted successfully to canister!');
          window.location.href = '/dashboard/applications';
          return;
        } catch (err: any) {
          console.error('Failed to submit to canister', err);
          window.alert('❌ Failed to submit to canister: ' + (err?.message || String(err)));
          setLoading(false);
          return;
        }
      } else {
        // User not authenticated, save locally and redirect to login
        try { 
          savePendingApplication({ 
            jobId: job.id, 
            cover: cover || '', 
            budget: budget || '' 
          }); 
        } catch (err: any) {
          console.error('Failed to save pending application', err);
        }
        
        window.alert('🔐 Please sign in with Internet Identity to submit your application to the canister. Your application is saved locally and will be submitted after sign-in.');
        
        // Redirect to login
        setTimeout(() => {
          window.location.href = '/api/ii?redirect=/dashboard/jobboard';
        }, 1000);
        
        setLoading(false);
        return;
      }
    } catch (err: any) {
      console.error('Unexpected error in submit', err);
      window.alert('❌ Unexpected error: ' + (err?.message || String(err)));
    } finally {
      setLoading(false);
    }
  }

  return (
    <React.Fragment>
      <div className="fixed inset-0 z-50 flex items-center justify-center">
        <div className="absolute inset-0 bg-black/40" onClick={onClose} />
        <div className="relative w-full max-w-xl mx-4 bg-white rounded-lg shadow-lg border border-gray-200 p-6 z-60">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Apply to {job?.title}</h3>
            <button onClick={onClose} className="p-1 rounded-md hover:bg-gray-100">
              <X size={18} />
            </button>
          </div>
          
          <div className="space-y-3">
            <div>
              <label className="text-sm font-medium">Cover letter</label>
              <textarea 
                value={cover} 
                onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setCover(e.target.value)} 
                rows={6} 
                className="w-full p-3 border rounded resize-none" 
                placeholder="Explain why you're interested in this position..."
              />
            </div>
            
            <div>
              <label className="text-sm font-medium">Proposed budget</label>
              <input 
                type="text" 
                value={budget} 
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setBudget(e.target.value)} 
                className="w-full p-3 border rounded" 
                placeholder="e.g., $50/hour or $5000 project"
              />
            </div>
            
            <div className="pt-4">
              <Button 
                onClick={submit} 
                disabled={loading || !cover.trim() || !budget.trim()} 
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Submitting...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <Send size={16} />
                    Submit Application
                  </div>
                )}
              </Button>
              
              {(!cover.trim() || !budget.trim()) && (
                <p className="text-xs text-red-500 mt-2 text-center">
                  Please fill in both cover letter and budget before submitting
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
}
