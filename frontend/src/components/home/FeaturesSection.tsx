"use client";

export default function FeaturesSection() {
  const features = [
    {
      icon: "🤖",
      title: "AI-Powered Matching",
      description: "Fetch.ai agents automatically match job seekers with perfect opportunities based on skills and culture fit."
    },
    {
      icon: "🔒",
      title: "Secure & Decentralized",
      description: "ICP blockchain ensures secure, private, and verifiable employment data and smart contracts."
    },
    {
      icon: "⚡",
      title: "Fast & Efficient",
      description: "Autonomous agents handle negotiations and matching, making hiring 10x faster than traditional methods."
    },
    {
      icon: "🌍",
      title: "Borderless Economy",
      description: "Connect with opportunities worldwide in a transparent, efficient job economy without borders."
    }
  ];

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4" data-testid="features-title">
            Revolutionary Job Matching
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Experience the future of hiring with AI agents and blockchain technology
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="text-center p-6 rounded-lg hover:shadow-lg transition-shadow" data-testid={`feature-card-${index}`}>
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}