import TopNavigation from "@/components/layout/TopNavigation";

export default function DemoPage() {
  return (
    <>
      <TopNavigation />
      <div className="pt-16 min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              🚀 Floating AI Assistant Demo
            </h1>
            <p className="text-xl text-gray-600">
              Look for the blue AI assistant icon in the bottom-right corner!
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Feature 1 */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-3xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Always Accessible
              </h3>
              <p className="text-gray-600">
                The AI assistant is available on every page as a floating icon. 
                Click it anytime to start chatting about your career!
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-3xl mb-4">💬</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Seamless Chat
              </h3>
              <p className="text-gray-600">
                Expand the chat window, minimize it, or keep it floating. 
                The conversation stays open as you browse the site.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-3xl mb-4">🔍</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Quick Actions
              </h3>
              <p className="text-gray-600">
                Use quick action buttons for common requests like finding jobs 
                or optimizing your profile. No need to type everything!
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="text-3xl mb-4">📱</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Mobile Friendly
              </h3>
              <p className="text-gray-600">
                The floating assistant works perfectly on all devices. 
                Responsive design ensures great experience everywhere.
              </p>
            </div>
          </div>

          <div className="mt-12 text-center">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-900 mb-2">
                🎉 Try It Now!
              </h3>
              <p className="text-blue-700">
                Look at the bottom-right corner of your screen. You'll see a blue AI icon. 
                Click it to open the chat window and start talking to your AI career assistant!
              </p>
            </div>
          </div>

          <div className="mt-8 text-center text-sm text-gray-500">
            <p>
              💡 <strong>Pro Tip:</strong> The assistant remembers your conversation even when minimized. 
              You can minimize it to keep it out of the way while browsing!
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
