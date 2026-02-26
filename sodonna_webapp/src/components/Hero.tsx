import { motion } from 'motion/react';
import { ArrowRight, ChevronDown } from 'lucide-react';

export function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center pt-20 px-6 text-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        className="max-w-4xl mx-auto flex flex-col items-center"
      >
        <h1 className="font-serif text-5xl md:text-7xl lg:text-[96px] leading-[1.1] tracking-[0.02em] mb-8">
          <span className="text-gradient bg-gradient-to-b from-white to-[#C084FC]">
            你负责思考商业版图，
            <br />
            剩下的交给我。
          </span>
        </h1>
        
        <p className="text-lg md:text-[22px] text-white/60 leading-[1.7] max-w-2xl mb-12">
          SoDonna —— 专为"一人公司"打造的 CEO 终极支持系统。
          你是冲锋陷阵的 1，我们是为你打理工具、整理日志、扫除一切执行障碍的 0.1。
        </p>

        <motion.button 
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="glass-button flex items-center gap-2 px-8 py-4 rounded-full text-white font-medium text-lg mb-6 group"
        >
          雇佣你的专属 Donna
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </motion.button>

        <p className="text-sm text-white/35">
          告别在 10 个后台中来回切换的崩溃感。
        </p>
      </motion.div>

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
