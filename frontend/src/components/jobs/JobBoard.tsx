"use client";

import { useState, useEffect, useRef, useCallback } from 'react';

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

// Interface for explorer agent jobs - now matches frontend structure exactly
interface ExplorerJob {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  jobDescription: string;  // Matches frontend
  jobRequirements: string[];  // Matches frontend
  salary: string;
  skills: string[];  // Matches frontend
  rating: number;  // Matches frontend
  postedDate: string;  // Matches frontend
  // Additional explorer fields
  source: string;
  scraped_at: string;
  application_url: string;
  original_url: string;  // Original job posting URL
  full_description: string;  // Complete job description
  job_type: string;
  experience_level: string;
  budget_min?: number;  // Budget range from chat
  budget_max?: number;  // Budget range from chat
  extracted_skills?: string[];
  job_category?: string;
  estimated_experience?: string;
}

interface JobBoardProps {
  chatContext?: {
    keywords?: string;
    location?: string;
    requiredSkills?: string[];
    experienceLevel?: string;
    jobType?: string;
    industry?: string;
  };
}

export default function JobBoard({ chatContext }: JobBoardProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showModal, setShowModal] = useState(false);
  const [showApplyForm, setShowApplyForm] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  
  // New state for explorer agent integration
  const [isSearching, setIsSearching] = useState(false);
  const [searchStatus, setSearchStatus] = useState('');
  const [explorerJobs, setExplorerJobs] = useState<ExplorerJob[]>([]);
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [showExplorerJobs, setShowExplorerJobs] = useState(false);
  const [filteringStats, setFilteringStats] = useState<{
    totalJobs: number;
    validJobs: number;
    filteredJobs: number;
    qualityRate: string;
  } | null>(null);
  const [hasChatbotRequirements, setHasChatbotRequirements] = useState(false);
  
  const websocketRef = useRef<WebSocket | null>(null);

  // Your existing static jobs
  const staticJobs: Job[] = [
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

  // Combine static jobs with explorer jobs
  const allJobs = showExplorerJobs ? [...staticJobs, ...explorerJobs] : staticJobs;

  const categories = [
    { value: 'all', label: 'All Jobs' },
    { value: 'frontend', label: 'Frontend' },
    { value: 'blockchain', label: 'Blockchain' },
    { value: 'ai', label: 'AI/ML' },
    { value: 'design', label: 'Design' }
  ];

  // Extract search parameters from chatbot conversation
  const extractSearchParamsFromChat = () => {
    // First, try to get requirements from localStorage (set by chatbot)
    const chatbotRequirements = localStorage.getItem('chatbotJobRequirements');
    
    if (chatbotRequirements) {
      try {
        const requirements = JSON.parse(chatbotRequirements);
        console.log('📋 Using job requirements from chatbot:', requirements);
        
        // Clear the requirements after using them
        localStorage.removeItem('chatbotJobRequirements');
        
        return {
          keywords: requirements.keywords || 'Software Developer',
          location: requirements.location || 'San Francisco',
          required_skills: requirements.required_skills || ['React', 'Python', 'AWS'],
          experience_level: requirements.experience_level || 'Mid-level',
          job_type: requirements.job_type || 'Full-time',
          industry: requirements.industry || 'Technology',
          remote_preference: requirements.remote_preference || '',
          budget_min: requirements.budget_min || null,
          budget_max: requirements.budget_max || null
        };
      } catch (error) {
        console.error('Error parsing chatbot requirements:', error);
      }
    }
    
    // Use chat context if provided, otherwise use defaults
    if (chatContext) {
      return {
        keywords: chatContext.keywords || 'Software Developer',
        location: chatContext.location || 'San Francisco',
        required_skills: chatContext.requiredSkills || ['React', 'Python', 'AWS'],
        experience_level: chatContext.experienceLevel || 'Mid-level',
        job_type: chatContext.jobType || 'Full-time',
        industry: chatContext.industry || 'Technology'
      };
    }
    
    // Default parameters if no chat context
    return {
      keywords: 'Software Developer',
      location: 'San Francisco',
      required_skills: ['React', 'Python', 'AWS'],
      experience_level: 'Mid-level',
      job_type: 'Full-time',
      industry: 'Technology'
    };
  };
  
  // Check if we should auto-start job search when component mounts
  useEffect(() => {
    // Only run on client side
    if (typeof window === 'undefined') return;
    
    const hasRequirements = localStorage.getItem('chatbotJobRequirements') !== null || chatContext;
    setHasChatbotRequirements(!!hasRequirements);
    
    if (hasRequirements && !isSearching) {
      // Small delay to ensure component is fully mounted
      const timer = setTimeout(() => {
        console.log('Auto-starting job search from chatbot...');
        startJobSearch();
      }, 500);
      
      return () => clearTimeout(timer);
    }
  }, [chatContext]); // Only run when chatContext changes
  
  // Cleanup effect
  useEffect(() => {
    return () => {
      // Reset state when component unmounts
      setHasChatbotRequirements(false);
    };
  }, []);

  // Start job search with explorer agent
  const startJobSearch = useCallback(async () => {
    setIsSearching(true);
    setSearchStatus('Connecting to Explorer Agent...');
    setExplorerJobs([]);
    setShowExplorerJobs(true);

    try {
      // Connect to explorer agent WebSocket
      const ws = new WebSocket('ws://localhost:8001/ws/jobs/stream');
      
      ws.onopen = () => {
        console.log('Connected to Explorer Agent');
        const searchParams = extractSearchParamsFromChat();
        let statusMessage = `Connected! Searching for ${searchParams.keywords} jobs in ${searchParams.location}`;
        
        // Add budget information if available
        if (searchParams.budget_min && searchParams.budget_max) {
          statusMessage += ` with budget $${searchParams.budget_min}-$${searchParams.budget_max}`;
        }
        
        // Add experience level if available
        if (searchParams.experience_level) {
          statusMessage += ` (${searchParams.experience_level} level)`;
        }
        
        statusMessage += '...';
        setSearchStatus(statusMessage);
        
        // Send search parameters based on chatbot conversation
        const websocketMessage = {
          command: 'start_search',
          search_params: searchParams
        };
        
        ws.send(JSON.stringify(websocketMessage));
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'job_data':
            // The explorer agent now sends data in the correct structure
            const newJob: ExplorerJob = data.data;
            console.log('Received job from explorer agent:', newJob);
            setExplorerJobs(prev => [...prev, newJob]);
            setSearchStatus(`Found ${explorerJobs.length + 1} jobs from ${newJob.source}...`);
            break;
          case 'status':
            setSearchStatus(data.message);
            break;
          case 'scraper_status':
            if (data.status === 'completed' && data.stats) {
              const stats = data.stats;
              setSearchStatus(
                `✅ ${data.scraper} completed: ${stats.valid_jobs} quality jobs found ` +
                `(${stats.filtered_jobs} filtered out, ${stats.quality_rate} pass rate)`
              );
              
              // Store filtering statistics
              setFilteringStats({
                totalJobs: stats.total_jobs,
                validJobs: stats.valid_jobs,
                filteredJobs: stats.filtered_jobs,
                qualityRate: stats.quality_rate
              });
            } else {
              setSearchStatus(`${data.scraper} ${data.status}...`);
            }
            break;
          case 'scraper_error':
            setSearchStatus(`Error with ${data.scraper}: ${data.error}`);
            break;
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setSearchStatus('Connection error. Please try again.');
        setIsSearching(false);
      };
      
      ws.onclose = () => {
        console.log('WebSocket connection closed');
        setSearchStatus('Search completed!');
        setIsSearching(false);
      };
      
      setWebsocket(ws);
      websocketRef.current = ws;
      
    } catch (error) {
      console.error('Failed to start job search:', error);
      setSearchStatus('Failed to start search. Please try again.');
      setIsSearching(false);
    }
  }, []); // Empty dependency array since this function doesn't depend on any props/state

  // Stop job search
  const stopJobSearch = () => {
    if (websocketRef.current) {
      websocketRef.current.close();
      setWebsocket(null);
      websocketRef.current = null;
    }
    setIsSearching(false);
    setSearchStatus('Search stopped.');
  };

  // Cleanup WebSocket on component unmount
  useEffect(() => {
    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  // Convert explorer job to your job format for display
  const convertExplorerJobToJob = (explorerJob: ExplorerJob): Job => {
    return {
      id: parseInt(explorerJob.id) || Math.floor(Math.random() * 10000),
      title: explorerJob.title,
      company: explorerJob.company,
      description: explorerJob.description,
      jobDescription: explorerJob.jobDescription,
      jobRequirements: explorerJob.jobRequirements,
      salary: explorerJob.salary,
      skills: explorerJob.skills,
      rating: explorerJob.rating,
      location: explorerJob.location,
      postedDate: explorerJob.postedDate
    };
  };

  const openModal = (job: Job) => {
    setSelectedJob(job);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedJob(null);
  };

  const openApplyForm = () => {
    setShowModal(false);
    setShowApplyForm(true);
  };

  const closeApplyForm = () => {
    setShowApplyForm(false);
    setSelectedJob(null);
  };

  // Helper function to safely open modal with proper type handling
  const handleJobClick = (job: Job | ExplorerJob, index: number) => {
    const isExplorerJob = index >= staticJobs.length;
    if (isExplorerJob) {
      const convertedJob = convertExplorerJobToJob(job as ExplorerJob);
      openModal(convertedJob);
    } else {
      openModal(job as Job);
    }
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

        {/* Explorer Agent Integration */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-sm p-6 mb-8 border border-blue-200">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-blue-900 mb-2">
                🚀 AI-Powered Job Discovery
              </h3>
              <p className="text-blue-700 text-sm">
                Use our Explorer Agent to find real-time job listings from LinkedIn, Indeed, Glassdoor, and more
              </p>
              
              {/* Auto-start notification */}
              {hasChatbotRequirements && !isSearching && (
                <div className="mt-2 p-2 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-green-700 text-sm font-medium">
                    🎯 Job search will start automatically based on your chatbot conversation!
                  </p>
                </div>
              )}
              {searchStatus && (
                <p className="text-blue-600 text-sm mt-2 font-medium">
                  {searchStatus}
                </p>
              )}
              
              {/* Filtering Statistics */}
              {filteringStats && (
                <div className="mt-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="text-sm font-semibold text-blue-800 mb-2">🔍 Quality Filter Results</h4>
                  <div className="grid grid-cols-2 gap-4 text-xs">
                    <div>
                      <span className="text-blue-600 font-medium">Total Scraped:</span>
                      <span className="ml-2 text-blue-800">{filteringStats.totalJobs}</span>
                    </div>
                    <div>
                      <span className="text-green-600 font-medium">Quality Jobs:</span>
                      <span className="ml-2 text-green-800">{filteringStats.validJobs}</span>
                    </div>
                    <div>
                      <span className="text-orange-600 font-medium">Filtered Out:</span>
                      <span className="ml-2 text-orange-800">{filteringStats.filteredJobs}</span>
                    </div>
                    <div>
                      <span className="text-purple-600 font-medium">Pass Rate:</span>
                      <span className="ml-2 text-purple-800">{filteringStats.qualityRate}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="flex gap-3">
              {!isSearching ? (
                <button
                  onClick={startJobSearch}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-all duration-200 font-medium shadow-sm"
                >
                  🔍 Find Jobs
                </button>
              ) : (
                <button
                  onClick={stopJobSearch}
                  className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-all duration-200 font-medium shadow-sm"
                >
                  ⏹️ Stop Search
                </button>
              )}
              
              {/* Show auto-start indicator when coming from chatbot */}
              {hasChatbotRequirements && !isSearching && (
                <div className="text-blue-600 text-sm font-medium flex items-center">
                  🚀 Auto-starting from chatbot...
                </div>
              )}
              {explorerJobs.length > 0 && (
                <button
                  onClick={() => setShowExplorerJobs(!showExplorerJobs)}
                  className={`px-4 py-2 rounded-lg font-medium shadow-sm transition-all duration-200 ${
                    showExplorerJobs 
                      ? 'bg-green-600 text-white hover:bg-green-700' 
                      : 'bg-gray-600 text-white hover:bg-gray-700'
                  }`}
                >
                  {showExplorerJobs ? 'Hide' : 'Show'} Explorer Jobs ({explorerJobs.length})
                </button>
              )}
            </div>
          </div>
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
          {allJobs.map((job, index) => {
            // Check if this is an explorer job
            const isExplorerJob = index >= staticJobs.length;
            const displayJob = isExplorerJob ? convertExplorerJobToJob(job as ExplorerJob) : job;
            
            return (
              <div 
                key={job.id} 
                className={`bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-all duration-200 border border-gray-100 flex flex-col h-full cursor-pointer ${
                  isExplorerJob ? 'border-l-4 border-l-blue-500' : ''
                }`} 
                data-testid={`job-card-${job.id}`} 
                onClick={() => handleJobClick(job, index)}
              >
                {/* Explorer Job Badge */}
                {isExplorerJob && (
                  <div className="mb-3">
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      🌐 {(job as ExplorerJob).source}
                    </span>
                  </div>
                )}
                
                {/* Header Section */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2" data-testid={`job-title-${job.id}`}>
                      {displayJob.title}
                    </h3>
                    <p className="text-blue-600 font-medium text-sm" data-testid={`job-company-${job.id}`}>
                      {displayJob.company}
                    </p>
                  </div>
                  <div className="flex items-center space-x-1 ml-2">
                    <span className="text-yellow-500 text-sm">⭐</span>
                    <span className="text-gray-700 font-medium text-sm" data-testid={`job-rating-${job.id}`}>
                      {displayJob.rating}
                    </span>
                  </div>
                </div>

                {/* Description Section */}
                <div className="mb-4 flex-grow">
                  <p className="text-gray-600 text-sm line-clamp-3" data-testid={`job-description-${job.id}`}>
                    {displayJob.description}
                  </p>
                  
                  {/* Show full description for explorer jobs */}
                  {isExplorerJob && (job as ExplorerJob).full_description && (
                    <div className="mt-2">
                      <details className="group">
                        <summary className="cursor-pointer text-blue-600 text-xs hover:text-blue-800 font-medium">
                          📖 Read full description
                        </summary>
                        <div className="mt-2 p-3 bg-gray-50 rounded text-xs text-gray-700 max-h-32 overflow-y-auto">
                          {(job as ExplorerJob).full_description}
                        </div>
                      </details>
                    </div>
                  )}
                </div>

                {/* Skills Section */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {displayJob.skills.slice(0, 3).map((skill, skillIndex) => (
                    <span
                      key={skillIndex}
                      className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium"
                      data-testid={`job-skill-${job.id}-${skillIndex}`}
                    >
                      {skill}
                    </span>
                  ))}
                  {displayJob.skills.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded-full text-xs">
                      +{displayJob.skills.length - 3} more
                    </span>
                  )}
                </div>

                {/* Footer Section - Job Details */}
                <div className="mt-auto space-y-3">
                  <div className="flex flex-col space-y-2 text-xs text-gray-600">
                    <div className="flex items-center space-x-2">
                      <span>💰</span>
                      <span data-testid={`job-salary-${job.id}`}>{displayJob.salary}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span>📍</span>
                      <span data-testid={`job-location-${job.id}`}>{displayJob.location}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span>🕒</span>
                      <span data-testid={`job-posted-${job.id}`}>{displayJob.postedDate}</span>
                    </div>
                  </div>
                  
                  {/* View Original Button for Explorer Jobs */}
                  {isExplorerJob && (job as ExplorerJob).original_url && (
                    <div className="pt-2 border-t border-gray-100">
                      <a
                        href={(job as ExplorerJob).original_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center justify-center w-full px-3 py-2 text-xs font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 hover:text-blue-700 transition-colors"
                      >
                        🌐 View Original on {(job as ExplorerJob).source}
                      </a>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* No Jobs Message */}
        {allJobs.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No jobs found. Try adjusting your search or use the Explorer Agent to find more opportunities.</p>
          </div>
        )}
      </div>

      {/* Job Detail Modal */}
      {showModal && selectedJob && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center z-50" onClick={closeModal}>
          <div className="relative p-8 bg-white w-full max-w-2xl mx-auto rounded-lg shadow-lg" onClick={(e) => e.stopPropagation()}>
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
              className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-all duration-200 text-sm font-medium shadow-sm"
              onClick={openApplyForm}
            >
              Apply Now
            </button>
          </div>
        </div>
      )}

      {/* Application Form Modal */}
      {showApplyForm && selectedJob && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex justify-center items-center z-50" onClick={closeApplyForm}>
          <div className="relative p-8 bg-white w-full max-w-lg mx-auto rounded-lg shadow-lg" onClick={(e) => e.stopPropagation()}>
            <button
              className="absolute top-3 right-3 text-gray-500 hover:text-gray-800 text-2xl"
              onClick={closeApplyForm}
            >
              &times;
            </button>
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-bold text-gray-900">{selectedJob.title}</h2>
              <p className="text-blue-600 font-medium">{selectedJob.company}</p>
            </div>
            <form>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="relative">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3">👤</span>
                  <input type="text" placeholder="First Name" className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                </div>
                <div className="relative">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3">👤</span>
                  <input type="text" placeholder="Last Name" className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                </div>
              </div>
              <div className="relative mb-4">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">✉️</span>
                <input type="email" placeholder="Email Address" className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
              </div>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="relative col-span-1">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3">📞</span>
                  <input type="text" placeholder="+62" className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                </div>
                <div className="relative col-span-2">
                  <input type="text" placeholder="Phone Number" className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
                </div>
              </div>
              <div className="relative mb-4">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">🔒</span>
                <input type="password" placeholder="Password" className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500" />
              </div>
              <div className="relative mb-6">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3">📄</span>
                <input type="file" className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg" />
              </div>
              <button
                type="submit"
                className="w-full bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-all duration-200 text-sm font-medium shadow-sm"
              >
                Sign Up and Apply
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
