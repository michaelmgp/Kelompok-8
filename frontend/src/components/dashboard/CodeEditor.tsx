import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function CodeEditor() {
  return (
    <div className="mt-8 bg-white rounded-xl border border-gray-200 overflow-hidden" data-testid="code-editor">
      <div className="p-4 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <i className="fas fa-code text-career-blue"></i>
          <span className="text-sm font-medium text-black">Code Editor</span>
        </div>
        <Button 
          variant="ghost"
          className="text-career-blue hover:text-blue-600 text-sm"
          data-testid="button-open-editor"
        >
          Open Full Editor
        </Button>
      </div>
      <div className="p-6 bg-gray-900 text-gray-300 font-mono text-sm overflow-x-auto">
        <div className="space-y-2">
          <div>
            <span className="text-purple-400">import</span>{" "}
            <span className="text-blue-400">React</span>{" "}
            <span className="text-purple-400">from</span>{" "}
            <span className="text-green-400">&apos;react&apos;</span>;
          </div>
          <div>
            <span className="text-purple-400">import</span>{" "}
            <span className="text-blue-400">{"{ NextPage }"}</span>{" "}
            <span className="text-purple-400">from</span>{" "}
            <span className="text-green-400">&apos;next&apos;</span>;
          </div>
          <div></div>
          <div>
            <span className="text-purple-400">const</span>{" "}
            <span className="text-blue-400">Dashboard</span>:{" "}
            <span className="text-blue-400">NextPage</span> = () =&gt; {"{"}
          </div>
          <div className="ml-4">
            <span className="text-purple-400">return</span> (
          </div>
          <div className="ml-8">
            &lt;<span className="text-red-400">div</span>{" "}
            <span className="text-yellow-400">className</span>=
            <span className="text-green-400">&quot;p-6&quot;</span>&gt;
          </div>
          <div className="ml-12">
            &lt;<span className="text-red-400">h1</span>&gt;Welcome to CareerVerse&lt;/
            <span className="text-red-400">h1</span>&gt;
          </div>
          <div className="ml-8">
            &lt;/<span className="text-red-400">div</span>&gt;
          </div>
          <div className="ml-4">);</div>
          <div>{"}"}</div>
          <div></div>
          <div>
            <span className="text-purple-400">export default</span>{" "}
            <span className="text-blue-400">Dashboard</span>;
          </div>
        </div>
      </div>
    </div>
  );
}
