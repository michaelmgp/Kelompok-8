import TopNavigation from "@/components/layout/TopNavigation";
import JobBoard from "@/components/jobs/JobBoard";

export default function JobsPage() {
  return (
    <>
      <TopNavigation />
      <div className="pt-16">
        <JobBoard />
      </div>
    </>
  );
}