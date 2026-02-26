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
          className="font-serif text-3xl md:text-[40px] text-white tracking-[0.12em] mb-24"
        >
          超级个体的终极形态。
        </motion.p>

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
                代表着你：<br />
                独一无二的战略眼光、创意和商业直觉。
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
                代表着 SoDonna：<br />
                一套不知疲倦、没有情绪、永远在线的支持系统。
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
          我们不干涉你的决断，<br />
          我们只负责让你的每一个决断都丝滑落地。
        </motion.p>
      </div>
    </section>
  );
}
