import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Menu, X } from 'lucide-react';

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled ? 'bg-[#09090B]/70 backdrop-blur-md border-b border-white/5' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 h-[72px] flex items-center justify-between">
        <div className="font-serif text-xl font-medium text-white">SoDonna</div>

        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-white/60 hover:text-white transition-colors text-sm">Features</a>
          <a href="#philosophy" className="text-white/60 hover:text-white transition-colors text-sm">Philosophy</a>
          <button className="glass-button px-5 py-2 rounded-full text-sm text-white font-medium">
            Sign In
          </button>
        </div>

        <button
          className="md:hidden text-white"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute top-[72px] left-0 right-0 bg-[#09090B]/95 backdrop-blur-xl border-b border-white/10 p-6 flex flex-col gap-6 md:hidden"
        >
          <a href="#features" className="text-white/80 text-lg" onClick={() => setMobileMenuOpen(false)}>Features</a>
          <a href="#philosophy" className="text-white/80 text-lg" onClick={() => setMobileMenuOpen(false)}>Philosophy</a>
          <button className="bg-white text-black rounded-full py-3 font-medium mt-4">
            Get Started
          </button>
        </motion.div>
      )}
    </header>
  );
}
