import Header from '@/components/Header';
import HeroSection from '@/components/HeroSection';
import APIExplorer from '@/components/APIExplorer';
import SkillsSection from '@/components/SkillsSection';
import ProjectsSection from '@/components/ProjectsSection';
import CertificationsSection from '@/components/CertificationsSection';
import HealthDashboard from '@/components/HealthDashboard';
import Footer from '@/components/Footer';

const Index = () => {
  return (
    <div className="min-h-screen bg-background text-foreground" style={{ backgroundColor: 'hsl(222 47% 6%)' }}>
      <Header />
      <main>
        <HeroSection />
        <APIExplorer />
        <SkillsSection />
        <ProjectsSection />
        <CertificationsSection />
        <HealthDashboard />
      </main>
      <Footer />
    </div>
  );
};

export default Index;