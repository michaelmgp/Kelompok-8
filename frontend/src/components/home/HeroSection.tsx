"use client";

export default function HeroSection() {
  return (
    <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6" data-testid="hero-title">
            Decentralized Autonomous
            <span className="text-blue-600"> Job Marketplace</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto" data-testid="hero-description">
            A platform where AI agents represent job seekers and employers, autonomously matching candidates 
            to job openings based on skills, experience, and cultural fit, leveraging Fetch.ai for agent 
            interactions and ICP for secure, decentralized data storage.
          </p>
          <div className="flex justify-center space-x-4">
            <button className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors" data-testid="button-get-started">
              Get Started
            </button>
            <button className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors" data-testid="button-learn-more">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}