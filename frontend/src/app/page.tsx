import TopNavigation from "@/components/layout/TopNavigation";
import HeroSection from "@/components/home/HeroSection";
import FeaturesSection from "@/components/home/FeaturesSection";
import StatsSection from "@/components/home/StatsSection";

export default function HomePage() {
  return (
    <>
      <TopNavigation />
      <div className="pt-16">
        <HeroSection />
        <FeaturesSection />
        <StatsSection />
      </div>
    </>
  );
}