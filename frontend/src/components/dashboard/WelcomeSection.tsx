import { Button } from "@/components/ui/button";

export default function WelcomeSection() {
  return (
    <div className="mb-8" data-testid="welcome-section">
      <div className="bg-gradient-to-r from-black to-career-dark text-white rounded-xl p-8">
        <h1 className="text-3xl font-bold mb-2">Welcome to CareerVerse</h1>
        <p className="text-gray-300 mb-4">
          Your professional development platform. Focus on building amazing frontend experiences.
        </p>
        <div className="flex space-x-4">
          <Button 
            className="bg-career-blue hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            data-testid="button-start-coding"
          >
            Start Coding
          </Button>
          <Button 
            variant="outline"
            className="border border-gray-300 hover:bg-white hover:text-black text-white px-6 py-2 rounded-lg font-medium transition-colors"
            data-testid="button-view-docs"
          >
            View Docs
          </Button>
        </div>
      </div>
    </div>
  );
}
