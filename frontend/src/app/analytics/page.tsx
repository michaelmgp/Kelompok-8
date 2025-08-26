import TopNavigation from "@/components/layout/TopNavigation";
import Analytics from "@/components/analytics/Analytics";

export default function AnalyticsPage() {
  return (
    <>
      <TopNavigation />
      <div className="pt-16">
        <Analytics />
      </div>
    </>
  );
}