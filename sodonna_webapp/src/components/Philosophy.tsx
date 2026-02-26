import { motion } from 'motion/react';

export function Philosophy() {
  return (
    <section id="philosophy" className="relative py-40 px-6 overflow-hidden">
      {/* Spotlight Orb */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80vw] h-[80vw] rounded-full opacity-15 blur-[100px] pointer-events-none"
           style={{ background: 'radial-gradient(circle, rgba(124,58,237,0.5) 0%, transparent 60%)' }} />

      <div className="max-w-[1100px] mx-auto relative z-10 flex flex-col items-center text-center">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="font-serif text-5xl md:text-[72px] text-gradient bg-gradient-to-b from-[#C084FC] to-white mb-6"
        >
          The 1.1 Company
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="font-serif text-3xl md:text-[40px] text-white tracking-[0.12em] mb-16"
        >
          The ultimate form of a super-individual.
        </motion.p>

        {/* Donna philosophy image */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
          className="max-w-md mb-24 rounded-[24px] overflow-hidden border border-white/10"
        >
          <img
            src="/images/donna_philosophy.png"
            alt="The intelligence behind the scenes"
            className="w-full h-auto object-cover"
          />
        </motion.div>

        <div className="flex flex-col gap-8 w-full max-w-4xl text-left mb-24">
          <motion.div
            initial={{ opacity: 0, scale: 0.6, filter: 'blur(20px)' }}
            whileInView={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
            viewport={{ once: true }}
            transition={{ duration: 1.2, ease: [0.34, 1.56, 0.64, 1] }}
            className="glass-panel rounded-[24px] p-8 md:p-12 flex flex-col md:flex-row items-center md:items-start gap-8 md:gap-16"
          >
            <div className="font-serif text-[100px] md:text-[120px] leading-none text-gradient bg-gradient-to-b from-[#C084FC] to-white">
              1
            </div>
            <div className="flex-1 pt-4">
              <p className="text-xl md:text-[20px] text-white/80 leading-[1.8]">
                That's you:<br />
                Your irreplaceable strategic vision, creativity, and business instinct.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.6, filter: 'blur(20px)' }}
            whileInView={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
            viewport={{ once: true }}
            transition={{ duration: 1.2, delay: 0.2, ease: [0.34, 1.56, 0.64, 1] }}
            className="glass-panel rounded-[24px] p-8 md:p-12 flex flex-col md:flex-row items-center md:items-start gap-8 md:gap-16"
          >
            <div className="font-serif text-[100px] md:text-[120px] leading-none text-gradient bg-gradient-to-b from-[#2563EB] to-white">
              0.1
            </div>
            <div className="flex-1 pt-4">
              <p className="text-xl md:text-[20px] text-white/80 leading-[1.8]">
                That's SoDonna:<br />
                A tireless, emotionless, always-on support system that never sleeps.
              </p>
            </div>
          </motion.div>
        </div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-xl text-white/50 leading-[1.8] max-w-2xl"
        >
          We don't interfere with your decisions.<br />
          We just make sure every one of them lands flawlessly.
        </motion.p>
      </div>
    </section>
  );
}
