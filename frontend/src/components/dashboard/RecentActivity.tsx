import { Card } from "@/components/ui/card";

export default function RecentActivity() {
  const recentFiles = [
    {
      name: "components/Dashboard.tsx",
      time: "Modified 1h ago",
      icon: "fas fa-file-code",
      iconColor: "text-blue-500"
    },
    {
      name: "app/page.tsx",
      time: "Modified 3h ago",
      icon: "fas fa-file-code",
      iconColor: "text-green-500"
    },
    {
      name: "styles/globals.css",
      time: "Modified 5h ago",
      icon: "fas fa-file-alt",
      iconColor: "text-yellow-500"
    }
  ];

  const devTools = [
    {
      title: "Terminal",
      description: "Open integrated terminal",
      icon: "fas fa-terminal",
      iconColor: "text-career-blue",
      status: null,
      testId: "tool-terminal"
    },
    {
      title: "Git Status",
      description: "3 files changed",
      icon: "fas fa-code-branch",
      iconColor: "text-green-600",
      status: null,
      testId: "tool-git"
    },
    {
      title: "Dev Server",
      description: "localhost:3000",
      icon: "fas fa-server",
      iconColor: "text-purple-600",
      status: "Running",
      testId: "tool-server"
    }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6" data-testid="recent-activity">
      {/* Recent Files */}
      <Card className="bg-white rounded-xl border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-black">Recent Files</h2>
        </div>
        <div className="p-6">
          {recentFiles.map((file, index) => (
            <div
              key={index}
              className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer"
              data-testid={`recent-file-${index}`}
            >
              <i className={`${file.icon} ${file.iconColor}`}></i>
              <div className="flex-1">
                <p className="text-sm font-medium text-black">{file.name}</p>
                <p className="text-xs text-gray-500">{file.time}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Development Tools */}
      <Card className="bg-white rounded-xl border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-black">Development Tools</h2>
        </div>
        <div className="p-6 space-y-4">
          {devTools.map((tool, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-career-gray rounded-lg"
              data-testid={tool.testId}
            >
              <div className="flex items-center space-x-3">
                <i className={`${tool.icon} ${tool.iconColor}`}></i>
                <div>
                  <p className="text-sm font-medium text-black">{tool.title}</p>
                  <p className="text-xs text-gray-500">{tool.description}</p>
                </div>
              </div>
              {tool.status ? (
                <div className="flex space-x-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                  <span className="text-xs text-green-600 font-medium">{tool.status}</span>
                </div>
              ) : (
                <button className={`${tool.iconColor} hover:opacity-70`} data-testid={`button-${tool.testId}`}>
                  <i className="fas fa-external-link-alt"></i>
                </button>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
