"use client";

import { useState } from 'react';

export default function Analytics() {
  const [timeRange, setTimeRange] = useState('30d');

  const stats = {
    totalEarnings: '$45,750',
    jobsCompleted: 23,
    avgRating: 4.8,
    profileViews: 1250
  };

  const monthlyData = [
    { month: 'Jan', earnings: 3200, jobs: 2, rating: 4.6 },
    { month: 'Feb', earnings: 4100, jobs: 3, rating: 4.7 },
    { month: 'Mar', earnings: 5200, jobs: 4, rating: 4.8 },
    { month: 'Apr', earnings: 3800, jobs: 2, rating: 4.9 },
    { month: 'May', earnings: 6100, jobs: 5, rating: 4.8 },
    { month: 'Jun', earnings: 7300, jobs: 4, rating: 4.9 },
    { month: 'Jul', earnings: 8200, jobs: 6, rating: 4.8 },
    { month: 'Aug', earnings: 7800, jobs: 3, rating: 4.7 }
  ];

  const skills = [
    { name: 'React', demand: 92, growth: '+15%' },
    { name: 'Blockchain', demand: 88, growth: '+25%' },
    { name: 'AI/ML', demand: 85, growth: '+30%' },
    { name: 'TypeScript', demand: 78, growth: '+12%' },
    { name: 'Solidity', demand: 75, growth: '+40%' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4" data-testid="analytics-title">
            Performance Analytics
          </h1>
          <p className="text-xl text-gray-600">
            Track your performance and earnings over time in the decentralized marketplace
          </p>
        </div>

        {/* Time Range Selector */}
        <div className="mb-6">
          <div className="flex space-x-2">
            {['7d', '30d', '90d', '1y'].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  timeRange === range
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
                data-testid={`time-range-${range}`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm p-6" data-testid="stat-earnings">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Earnings</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalEarnings}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-green-600 text-xl">💰</span>
              </div>
            </div>
            <p className="text-sm text-green-600 mt-2">+18% from last month</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6" data-testid="stat-jobs">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Jobs Completed</p>
                <p className="text-2xl font-bold text-gray-900">{stats.jobsCompleted}</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-blue-600 text-xl">✅</span>
              </div>
            </div>
            <p className="text-sm text-blue-600 mt-2">+3 this month</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6" data-testid="stat-rating">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Average Rating</p>
                <p className="text-2xl font-bold text-gray-900">{stats.avgRating}</p>
              </div>
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <span className="text-yellow-600 text-xl">⭐</span>
              </div>
            </div>
            <p className="text-sm text-yellow-600 mt-2">+0.2 improvement</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6" data-testid="stat-views">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Profile Views</p>
                <p className="text-2xl font-bold text-gray-900">{stats.profileViews}</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-purple-600 text-xl">👁️</span>
              </div>
            </div>
            <p className="text-sm text-purple-600 mt-2">+25% visibility</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Earnings Chart */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4" data-testid="earnings-chart-title">
              Monthly Earnings
            </h3>
            <div className="space-y-3">
              {monthlyData.map((data, index) => (
                <div key={data.month} className="flex items-center justify-between" data-testid={`earnings-bar-${index}`}>
                  <span className="text-sm text-gray-600 w-8">{data.month}</span>
                  <div className="flex-1 mx-4">
                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${(data.earnings / 8500) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-sm font-medium text-gray-900 w-16">${data.earnings}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Jobs Completed Chart */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4" data-testid="jobs-chart-title">
              Jobs Completed
            </h3>
            <div className="space-y-3">
              {monthlyData.map((data, index) => (
                <div key={data.month} className="flex items-center justify-between" data-testid={`jobs-bar-${index}`}>
                  <span className="text-sm text-gray-600 w-8">{data.month}</span>
                  <div className="flex-1 mx-4">
                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-600 h-2 rounded-full"
                        style={{ width: `${(data.jobs / 6) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-sm font-medium text-gray-900 w-8">{data.jobs}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Skills Demand */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4" data-testid="skills-demand-title">
            Skills Market Demand
          </h3>
          <div className="space-y-4">
            {skills.map((skill, index) => (
              <div key={skill.name} className="flex items-center justify-between" data-testid={`skill-demand-${index}`}>
                <div className="flex items-center space-x-4 flex-1">
                  <span className="text-sm font-medium text-gray-900 w-20">{skill.name}</span>
                  <div className="flex-1">
                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${skill.demand}%` }}
                      ></div>
                    </div>
                  </div>
                  <span className="text-sm text-gray-600 w-8">{skill.demand}%</span>
                </div>
                <span className="text-sm font-medium text-green-600 ml-4">{skill.growth}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}