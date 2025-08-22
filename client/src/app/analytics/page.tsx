'use client';

import { DollarSign, Target, Briefcase } from 'lucide-react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useState } from 'react';

// --- Implementasi Data Dummy ---
const dummyChartData = [
  { name: 'Jan', earnings: 4000, projects: 3 },
  { name: 'Feb', earnings: 3000, projects: 5 },
  { name: 'Mar', earnings: 5000, projects: 4 },
  { name: 'Apr', earnings: 4500, projects: 6 },
  { name: 'May', earnings: 6000, projects: 7 },
  { name: 'Jun', earnings: 5500, projects: 8 },
  { name: 'Jul', earnings: 7000, projects: 9 },
  { name: 'Aug', earnings: 6500, projects: 7 },
  { name: 'Sep', earnings: 7500, projects: 10 },
  { name: 'Oct', earnings: 8000, projects: 11 },
  { name: 'Nov', earnings: 7800, projects: 9 },
  { name: 'Dec', earnings: 9000, projects: 12 },
];

const dummySummaryData = {
  totalEarnings: 73800,
  earningsChange: '+22.5%',
  successRate: '95.8%',
  rateChange: '+1.3%',
  activeProjects: 12,
  projectsChange: '+4 from last half'
};
// --- Akhir Implementasi Data Dummy ---

export default function AnalyticsPage() {
  const [chartData, setChartData] = useState(dummyChartData);
  const [summaryData, setSummaryData] = useState(dummySummaryData);

  // --- Implementasi REST API (di-comment) ---
  /*
  useEffect(() => {
    const fetchData = async () => {
      try {
        const chartResponse = await fetch('http://localhost:5000/api/analytics/chart-data');
        const newChartData = await chartResponse.json();
        setChartData(newChartData);

        const summaryResponse = await fetch('http://localhost:5000/api/analytics/summary');
        const newSummaryData = await summaryResponse.json();
        setSummaryData(newSummaryData);

      } catch (error) {
        console.error('Gagal mengambil data analytics:', error);
      }
    };

    fetchData();
  }, []);
  */
  // --- Akhir Implementasi REST API ---

  return (
    <div className="space-y-8">
      {/* Analytics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-100">Total Earnings</h3>
            <DollarSign className="w-6 h-6 text-green-400" />
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-100">${summaryData.totalEarnings.toLocaleString()}</p>
            <p className="text-sm text-green-400 mt-1">{summaryData.earningsChange}</p>
          </div>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-100">Success Rate</h3>
            <Target className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-100">{summaryData.successRate}</p>
            <p className="text-sm text-blue-400 mt-1">{summaryData.rateChange}</p>
          </div>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-100">Active Projects</h3>
            <Briefcase className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <p className="text-3xl font-bold text-gray-100">{summaryData.activeProjects}</p>
            <p className="text-sm text-purple-400 mt-1">{summaryData.projectsChange}</p>
          </div>
        </motion.div>
      </div>
      
      {/* Chart Section */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-gray-100 mb-6">Performance Overview (12 Months)</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.2} />
              <XAxis dataKey="name" stroke="#9ca3af" />
              
              {/* Sumbu Y Kiri untuk Earnings */}
              <YAxis 
                yAxisId="left" 
                orientation="left" 
                stroke="#4ade80"
                tickFormatter={(value) => `$${Number(value) / 1000}k`}
              />
              
              {/* Sumbu Y Kanan untuk Projects */}
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                stroke="#8b5cf6"
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(31, 41, 55, 0.8)',
                  borderColor: 'rgba(255, 255, 255, 0.2)',
                  borderRadius: '0.75rem',
                  color: '#e5e7eb',
                }}
                formatter={(value, name) => {
                  if (name === 'Earnings') {
                    return [`$${value.toLocaleString()}`, name];
                  }
                  return [value, name];
                }}
              />
              <Legend wrapperStyle={{ color: '#e5e7eb' }} />
              <Bar yAxisId="left" dataKey="earnings" fill="#4ade80" name="Earnings" />
              <Bar yAxisId="right" dataKey="projects" fill="#8b5cf6" name="Projects" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    </div>
  );
}
