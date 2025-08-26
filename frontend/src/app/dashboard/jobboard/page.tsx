"use client";

import React, { useMemo, useState, useEffect } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import { Card } from '@/components/ui/card';
import jobs from '@/lib/jobs';
import ApplyModal from '@/components/jobs/ApplyModal';
import { Button } from '@/components/ui/button';
import { AuthClient } from '@dfinity/auth-client';

export default function JobBoardPage() {
  const [page, setPage] = useState(1);
  const [pageSize] = useState(4);
  const [searchTerm, setSearchTerm] = useState('');
  const [applyingJob, setApplyingJob] = useState<any | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState<string[]>([]);
  const [showLogs, setShowLogs] = useState(false);

  useEffect(() => {
    async function checkAuth() {
      try {
        const authClient = await AuthClient.create();
        const auth = await authClient.isAuthenticated();
        setIsAuthenticated(!!auth);
      } catch (err) {
        console.debug('Failed to check authentication', err);
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, []);

  function openApply(job: any) {
    setApplyingJob(job);
  }

  function closeApply() {
    setApplyingJob(null);
  }

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${timestamp}] ${message}`]);
    console.log(`[JobBoard] ${message}`);
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const filteredJobs = useMemo(() => {
    const q = searchTerm.trim().toLowerCase();
    if (!q) return jobs;
    return jobs.filter((job) => {
      const inTitle = job.title?.toLowerCase().includes(q);
      const inCompany = job.company?.toLowerCase().includes(q);
      const inLocation = job.location?.toLowerCase().includes(q);
      const inSkills = (job.skills || []).join(' ').toLowerCase().includes(q);
      const inDescription = job.description?.toLowerCase().includes(q);
      return inTitle || inCompany || inLocation || inSkills || inDescription;
    });
  }, [searchTerm]);

  const totalPages = Math.max(1, Math.ceil(filteredJobs.length / pageSize));

  const current = useMemo(() => {
    const start = (page - 1) * pageSize;
    return filteredJobs.slice(start, start + pageSize);
  }, [page, pageSize, filteredJobs]);

  function go(n: number) {
    const next = Math.min(Math.max(1, n), totalPages);
    setPage(next);
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <Sidebar />
  <div className="max-w-8xl ml-0 lg:ml-80 px-4 sm:px-6 lg:px-8">
        <div className="mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="w-full md:flex-1">
            <h1 className="text-2xl font-bold">Job Board</h1>
            <p className="text-sm text-gray-600 mt-1">Browse curated openings matched by our AI agents.</p>
            {!loading && (
              <div className="mt-2">
                {isAuthenticated ? (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    ✅ Connected to Canister
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    ⚠️ Not Connected (Apply will be saved locally)
                  </span>
                )}
              </div>
            )}
          </div>

          <div className="flex-1 md:flex-none w-full md:w-auto flex items-center gap-3">
            <input
              type="text"
              placeholder="Search jobs, skills, companies, locations..."
              value={searchTerm}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => { setSearchTerm(e.target.value); setPage(1); }}
              className="w-full md:w-96 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              data-testid="input-search-jobs"
            />

            <label className="text-sm text-gray-600">Per page</label>
            <select value={pageSize} onChange={(e: React.ChangeEvent<HTMLSelectElement>) => { setPage(1); }} className="px-2 py-1 border rounded">
              <option value={4}>4</option>
              <option value={6}>6</option>
              <option value={8}>8</option>
            </select>

            {!isAuthenticated && (
              <Button 
                onClick={() => window.location.href = '/api/ii?redirect=/dashboard/jobboard'} 
                variant="outline" 
                className="bg-green-50 text-green-700 border-green-200 hover:bg-green-100 whitespace-nowrap"
              >
                🔐 Sign In to Apply
              </Button>
            )}
          </div>
        </div>

        <div className="grid gap-6 sm:grid-cols-2">
          {current.map((job) => (
            <Card key={job.id} className="p-6 border border-gray-200 hover:shadow-md" data-testid={`job-card-${job.id}`}>
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2" data-testid={`job-title-${job.id}`}>
                    {job.title}
                  </h3>
                  <p className="text-blue-600 font-medium" data-testid={`job-company-${job.id}`}>
                    {job.company}
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-yellow-500">⭐</span>
                  <span className="text-gray-700 font-medium" data-testid={`job-rating-${job.id}`}>{job.rating}</span>
                </div>
              </div>

              <p className="text-gray-600 mb-4" data-testid={`job-description-${job.id}`}>
                {job.description}
              </p>

              <div className="flex flex-wrap gap-2 mb-4">
                {job.skills?.map((skill: string, index: number) => (
                  <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm" data-testid={`job-skill-${job.id}-${index}`}>{skill}</span>
                ))}
              </div>

              <div className="flex justify-between items-center">
                <div className="flex space-x-6 text-sm text-gray-600">
                  <span data-testid={`job-salary-${job.id}`}>💰 {job.salary}</span>
                  <span data-testid={`job-location-${job.id}`}>📍 {job.location}</span>
                  <span data-testid={`job-posted-${job.id}`}>🕒 {job.postedDate}</span>
                </div>
        <button onClick={() => openApply(job)} className="text-sm text-white bg-blue-600 px-3 py-1 rounded">Apply</button>
              </div>
            </Card>
          ))}
      {applyingJob && <ApplyModal open={true} job={applyingJob} onClose={closeApply} onLog={addLog} />}
        </div>

        {/* Pagination controls */}
        {filteredJobs.length === 0 ? (
          <div className="mt-6 text-center text-gray-600">No jobs match "{searchTerm}"</div>
        ) : (
          <div className="mt-6 flex items-center justify-center space-x-3">
          <button onClick={() => go(page - 1)} disabled={page <= 1} className="px-3 py-1 border rounded disabled:opacity-50">Prev</button>
          {Array.from({ length: totalPages }).map((_, i) => (
            <button key={i} onClick={() => go(i + 1)} className={`px-3 py-1 border rounded ${page === i + 1 ? 'bg-blue-600 text-white' : ''}`}>{i + 1}</button>
          ))}
          <button onClick={() => go(page + 1)} disabled={page >= totalPages} className="px-3 py-1 border rounded disabled:opacity-50">Next</button>
          </div>
        )}

        
      </div>
    </div>
  );
}
