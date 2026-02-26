import { BackgroundOrbs } from './components/BackgroundOrbs';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { PainPoints } from './components/PainPoints';
import { Features } from './components/Features';
import { Philosophy } from './components/Philosophy';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen selection:bg-[#7C3AED]/30 selection:text-white">
      <BackgroundOrbs />
      <Navbar />
      <main>
        <Hero />
        <PainPoints />
        <Features />
        <Philosophy />
      </main>
      <Footer />
    </div>
  );
}
