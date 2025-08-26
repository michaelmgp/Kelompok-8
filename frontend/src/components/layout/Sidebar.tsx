"use client";

import { useState } from "react";

export default function Sidebar() {
  const [expandedFolders, setExpandedFolders] = useState<{ [key: string]: boolean }>({
    frontend: true,
    src: true,
  });

  const toggleFolder = (folderName: string) => {
    setExpandedFolders((prev) => ({
      ...prev,
      [folderName]: !prev[folderName],
    }));
  };

  return (
    <aside className="w-64 bg-white border-r border-gray-200 fixed h-full overflow-y-auto" data-testid="sidebar">
      <div className="p-6">
        {/* Project Info */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-black mb-2">Frontend Project</h2>
          <p className="text-sm text-gray-600">Next.js 14 App Router</p>
        </div>

        {/* File Explorer */}
        <div className="space-y-1">
          <div className="flex items-center text-sm font-medium text-gray-900 mb-3">
            <i className="fas fa-folder text-career-blue mr-2"></i>
            Project Structure
          </div>

          {/* Frontend Folder (Expanded) */}
          <div className="ml-2">
            <div
              className="flex items-center py-1 px-2 text-sm text-black bg-career-blue-light rounded hover:bg-blue-100 cursor-pointer"
              onClick={() => toggleFolder("frontend")}
              data-testid="folder-frontend"
            >
              <i className={`fas ${expandedFolders.frontend ? 'fa-folder-open' : 'fa-folder'} text-career-blue mr-2`}></i>
              <span className="font-medium">frontend/</span>
            </div>

            {/* Nested Structure */}
            {expandedFolders.frontend && (
              <div className="ml-4 mt-1 space-y-1">
                <div
                  className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer"
                  onClick={() => toggleFolder("src")}
                  data-testid="folder-src"
                >
                  <i className={`fas ${expandedFolders.src ? 'fa-folder-open' : 'fa-folder'} text-yellow-500 mr-2`}></i>
                  <span>src/</span>
                </div>

                {expandedFolders.src && (
                  <div className="ml-4 space-y-1">
                    <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="folder-app">
                      <i className="fas fa-folder text-yellow-500 mr-2"></i>
                      <span>app/</span>
                    </div>
                    <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="folder-components">
                      <i className="fas fa-folder text-yellow-500 mr-2"></i>
                      <span>components/</span>
                    </div>
                    <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="folder-lib">
                      <i className="fas fa-folder text-yellow-500 mr-2"></i>
                      <span>lib/</span>
                    </div>
                    <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="folder-styles">
                      <i className="fas fa-folder text-yellow-500 mr-2"></i>
                      <span>styles/</span>
                    </div>
                  </div>
                )}

                <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="folder-public">
                  <i className="fas fa-folder text-yellow-500 mr-2"></i>
                  <span>public/</span>
                </div>

                <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="file-package">
                  <i className="fas fa-file-code text-green-500 mr-2"></i>
                  <span>package.json</span>
                </div>

                <div className="flex items-center py-1 px-2 text-sm text-gray-700 hover:bg-gray-100 rounded cursor-pointer" data-testid="file-nextconfig">
                  <i className="fas fa-file-code text-blue-500 mr-2"></i>
                  <span>next.config.js</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8">
          <h3 className="text-sm font-medium text-gray-900 mb-3">Quick Actions</h3>
          <div className="space-y-2">
            <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded flex items-center" data-testid="button-new-file">
              <i className="fas fa-plus mr-2"></i>
              New File
            </button>
            <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded flex items-center" data-testid="button-new-folder">
              <i className="fas fa-folder-plus mr-2"></i>
              New Folder
            </button>
            <button className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded flex items-center" data-testid="button-git-commit">
              <i className="fas fa-code-branch mr-2"></i>
              Git Commit
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
}