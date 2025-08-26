"use client";

import { useState } from 'react';

export default function Documentation() {
  const [activeSection, setActiveSection] = useState('overview');

  const sections = [
    { id: 'overview', title: 'Overview', icon: '📖' },
    { id: 'getting-started', title: 'Getting Started', icon: '🚀' },
    { id: 'ai-agents', title: 'AI Agents', icon: '🤖' },
    { id: 'blockchain', title: 'Blockchain Integration', icon: '⛓️' },
    { id: 'api', title: 'API Reference', icon: '🔧' },
    { id: 'faq', title: 'FAQ', icon: '❓' }
  ];

  const content = {
    overview: {
      title: 'CareerVerse Overview',
      content: `
        <h2>What is CareerVerse?</h2>
        <p>CareerVerse is a revolutionary decentralized autonomous job marketplace that leverages AI agents and blockchain technology to transform how employers and job seekers connect.</p>
        
        <h3>Key Features</h3>
        <ul>
          <li><strong>AI-Powered Matching:</strong> Fetch.ai agents automatically match candidates with opportunities</li>
          <li><strong>Decentralized Security:</strong> ICP blockchain ensures secure, private data storage</li>
          <li><strong>Autonomous Negotiation:</strong> AI agents handle salary and terms negotiations</li>
          <li><strong>Global Accessibility:</strong> Borderless job economy with worldwide opportunities</li>
        </ul>

        <h3>How It Works</h3>
        <ol>
          <li>Create your profile and define your preferences</li>
          <li>AI agents analyze your skills and market demand</li>
          <li>Automatic matching with relevant opportunities</li>
          <li>AI-assisted negotiations and contract finalization</li>
          <li>Secure payments through blockchain smart contracts</li>
        </ol>
      `
    },
    'getting-started': {
      title: 'Getting Started',
      content: `
        <h2>Quick Start Guide</h2>
        
        <h3>1. Create Your Account</h3>
        <p>Sign up using your email or connect your Web3 wallet for full decentralized experience.</p>
        
        <h3>2. Complete Your Profile</h3>
        <ul>
          <li>Add your skills and experience</li>
          <li>Upload portfolio and certifications</li>
          <li>Set your availability and preferences</li>
          <li>Define salary expectations and work arrangements</li>
        </ul>

        <h3>3. AI Agent Setup</h3>
        <p>Your personal AI agent will be configured based on your profile. This agent will:</p>
        <ul>
          <li>Search for opportunities 24/7</li>
          <li>Screen job postings for compatibility</li>
          <li>Handle initial communications with employers</li>
          <li>Negotiate terms on your behalf</li>
        </ul>

        <h3>4. Start Exploring</h3>
        <p>Visit the Job Board to see matched opportunities or use the AI Assistant for personalized guidance.</p>
      `
    },
    'ai-agents': {
      title: 'AI Agents',
      content: `
        <h2>Understanding AI Agents</h2>
        
        <h3>Fetch.ai Integration</h3>
        <p>CareerVerse uses Fetch.ai's autonomous economic agents (AEAs) to create a truly decentralized marketplace.</p>

        <h3>Agent Types</h3>
        <ul>
          <li><strong>Job Seeker Agents:</strong> Represent individuals looking for opportunities</li>
          <li><strong>Employer Agents:</strong> Represent companies posting job requirements</li>
          <li><strong>Matching Agents:</strong> Facilitate connections between seekers and employers</li>
          <li><strong>Negotiation Agents:</strong> Handle contract terms and compensation discussions</li>
        </ul>

        <h3>Agent Capabilities</h3>
        <ul>
          <li>24/7 autonomous operation</li>
          <li>Machine learning-based decision making</li>
          <li>Multi-party negotiations</li>
          <li>Reputation and trust management</li>
          <li>Cross-platform communication</li>
        </ul>

        <h3>Privacy & Control</h3>
        <p>You maintain full control over your agent's behavior through preference settings and approval mechanisms.</p>
      `
    },
    blockchain: {
      title: 'Blockchain Integration',
      content: `
        <h2>ICP Blockchain Features</h2>
        
        <h3>Data Security</h3>
        <p>All sensitive data is stored on the Internet Computer Protocol (ICP) blockchain, ensuring:</p>
        <ul>
          <li>Immutable employment records</li>
          <li>Encrypted personal information</li>
          <li>Verifiable credentials and certifications</li>
          <li>Tamper-proof reputation scores</li>
        </ul>

        <h3>Smart Contracts</h3>
        <p>Employment agreements are managed through smart contracts that provide:</p>
        <ul>
          <li>Automated milestone payments</li>
          <li>Escrow services for project-based work</li>
          <li>Dispute resolution mechanisms</li>
          <li>Performance-based releases</li>
        </ul>

        <h3>Decentralized Identity</h3>
        <p>Your professional identity is owned and controlled by you, portable across the entire Web3 ecosystem.</p>
      `
    },
    api: {
      title: 'API Reference',
      content: `
        <h2>API Documentation</h2>
        
        <h3>Authentication</h3>
        <pre><code>
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
        </code></pre>

        <h3>Job Endpoints</h3>
        <pre><code>
GET /api/jobs
GET /api/jobs/:id
POST /api/jobs (employer only)
PUT /api/jobs/:id (employer only)
DELETE /api/jobs/:id (employer only)
        </code></pre>

        <h3>Profile Endpoints</h3>
        <pre><code>
GET /api/profile
PUT /api/profile
POST /api/profile/skills
DELETE /api/profile/skills/:id
        </code></pre>

        <h3>Agent Endpoints</h3>
        <pre><code>
GET /api/agent/status
POST /api/agent/configure
GET /api/agent/matches
POST /api/agent/negotiate
        </code></pre>
      `
    },
    faq: {
      title: 'Frequently Asked Questions',
      content: `
        <h2>Common Questions</h2>
        
        <h3>Q: How do AI agents ensure fair matching?</h3>
        <p>A: Our agents use machine learning algorithms trained on successful hiring patterns, skills compatibility, and cultural fit indicators to ensure objective, bias-free matching.</p>

        <h3>Q: Is my data secure on the blockchain?</h3>
        <p>A: Yes, all sensitive data is encrypted before being stored on ICP. You maintain full control over who can access your information.</p>

        <h3>Q: How are payments handled?</h3>
        <p>A: Payments are managed through smart contracts with built-in escrow functionality, ensuring both parties are protected.</p>

        <h3>Q: Can I opt out of AI agent negotiations?</h3>
        <p>A: Absolutely. You can configure your agent's autonomy level or handle negotiations manually through the platform.</p>

        <h3>Q: What happens if there's a dispute?</h3>
        <p>A: Our decentralized dispute resolution system uses community arbitrators and smart contract mechanisms to resolve conflicts fairly.</p>

        <h3>Q: Are there fees for using CareerVerse?</h3>
        <p>A: Basic job searching is free. We charge a small percentage only on successful placements, significantly lower than traditional recruiting firms.</p>
      `
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4" data-testid="docs-title">
            Documentation
          </h1>
          <p className="text-xl text-gray-600">
            Complete guide to using CareerVerse's decentralized job marketplace
          </p>
        </div>

        <div className="grid lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <nav className="bg-white rounded-lg shadow-sm p-4 sticky top-8" data-testid="docs-navigation">
              <h3 className="font-semibold text-gray-900 mb-4">Contents</h3>
              <ul className="space-y-2">
                {sections.map((section) => (
                  <li key={section.id}>
                    <button
                      onClick={() => setActiveSection(section.id)}
                      className={`w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center space-x-2 ${
                        activeSection === section.id
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                      data-testid={`nav-${section.id}`}
                    >
                      <span>{section.icon}</span>
                      <span className="text-sm">{section.title}</span>
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
          </div>

          {/* Content Area */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm p-8" data-testid="docs-content">
              <h1 className="text-3xl font-bold text-gray-900 mb-6">
                {content[activeSection as keyof typeof content].title}
              </h1>
              <div 
                className="prose prose-blue max-w-none"
                dangerouslySetInnerHTML={{ 
                  __html: content[activeSection as keyof typeof content].content.replace(/\n/g, '<br>')
                }}
                data-testid="docs-content-body"
              />
            </div>

            {/* Next/Previous Navigation */}
            <div className="mt-8 flex justify-between">
              <button
                onClick={() => {
                  const currentIndex = sections.findIndex(s => s.id === activeSection);
                  if (currentIndex > 0) {
                    setActiveSection(sections[currentIndex - 1].id);
                  }
                }}
                disabled={sections.findIndex(s => s.id === activeSection) === 0}
                className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:text-blue-700 disabled:text-gray-400 disabled:cursor-not-allowed"
                data-testid="button-previous"
              >
                <span>← Previous</span>
              </button>
              
              <button
                onClick={() => {
                  const currentIndex = sections.findIndex(s => s.id === activeSection);
                  if (currentIndex < sections.length - 1) {
                    setActiveSection(sections[currentIndex + 1].id);
                  }
                }}
                disabled={sections.findIndex(s => s.id === activeSection) === sections.length - 1}
                className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:text-blue-700 disabled:text-gray-400 disabled:cursor-not-allowed"
                data-testid="button-next"
              >
                <span>Next →</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}