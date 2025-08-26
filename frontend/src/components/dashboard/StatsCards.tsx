import { Card } from "@/components/ui/card";

export default function StatsCards() {
  const stats = [
    {
      title: "Total Files",
      value: "247",
      icon: "fas fa-file-code",
      bgColor: "bg-career-blue-light",
      iconColor: "text-career-blue",
      testId: "stat-files"
    },
    {
      title: "Components",
      value: "42",
      icon: "fas fa-puzzle-piece",
      bgColor: "bg-green-100",
      iconColor: "text-green-600",
      testId: "stat-components"
    },
    {
      title: "Last Deploy",
      value: "2h ago",
      icon: "fas fa-rocket",
      bgColor: "bg-purple-100",
      iconColor: "text-purple-600",
      testId: "stat-deploy"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8" data-testid="stats-cards">
      {stats.map((stat, index) => (
        <Card
          key={index}
          className="bg-white rounded-xl p-6 border border-gray-200 hover:shadow-lg transition-shadow"
          data-testid={stat.testId}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{stat.title}</p>
              <p className="text-2xl font-bold text-black">{stat.value}</p>
            </div>
            <div className={`w-12 h-12 ${stat.bgColor} rounded-lg flex items-center justify-center`}>
              <i className={`${stat.icon} ${stat.iconColor} text-xl`}></i>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
