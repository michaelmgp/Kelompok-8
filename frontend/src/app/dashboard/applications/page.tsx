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

import { createJobActor, getPendingApplications, flushPendingApplications, createHttpAgent } from '@/lib/icp';
import { AuthClient } from '@dfinity/auth-client';


export default function ApplicationsPage() {
	const [apps, setApps] = useState<Application[]>([]);
	const [filter, setFilter] = useState<'All'|'Submitted'|'UnderReview'|'Accepted'|'Rejected'|'Withdrawn'>('All');
	const [search, setSearch] = useState('');
	const [isAuthenticated, setIsAuthenticated] = useState(false);

	useEffect(() => {
		let mounted = true;
		(async () => {
			try {
				const authClient = await AuthClient.create();
				const auth = await authClient.isAuthenticated();
				setIsAuthenticated(!!auth);
				if (!auth) return;
				const identity = authClient.getIdentity();
				const host = process.env.NEXT_PUBLIC_DFX_HOST || (typeof window !== 'undefined' && window.location.hostname === 'localhost' ? 'http://127.0.0.1:8000' : window.location.origin);
				const agent = createHttpAgent({ identity, host });
				try { if (process.env.NODE_ENV !== 'production') await agent.fetchRootKey(); } catch (e) {}
				const actor = await createJobActor({ agent });
				const recs = await actor.getMyApplications();
				// recs expected to be array of ApplicationRecord from canister
				const mapped: Application[] = await Promise.all((recs || []).map(async (r: any) => {
					let applied = '';
					try {
						if (r.applied_at) {
							const n = Number(r.applied_at);
							if (!Number.isNaN(n) && n > 0) {
								const d = new Date(n);
								applied = d.toISOString().slice(0,10);
							}
						}
					} catch (e) {}
					
					// try to fetch job details for nicer display
					let jobTitle = 'Unknown Job';
					let company = 'Unknown Company';
					try {
						const jobRes = await actor.getJob(r.job_id || '');
						if (jobRes) {
							jobTitle = jobRes.title || 'Unknown Job';
							// For now, use job ID as company since client is Principal
							company = `Job #${r.job_id}`;
						}
					} catch (e) {
						console.debug('Failed to fetch job details:', e);
					}
					
					// Map canister status to UI status
					let status: Application['status'] = 'Submitted';
					if (r.status) {
						const statusStr = String(r.status);
						switch (statusStr) {
							case 'Submitted': status = 'Submitted'; break;
							case 'UnderReview': status = 'UnderReview'; break;
							case 'Accepted': status = 'Accepted'; break;
							case 'Rejected': status = 'Rejected'; break;
							case 'Withdrawn': status = 'Withdrawn'; break;
							default: status = 'Submitted';
						}
					}
					
					return {
						id: r.id || String(Math.random()).slice(2),
						jobTitle,
						company,
						appliedDate: applied,
						status,
						notes: r.cover_letter || '',
						role: jobTitle, // Use job title as role
						budget: r.proposed_budget || '',
					} as Application;
				}));
				if (!mounted) return;
				setApps(mapped);
			} catch (e) {
				console.warn('Failed to fetch applications', e);
			}
		})();

		// If not authenticated, load any locally saved pending applications so users
		// can see what will be submitted after they sign in.
		try {
			const pending = getPendingApplications();
			if (pending && pending.length > 0 && mounted) {
				// Map minimal pending structure into the UI model
				const mapped = pending.map((p: any) => ({
					id: p.jobId + '::pending::' + (p.createdAt || ''),
					jobTitle: 'Pending: ' + (p.jobTitle || p.jobId),
					company: 'Local Storage',
					appliedDate: p.createdAt ? (new Date(p.createdAt)).toISOString().slice(0,10) : '',
					status: 'Submitted' as any,
					notes: p.cover || '',
					budget: p.budget || '',
				}));
				setApps((s) => [...mapped, ...s]);
			}
		} catch (e) { /* ignore */ }
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
														const agent = createHttpAgent({ identity, host });
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
				</div>
			</div>
		</div>
	);
}

