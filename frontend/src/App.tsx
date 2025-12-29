import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import APIExplorer from './components/APIExplorer';
import SkillsSection from './components/SkillsSection';
import ProjectsSection from './components/ProjectsSection';
import './index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-900 text-white">
        <Header />
        <main>
          <HeroSection />
          <APIExplorer />
          <SkillsSection />
          <ProjectsSection />
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;