import { motion } from 'motion/react';
import { BrainCircuit, Wrench, FileClock } from 'lucide-react';

const PAIN_POINTS = [
  {
    icon: BrainCircuit,
    title: "Fragmented Focus",
    desc: "One moment you're crafting a grand strategy, the next you're hunting for that customer insight you scribbled down yesterday.",
    color: "from-purple-500/20"
  },
  {
    icon: Wrench,
    title: "Tool Overload",
    desc: "You're subscribed to a dozen SaaS tools, yet half your day is spent moving data from A to B.",
    color: "from-blue-500/20"
  },
  {
    icon: FileClock,
    title: "Zero Decision Trail",
    desc: "No one takes meeting notes for you. No debrief logs. Last month's winning playbook? Already forgotten.",
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
          The Solo CEO Reality:<br />
          You think you're running a company.<br />
          You're actually drowning in busywork.
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
