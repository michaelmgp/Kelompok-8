import TopNavigation from "@/components/layout/TopNavigation";
import Documentation from "@/components/docs/Documentation";

export default function DocsPage() {
  return (
    <>
      <TopNavigation />
      <div className="pt-16">
        <Documentation />
      </div>
    </>
  );
}