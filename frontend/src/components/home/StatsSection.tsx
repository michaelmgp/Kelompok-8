"use client";

export default function StatsSection() {
  const stats = [
    { number: "10,000+", label: "Active AI Agents" },
    { number: "5,000+", label: "Job Matches" },
    { number: "98%", label: "Success Rate" },
    { number: "24/7", label: "Autonomous Matching" }
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4" data-testid="stats-title">
            Platform Performance
          </h2>
          <p className="text-xl text-gray-600">
            See how our decentralized marketplace is transforming hiring
          </p>
        </div>
        
        <div className="grid md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center" data-testid={`stat-${index}`}>
              <div className="text-4xl font-bold text-blue-600 mb-2">{stat.number}</div>
              <div className="text-lg text-gray-700">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}