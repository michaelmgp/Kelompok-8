"use client";

import { useState, useEffect } from 'react';
import { fetchJobs } from '@/services/jobsApi';

// Define an interface for the job object from the API
interface Job {
  id: string;
  title: string;
  company: string;
  description: string | null;
  skills: string[];
  source_rating: number | null;
  location: string | null;
  posted_at: string;
  budget_min: number | null;
  budget_max: number | null;
  currency: string | null;
  rate_type: string | null;
}

export default function JobBoard() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getJobs = async () => {
      try {
        setLoading(true);
        const data = await fetchJobs();
        setJobs(data.jobs);
        setError(null);
      } catch (err) {
        setError('Failed to fetch jobs.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    getJobs();
  }, []);


  const categories = [
    { value: 'all', label: 'All Jobs' },
    { value: 'frontend', label: 'Frontend' },
    { value: 'blockchain', label: 'Blockchain' },
    { value: 'ai', label: 'AI/ML' },
    { value: 'design', label: 'Design' }
  ];

  const formatSalary = (job: Job) => {
    if (job.budget_min && job.budget_max) {
      return `${job.currency} ${job.budget_min} - ${job.budget_max}`;
    }
    if (job.rate_type) {
        return `Rate type: ${job.rate_type}`;
    }
    return 'Not specified';
  };

  const formatPostedDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays === 1) {
        return "1 day ago";
    }
    return `${diffDays} days ago`;
  }


  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4" data-testid="job-board-title">
            Decentralized Job Board
          </h1>
          <p className="text-xl text-gray-600">
            Find opportunities matched by AI agents in the decentralized economy
          </p>
        </div>

        {/* Search and Filter */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Search jobs, skills, companies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                data-testid="input-search-jobs"
              />
            </div>
            <div>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                data-testid="select-category"
              >
                {categories.map(category => (
                  <option key={category.value} value={category.value}>
                    {category.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Job Listings */}
        {loading && <p>Loading jobs...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {!loading && !error && (
            <div className="grid gap-6">
            {jobs.map((job) => (
                <div key={job.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow" data-testid={`job-card-${job.id}`}>
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
                    <span className="text-gray-700 font-medium" data-testid={`job-rating-${job.id}`}>
                        {job.source_rating || 'N/A'}
                    </span>
                    </div>
                </div>

                <p className="text-gray-600 mb-4" data-testid={`job-description-${job.id}`}>
                    {job.description || 'No description available.'}
                </p>

                <div className="flex flex-wrap gap-2 mb-4">
                    {job.skills.map((skill, index) => (
                    <span
                        key={index}
                        className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                        data-testid={`job-skill-${job.id}-${index}`}
                    >
                        {skill}
                    </span>
                    ))}
                </div>

                <div className="flex justify-between items-center">
                    <div className="flex space-x-6 text-sm text-gray-600">
                    <span data-testid={`job-salary-${job.id}`}>💰 {formatSalary(job)}</span>
                    <span data-testid={`job-location-${job.id}`}>📍 {job.location || 'Remote'}</span>
                    <span data-testid={`job-posted-${job.id}`}>🕒 {formatPostedDate(job.posted_at)}</span>
                    </div>
                    <button
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    data-testid={`button-apply-${job.id}`}
                    >
                    Apply Now
                    </button>
                </div>
                </div>
            ))}
            </div>
        )}
      </div>
    </div>
  );
}