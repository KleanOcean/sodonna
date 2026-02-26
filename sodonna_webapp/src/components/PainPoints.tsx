import { motion } from 'motion/react';
import { BrainCircuit, Wrench, FileClock } from 'lucide-react';

const PAIN_POINTS = [
  {
    icon: BrainCircuit,
    title: "精力碎片化",
    desc: "上一秒在构思宏大战略，下一秒却在寻找昨天随手记下的某个客户灵感？",
    color: "from-purple-500/20"
  },
  {
    icon: Wrench,
    title: "工具综合征",
    desc: "订阅了无数个 SaaS 软件，却每天要把一半的时间花在将数据从 A 搬运到 B 上。",
    color: "from-blue-500/20"
  },
  {
    icon: FileClock,
    title: "决策无记录",
    desc: "没有人帮你做会议纪要，没有复盘日志，上个月的成功经验这个月无法复用。",
    color: "from-cyan-500/20"
  }
];

export function PainPoints() {
  return (
    <section className="py-32 px-6 max-w-[1100px] mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.8 }}
        className="mb-20"
      >
        <h2 className="font-serif text-3xl md:text-5xl text-gradient bg-gradient-to-b from-white to-white/60 tracking-[0.02em] leading-tight">
          一人公司的真相：<br />
          你以为你在做 CEO，其实你在做打字员。
        </h2>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {PAIN_POINTS.map((point, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-50px" }}
            transition={{ duration: 0.7, delay: index * 0.15, ease: [0.16, 1, 0.3, 1] }}
            className="glass-panel rounded-[20px] p-8 md:p-10 relative group hover:-translate-y-1 transition-all duration-300 hover:shadow-[0_8px_40px_rgba(0,0,0,0.5)] hover:border-white/20 overflow-hidden"
          >
            {/* Top gradient line */}
            <div className={`absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r ${point.color} to-transparent opacity-50 group-hover:opacity-100 transition-opacity`} />
            
            <div className="w-14 h-14 rounded-full flex items-center justify-center mb-8 relative">
              <div className={`absolute inset-0 rounded-full bg-gradient-to-br ${point.color} to-transparent opacity-50`} />
              <point.icon className="w-6 h-6 text-white/80 relative z-10" />
            </div>

            <h3 className="text-[22px] font-semibold text-white mb-4">{point.title}</h3>
            <p className="text-[15px] text-white/50 leading-[1.75]">{point.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
