import Header from '@/components/Header';
import HeroSection from '@/components/HeroSection';
import APIExplorer from '@/components/APIExplorer';
import SkillsSection from '@/components/SkillsSection';
import ProjectsSection from '@/components/ProjectsSection';
import HealthDashboard from '@/components/HealthDashboard';
import Footer from '@/components/Footer';

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <HeroSection />
        <APIExplorer />
        <SkillsSection />
        <ProjectsSection />
        <HealthDashboard />
      </main>
      <Footer />
    </div>
  );
};

export default Index;