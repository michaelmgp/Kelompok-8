"use client";

import { useState } from 'react';

interface Job {
  id: number;
  title: string;
  company: string;
  description: string;
  jobDescription: string;
  jobRequirements: string[];
  salary: string;
  skills: string[];
  rating: number;
  location: string;
  postedDate: string;
}

export default function JobBoard() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  const jobs: Job[] = [
    {
      id: 1,
      title: "Senior Frontend Developer",
      company: "TechCorp AI",
      description: "Build next-generation decentralized applications using React and Web3 technologies.",
      jobDescription: "We are looking for a Senior Frontend Developer to join our team. You will be responsible for building the user interface of our decentralized applications. You will work with a team of engineers to design and build a high-quality product.",
      jobRequirements: [
        "5+ years of experience in frontend development",
        "Experience with React, TypeScript, and Web3",
        "Experience with Solidity is a plus",
        "Strong understanding of blockchain technology"
      ],
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
      jobDescription: "We are looking for a Blockchain Engineer to join our team. You will be responsible for designing and implementing smart contracts for our decentralized finance applications. You will work with a team of engineers to design and build a high-quality product.",
      jobRequirements: [
        "3+ years of experience in blockchain development",
        "Experience with Solidity, Rust, and ICP",
        "Experience with smart contract development and auditing",
        "Strong understanding of decentralized finance"
      ],
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
      jobDescription: "We are looking for an AI/ML Research Scientist to join our team. You will be responsible for researching and developing autonomous agents for our decentralized marketplaces. You will work with a team of researchers and engineers to design and build a high-quality product.",
      jobRequirements: [
        "PhD in Computer Science or related field",
        "Experience with Python, TensorFlow, and multi-agent systems",
        "Experience with Fetch.ai is a plus",
        "Strong understanding of artificial intelligence and machine learning"
      ],
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
      jobDescription: "We are looking for a Product Designer to join our team. You will be responsible for designing intuitive interfaces for our decentralized applications and blockchain tools. You will work with a team of designers and engineers to design and build a high-quality product.",
      jobRequirements: [
        "3+ years of experience in product design",
        "Experience with Figma, UI/UX, and design systems",
        "Experience with Web3 is a plus",
        "Strong understanding of user-centered design principles"
      ],
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

  const openModal = (job: Job) => {
    setSelectedJob(job);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedJob(null);
  };

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
            <div key={job.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-all duration-200 border border-gray-100 flex flex-col h-full" data-testid={`job-card-${job.id}`}>
              {/* Header Section */}
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

              {/* Description Section */}
              <p className="text-gray-600 mb-4 text-sm line-clamp-3 flex-grow" data-testid={`job-description-${job.id}`}>
                {job.description}
              </p>

              {/* Skills Section */}
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

              {/* Footer Section - Job Details and Apply Button */}
              <div className="mt-auto space-y-3">
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
                
                {/* Apply Button - Centered and Symmetrical */}
                <div className="pt-2">
                  <button 
                    className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-all duration-200 text-sm font-medium shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
                    data-testid={`button-apply-${job.id}`}
                    onClick={() => openModal(job)}
                  >
                    Apply Now
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Job Detail Modal */}
      {showModal && selectedJob && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center z-50">
          <div className="relative p-8 bg-white w-full max-w-2xl mx-auto rounded-lg shadow-lg">
            <button
              className="absolute top-3 right-3 text-gray-500 hover:text-gray-800 text-2xl"
              onClick={closeModal}
            >
              &times;
            </button>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">{selectedJob.title}</h2>
            <p className="text-blue-600 font-medium mb-2">{selectedJob.company}</p>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Job Description:</h3>
              <p className="text-gray-700 mb-4">{selectedJob.jobDescription}</p>
            </div>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Job Requirements:</h3>
              <ul className="list-disc list-inside text-gray-700">
                {selectedJob.jobRequirements.map((requirement, index) => (
                  <li key={index}>{requirement}</li>
                ))}
              </ul>
            </div>
            <div className="mb-4">
              <p className="text-gray-600"><strong>Salary:</strong> {selectedJob.salary}</p>
              <p className="text-gray-600"><strong>Location:</strong> {selectedJob.location}</p>
              <p className="text-gray-600"><strong>Posted:</strong> {selectedJob.postedDate}</p>
              <p className="text-gray-600"><strong>Rating:</strong> {selectedJob.rating} ⭐</p>
            </div>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Skills:</h3>
              <div className="flex flex-wrap gap-2">
                {selectedJob.skills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <button
              className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-all duration-200 text-sm font-medium shadow-sm"
              onClick={() => {
                alert(`Applying for ${selectedJob.title} at ${selectedJob.company}!`);
                closeModal();
              }}
            >
              Proceed to Apply
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
