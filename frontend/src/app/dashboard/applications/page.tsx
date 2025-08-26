"use client";

import React, { useMemo, useState, useEffect } from 'react';
import Sidebar from '@/components/dashboard/Sidebar';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

type Application = {
	id: string;
	jobTitle: string;
	company: string;
	appliedDate: string; // ISO date
	status: 'Submitted' | 'UnderReview' | 'Accepted' | 'Rejected' | 'Withdrawn';
	notes?: string;
	role?: string;
	budget?: string;
};

import { createJobActor } from '@/lib/icp';
import { AuthClient } from '@dfinity/auth-client';


export default function ApplicationsPage() {
	const [apps, setApps] = useState<Application[]>([]);
	const [filter, setFilter] = useState<'All'|'Submitted'|'UnderReview'|'Accepted'|'Rejected'|'Withdrawn'>('All');
	const [search, setSearch] = useState('');
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [logs, setLogs] = useState<string[]>([]);
	const [loading, setLoading] = useState(false);

	const addLog = (message: string) => {
		const timestamp = new Date().toLocaleTimeString();
		setLogs(prev => [...prev, `[${timestamp}] ${message}`]);
		console.log(`[Applications] ${message}`);
	};

	useEffect(() => {
		let mounted = true;
		(async () => {
			try {
				addLog('🔄 Starting to fetch applications...');
				setLoading(true);
				
				const authClient = await AuthClient.create();
				addLog('✅ AuthClient created successfully');
				
				const auth = await authClient.isAuthenticated();
				addLog(`🔐 Authentication status: ${auth ? 'Authenticated' : 'Not authenticated'}`);
				setIsAuthenticated(!!auth);
				
				if (!auth) {
					addLog('⚠️ User not authenticated, skipping canister fetch');
					setLoading(false);
					return;
				}
				
				const identity = authClient.getIdentity();
				addLog(`👤 User identity: ${identity.getPrincipal().toString()}`);
				
				const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
				addLog(`🌐 Using host: ${host}`);
				
				// Create HttpAgent directly
				const { HttpAgent } = await import('@dfinity/agent');
				const agent = new HttpAgent({ identity, host });
				addLog('🔧 HttpAgent created successfully');
				
				try { 
					if (process.env.NODE_ENV !== 'production') {
						addLog('🔄 Fetching root key...');
						await agent.fetchRootKey(); 
						addLog('✅ Root key fetched successfully');
					}
				} catch (e) {
					addLog(`⚠️ Root key fetch failed: ${e}`);
				}
				
				addLog('🎯 Creating job actor...');
				const actor = await createJobActor({ agent });
				addLog('✅ Job actor created successfully');
				
				addLog('📋 Calling getMyApplications()...');
				const recs = await actor.getMyApplications();
				
				// Custom serializer to handle BigInt
				const safeRecs = JSON.parse(JSON.stringify(recs, (key, value) => {
					if (typeof value === 'bigint') {
						return value.toString();
					}
					return value;
				}));
				
				addLog(`📊 Raw response from canister: ${JSON.stringify(safeRecs, null, 2)}`);
				addLog(`📊 Number of applications: ${Array.isArray(recs) ? recs.length : 'Not an array'}`);
				
				// recs expected to be array of ApplicationRecord from canister
				addLog('🔄 Starting to map application records...');
				const mapped: Application[] = await Promise.all((recs || []).map(async (r: any, index: number) => {
					// Safe serialize for logging
					const safeR = JSON.parse(JSON.stringify(r, (key, value) => {
						if (typeof value === 'bigint') {
							return value.toString();
						}
						return value;
					}));
					
					addLog(`📝 Processing application ${index + 1}: ${JSON.stringify(safeR, null, 2)}`);
					
					let applied = '';
					try {
						if (r.applied_at) {
							// Convert BigInt to number for Date constructor
							const timestamp = typeof r.applied_at === 'bigint' ? Number(r.applied_at) : Number(r.applied_at);
							if (!Number.isNaN(timestamp) && timestamp > 0) {
								// Convert nanoseconds to milliseconds if needed
								const milliseconds = timestamp > 1e12 ? timestamp / 1e6 : timestamp;
								const d = new Date(milliseconds);
								applied = d.toISOString().slice(0,10);
								addLog(`📅 Applied date: ${applied} (from timestamp: ${r.applied_at})`);
							}
						}
					} catch (e) {
						addLog(`⚠️ Failed to parse applied_at: ${e}`);
					}
					
					// try to fetch job details for nicer display
					let jobTitle = 'Unknown Job';
					let company = 'Unknown Company';
					try {
						addLog(`🔍 Fetching job details for job_id: ${r.job_id}`);
						addLog(`🔍 Job ID type: ${typeof r.job_id}, value: ${r.job_id}`);
						
						const jobRes = await actor.getJob(r.job_id || '');
						addLog(`🔍 Raw job response: ${typeof jobRes}, value: ${jobRes}`);
						
						if (jobRes && typeof jobRes === 'object') {
							// Check if jobRes has title property
							if ('title' in jobRes && jobRes.title) {
								jobTitle = String(jobRes.title);
								addLog(`✅ Job title found: ${jobTitle}`);
							} else {
								addLog(`⚠️ Job response missing title property: ${Object.keys(jobRes)}`);
							}
							
							// Try to get company from job data or use fallback
							if ('client' in jobRes && jobRes.client) {
								// Extract company name from client principal or use job ID
								const clientStr = String(jobRes.client);
								company = clientStr.length > 10 ? `${clientStr.slice(0, 8)}...` : clientStr;
							} else {
								company = `Job #${r.job_id}`;
							}
							
							// Safe serialize job details for logging
							const safeJobRes = JSON.parse(JSON.stringify(jobRes, (key, value) => {
								if (typeof value === 'bigint') {
									return value.toString();
								}
								return value;
							}));
							addLog(`✅ Job details fetched: ${JSON.stringify(safeJobRes, null, 2)}`);
						} else if (jobRes === null || jobRes === undefined) {
							addLog(`⚠️ Job response is null/undefined for job_id: ${r.job_id}`);
						} else {
							addLog(`⚠️ Unexpected job response type: ${typeof jobRes}, value: ${jobRes}`);
						}
					} catch (e) {
						addLog(`❌ Failed to fetch job details: ${e}`);
						addLog(`❌ Error details: ${e instanceof Error ? e.message : String(e)}`);
						if (e instanceof Error && e.stack) {
							addLog(`❌ Error stack: ${e.stack}`);
						}
					}
					
					// Map canister status to UI status
					let status: Application['status'] = 'Submitted';
					if (r.status) {
						const statusStr = String(r.status);
						addLog(`🏷️ Raw status from canister: ${statusStr}`);
						switch (statusStr) {
							case 'Submitted': status = 'Submitted'; break;
							case 'UnderReview': status = 'UnderReview'; break;
							case 'Accepted': status = 'Accepted'; break;
							case 'Rejected': status = 'Rejected'; break;
							case 'Withdrawn': status = 'Withdrawn'; break;
							default: status = 'Submitted';
						}
						addLog(`✅ Mapped status: ${status}`);
					}
					
					const mappedApp = {
						id: r.id || String(Math.random()).slice(2),
						jobTitle,
						company,
						appliedDate: applied,
						status,
						notes: r.cover_letter || '',
						role: jobTitle, // Use job title as role
						budget: r.proposed_budget || '',
					} as Application;
					
					// Safe serialize mapped app for logging
					const safeMappedApp = JSON.parse(JSON.stringify(mappedApp, (key, value) => {
						if (typeof value === 'bigint') {
							return value.toString();
						}
						return value;
					}));
					addLog(`✅ Mapped application: ${JSON.stringify(safeMappedApp, null, 2)}`);
					return mappedApp;
				}));
				
				if (!mounted) return;
				addLog(`🎯 Setting ${mapped.length} applications to state`);
				setApps(mapped);
			} catch (e) {
				addLog(`❌ Failed to fetch applications from canister: ${e}`);
				console.warn('Failed to fetch applications', e);
			} finally {
				if (mounted) {
					setLoading(false);
					addLog('🏁 Finished fetching applications');
				}
			}
		})();

		// No localStorage fallback - only canister data
		addLog('ℹ️ No localStorage fallback - only canister data is used');
		return () => { mounted = false; };
		return () => { mounted = false; };
	}, []);

	const filtered = useMemo(() => {
		return apps.filter(a => {
			if (filter !== 'All' && a.status !== filter) return false;
			const q = search.trim().toLowerCase();
			if (!q) return true;
			return a.jobTitle.toLowerCase().includes(q) || a.company.toLowerCase().includes(q) || (a.notes || '').toLowerCase().includes(q);
		});
	}, [apps, filter, search]);

	function withdraw(id: string) {
		setApps(s => s.map(a => a.id === id ? { ...a, status: 'Withdrawn' } : a));
	}

		function statusClasses(status: Application['status']) {
			switch (status) {
				case 'UnderReview':
					return 'text-amber-800 bg-amber-100';
				case 'Rejected':
					return 'text-red-700 bg-red-100';
				case 'Accepted':
					return 'text-emerald-800 bg-emerald-100';
				case 'Withdrawn':
					return 'text-gray-700 bg-gray-100';
				case 'Submitted':
				default:
					return 'text-sky-700 bg-sky-100';
			}
		}

	return (
		<div className="min-h-screen bg-gray-50 py-8">
			<Sidebar />

			<div className="max-w-8xl ml-0 lg:ml-80 px-4 sm:px-6 lg:px-8">
				<div className="py-6">
					<Card className="p-6 border border-gray-200 bg-white">
						<div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
							<div>
								<h1 className="text-2xl font-bold">My Applications</h1>
								<p className="text-sm text-gray-500">Track your submitted applications and their status.</p>
								<div className="mt-2 flex items-center gap-2">
									{isAuthenticated ? (
										<span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
											✅ Connected to Canister
										</span>
									) : (
										<span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
											❌ Not Connected (Canister Only - No Local Storage)
										</span>
									)}
									{loading && (
										<span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
											🔄 Loading...
										</span>
									)}
								</div>
							</div>

											<div className="flex items-center gap-3 w-full md:w-auto">
												<input value={search} onChange={(e: React.ChangeEvent<HTMLInputElement>)=>setSearch(e.target.value)} placeholder="Search by job or company" className="px-3 py-2 border rounded w-full md:w-64" data-testid="input-search-apps" />
												<select value={filter} onChange={(e: React.ChangeEvent<HTMLSelectElement>)=>setFilter(e.target.value as any)} className="px-3 py-2 border rounded" data-testid="select-filter-apps">
									<option value="All">All</option>
									<option value="Submitted">Submitted</option>
									<option value="UnderReview">Under Review</option>
									<option value="Accepted">Accepted</option>
									<option value="Rejected">Rejected</option>
									<option value="Withdrawn">Withdrawn</option>
								</select>
								
								{!isAuthenticated && (
									<Button 
										onClick={() => window.location.href = '/api/ii?redirect=/dashboard/applications'} 
										variant="outline" 
										className="bg-green-50 text-green-700 border-green-200 hover:bg-green-100 whitespace-nowrap"
									>
										🔐 Sign In to View
									</Button>
								)}
							</div>
						</div>

						<div className="space-y-4">
							{filtered.length === 0 ? (
								<div className="text-center text-gray-600">No applications found.</div>
							) : (
								filtered.map(a => (
									<div key={a.id} className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 border rounded" data-testid={`application-${a.id}`}>
										<div className="flex-1">
											<div className="flex items-center gap-3">
												<h3 className="text-lg font-semibold">{a.role || a.jobTitle}</h3>
											</div>
											<div className="text-sm text-gray-500 mt-1">at {a.company}</div>
											<div className="text-sm text-gray-600 mt-1">
												Applied: {a.appliedDate} • 
												<span className={`font-medium inline-flex items-center gap-2 px-2 py-1 rounded ${statusClasses(a.status)}`} data-testid={`application-status-${a.id}`}>
													{a.status}
												</span>
												{a.budget && (
													<span className="ml-2 text-green-600">💰 {a.budget}</span>
												)}
											</div>
											{a.notes && <div className="text-sm text-gray-700 mt-2">{a.notes}</div>}
										</div>

										<div className="mt-3 sm:mt-0 sm:ml-6 flex items-center gap-2">
											{a.status !== 'Withdrawn' && a.status !== 'Accepted' && (
												<Button variant="outline" onClick={async () => {
													// attempt to call canister to withdraw or mark withdrawn
													try {
														const authClient = await AuthClient.create();
														if (!await authClient.isAuthenticated()) { window.alert('Please sign in to withdraw'); return; }
														const identity = authClient.getIdentity();
														const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
														// Create HttpAgent directly
														const { HttpAgent } = await import('@dfinity/agent');
														const agent = new HttpAgent({ identity, host });
														try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) {}
														const actor = await createJobActor({ agent });
														if (actor.withdrawApplication) {
															await actor.withdrawApplication(a.id);
														}
													} catch (e) {
														console.warn('withdraw failed', e);
													}
													// update UI locally
													setApps(s => s.map(x => x.id === a.id ? { ...x, status: 'Withdrawn' } : x));
												}} data-testid={`button-withdraw-${a.id}`}>Withdraw</Button>
											)}
											<Button variant="ghost">View</Button>
										</div>
									</div>
								))
							)}
						</div>
					</Card>

					{/* Debug Logs Card */}
					<Card className="p-6 border border-gray-200 bg-gray-50 mt-6">
						<div className="flex items-center justify-between mb-4">
							<h3 className="text-lg font-semibold text-gray-800">🔍 Debug Logs</h3>
							<Button 
								onClick={() => setLogs([])} 
								variant="outline" 
								size="sm"
								className="text-xs"
							>
								Clear Logs
							</Button>
						</div>
						<div className="max-h-64 overflow-y-auto space-y-1">
							{logs.length === 0 ? (
								<p className="text-gray-500 text-sm">No logs yet. Try refreshing the page or check console for more details.</p>
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
		</div>
	);
}


