"use client";

import { useState } from 'react';

export default function JobBoard() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const jobs = [
    {
      id: 1,
      title: "Senior Frontend Developer",
      company: "TechCorp AI",
      description: "Build next-generation decentralized applications using React and Web3 technologies.",
      salary: "$120,000 - $180,000",
      skills: ["React", "TypeScript", "Web3", "Solidity"],
      rating: 4.8,
      location: "Remote",
      postedDate: "2 days ago"
    },
    {
      id: 2,
      title: "Blockchain Engineer",
      company: "DeFi Solutions",
      description: "Design and implement smart contracts for decentralized finance applications.",
      salary: "$140,000 - $200,000", 
      skills: ["Solidity", "Rust", "ICP", "Smart Contracts"],
      rating: 4.9,
      location: "San Francisco, CA",
      postedDate: "1 day ago"
    },
    {
      id: 3,
      title: "AI/ML Research Scientist",
      company: "Fetch.ai Labs",
      description: "Research and develop autonomous agents for decentralized marketplaces.",
      salary: "$160,000 - $220,000",
      skills: ["Python", "TensorFlow", "Multi-Agent Systems", "Fetch.ai"],
      rating: 4.7,
      location: "Cambridge, UK",
      postedDate: "3 days ago"
    },
    {
      id: 4,
      title: "Product Designer",
      company: "Web3 Studios",
      description: "Design intuitive interfaces for decentralized applications and blockchain tools.",
      salary: "$90,000 - $130,000",
      skills: ["Figma", "UI/UX", "Web3", "Design Systems"],
      rating: 4.6,
      location: "Remote",
      postedDate: "1 week ago"
    }
  ];

  const categories = [
    { value: 'all', label: 'All Jobs' },
    { value: 'frontend', label: 'Frontend' },
    { value: 'blockchain', label: 'Blockchain' },
    { value: 'ai', label: 'AI/ML' },
    { value: 'design', label: 'Design' }
  ];

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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <div key={job.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow border border-gray-100" data-testid={`job-card-${job.id}`}>
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2" data-testid={`job-title-${job.id}`}>
                    {job.title}
                  </h3>
                  <p className="text-blue-600 font-medium text-sm" data-testid={`job-company-${job.id}`}>
                    {job.company}
                  </p>
                </div>
                <div className="flex items-center space-x-1 ml-2">
                  <span className="text-yellow-500 text-sm">⭐</span>
                  <span className="text-gray-700 font-medium text-sm" data-testid={`job-rating-${job.id}`}>
                    {job.rating}
                  </span>
                </div>
              </div>

              <p className="text-gray-600 mb-4 text-sm line-clamp-3" data-testid={`job-description-${job.id}`}>
                {job.description}
              </p>

              <div className="flex flex-wrap gap-2 mb-4">
                {job.skills.slice(0, 3).map((skill, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium"
                    data-testid={`job-skill-${job.id}-${index}`}
                  >
                    {skill}
                  </span>
                ))}
                {job.skills.length > 3 && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                    +{job.skills.length - 3} more
                  </span>
                )}
              </div>

              <div className="space-y-3">
                <div className="flex flex-col space-y-2 text-xs text-gray-600">
                  <div className="flex items-center space-x-2">
                    <span>💰</span>
                    <span data-testid={`job-salary-${job.id}`}>{job.salary}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span>📍</span>
                    <span data-testid={`job-location-${job.id}`}>{job.location}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span>🕒</span>
                    <span data-testid={`job-posted-${job.id}`}>{job.postedDate}</span>
                  </div>
                </div>
                <button 
                  className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                  data-testid={`button-apply-${job.id}`}
                >
                  Apply Now
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}