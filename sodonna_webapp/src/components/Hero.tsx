import { motion } from 'motion/react';
import { ArrowRight, ChevronDown } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center pt-20 px-6 overflow-hidden">
      <div className="max-w-[1100px] mx-auto w-full flex flex-col md:flex-row items-center gap-12 relative z-10">
        {/* Image LEFT */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="flex-1 w-full md:w-auto"
        >
          <div className="rounded-[24px] border border-white/10 overflow-hidden shadow-[0_0_60px_rgba(124,58,237,0.1)]">
            <img
              src="/images/hero_donna.png"
              alt="Donna at her desk"
              className="w-full h-auto object-cover"
            />
          </div>
        </motion.div>

        {/* Text RIGHT */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
          className="flex-1 flex flex-col items-start text-left"
        >
          <h1 className="font-serif text-4xl md:text-5xl lg:text-[72px] leading-[1.1] tracking-[0.02em] mb-8">
            <span className="text-gradient bg-gradient-to-b from-white to-[#C084FC]">
              You think big.
              <br />
              I handle everything else.
            </span>
          </h1>

          <p className="text-lg md:text-[20px] text-white/60 leading-[1.7] max-w-xl mb-10">
            SoDonna — the ultimate support system built for solo CEOs.
            You're the visionary 1. We're the tireless 0.1 behind the scenes,
            managing your tools, organizing your logs, clearing every obstacle.
          </p>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="glass-button flex items-center gap-2 px-8 py-4 rounded-full text-white font-medium text-lg mb-4 group"
          >
            Hire Your Donna
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </motion.button>

          <p className="text-sm text-white/35">
            Say goodbye to tab-switching chaos.
          </p>
        </motion.div>
      </div>

      <motion.div
        className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center text-white/30"
        animate={{ opacity: [0.3, 1, 0.3], y: [0, 5, 0] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      >
        <div className="w-1 h-1 rounded-full bg-white/50 mb-2" />
        <ChevronDown className="w-5 h-5" />
      </motion.div>
    </section>
  );
}
