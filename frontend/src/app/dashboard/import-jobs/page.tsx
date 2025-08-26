"use client";

import React, { useState } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import jobs from '@/lib/jobs';
import { createJobActor } from '@/lib/icp';
import { AuthClient } from '@dfinity/auth-client';

export default function ImportJobsPage() {
  const [importing, setImporting] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [importedJobs, setImportedJobs] = useState<string[]>([]);

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${timestamp}] ${message}`]);
    console.log(`[ImportJobs] ${message}`);
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const importAllJobs = async () => {
    setImporting(true);
    setImportedJobs([]);
    
    try {
      addLog('🔄 Starting job import process...');
      
      // Check authentication
      const authClient = await AuthClient.create();
      const isAuth = await authClient.isAuthenticated();
      
      if (!isAuth) {
        addLog('❌ User not authenticated. Please sign in first.');
        setImporting(false);
        return;
      }
      
      addLog('✅ User authenticated, proceeding with import...');
      
      // Create actor
      const identity = authClient.getIdentity();
      const host = process.env.NEXT_PUBLIC_DFX_HOST || 'http://127.0.0.1:8000';
      
      const { HttpAgent } = await import('@dfinity/agent');
      const agent = new HttpAgent({ identity, host });
      
      try { 
        if (process.env.NODE_ENV !== 'production') {
          addLog('🔄 Fetching root key...');
          await agent.fetchRootKey(); 
          addLog('✅ Root key fetched successfully');
        }
      } catch (e) {
        addLog(`⚠️ Root key fetch failed: ${e}`);
      }
      
      const actor = await createJobActor({ agent });
      addLog('✅ Job actor created successfully');
      
      // Import each job
      for (let i = 0; i < jobs.length; i++) {
        const job = jobs[i];
        try {
          addLog(`📝 Importing job ${i + 1}/${jobs.length}: ${job.title}`);
          
          // Convert skills array to string array
          const skills = job.skills || [];
          
                     // Use empty array for optional deadline parameter (Motoko ?Int)
           addLog(`  - Title: "${job.title}"`);
           addLog(`  - Description: "${job.description.substring(0, 50)}..."`);
           addLog(`  - Budget: "${job.salary}"`);
           addLog(`  - Skills: [${skills.join(', ')}]`);
           addLog(`  - Deadline: [] (empty array for optional)`);
           
           const result = await actor.createJob(
             job.title,
             job.description,
             job.salary,
             skills,
             []
           );
          
          addLog(`✅ Job "${job.title}" imported successfully: ${JSON.stringify(result, null, 2)}`);
          
          // Extract job ID from result
          let jobId = 'Unknown';
          if (result && typeof result === 'object' && 'ok' in result) {
            jobId = result.ok || 'Unknown';
          } else if (typeof result === 'string') {
            jobId = result;
          }
          
          setImportedJobs(prev => [...prev, `${job.title} (${jobId})`]);
          
        } catch (err: any) {
          const errorMsg = err?.message || String(err);
          addLog(`❌ Failed to import job "${job.title}": ${errorMsg}`);
        }
        
        // Small delay between imports
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
      
      addLog('🏁 Job import process completed!');
      
    } catch (err: any) {
      addLog(`❌ Unexpected error: ${err?.message || String(err)}`);
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <Sidebar />
      <div className="max-w-8xl ml-0 lg:ml-80 px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Import Jobs to Canister</h1>
          <p className="text-sm text-gray-600 mt-1">
            Import all dummy jobs from the static data to the canister so they can be applied to.
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {/* Import Control */}
          <Card className="p-6 border border-gray-200 bg-white">
            <h3 className="text-lg font-semibold mb-4">Import Control</h3>
            
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 mb-2">
                  Total jobs to import: <strong>{jobs.length}</strong>
                </p>
                <p className="text-sm text-gray-600">
                  This will create jobs in the canister that users can apply to.
                </p>
              </div>
              
              <Button 
                onClick={importAllJobs} 
                disabled={importing}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400"
              >
                {importing ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Importing Jobs...
                  </div>
                ) : (
                  '🚀 Import All Jobs to Canister'
                )}
              </Button>
              
              {importedJobs.length > 0 && (
                <div className="bg-green-50 p-3 rounded">
                  <h4 className="font-medium text-green-800 mb-2">✅ Imported Jobs:</h4>
                  <ul className="text-sm text-green-700 space-y-1">
                    {importedJobs.map((job, index) => (
                      <li key={index}>• {job}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </Card>

          {/* Jobs Preview */}
          <Card className="p-6 border border-gray-200 bg-white">
            <h3 className="text-lg font-semibold mb-4">Jobs to Import</h3>
            
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {jobs.map((job) => (
                <div key={job.id} className="p-3 border rounded bg-gray-50">
                  <h4 className="font-medium text-gray-900">{job.title}</h4>
                  <p className="text-sm text-gray-600">{job.company}</p>
                  <p className="text-sm text-gray-500">{job.salary} • {job.location}</p>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {job.skills.map((skill, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Debug Logs */}
        <Card className="p-6 border border-gray-200 bg-gray-50 mt-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">🔍 Import Logs</h3>
            <Button 
              onClick={clearLogs} 
              variant="outline" 
              size="sm"
              className="text-xs"
            >
              Clear Logs
            </Button>
          </div>
          
          <div className="max-h-64 overflow-y-auto space-y-1">
            {logs.length === 0 ? (
              <p className="text-gray-500 text-sm">No logs yet. Click "Import All Jobs" to start.</p>
            ) : (
              logs.map((log, index) => (
                <div key={index} className="text-xs font-mono bg-white p-2 rounded border">
                  {log}
                </div>
              ))
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
