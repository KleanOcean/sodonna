import { motion } from 'motion/react';

const FEATURES = [
  {
    title: "The Photographic Memory",
    subtitle: "Your Digital Second Brain",
    desc: "Just speak your mind. Every decision context, voice memo, and client note — SoDonna auto-files, auto-tags, and keeps it all searchable on demand.",
    align: "left",
    image: "/images/feature_brain.png"
  },
  {
    title: "The Command Center",
    subtitle: "Clarity in One Glance",
    desc: "Ditch the bookmark chaos. We consolidate the metrics you care about most — traffic, conversions, financials — into one minimal dashboard. Five minutes a day. Total control.",
    align: "right",
    image: "/images/feature_dashboard.png"
  },
  {
    title: "The Seamless Executor",
    subtitle: "Your Autopilot Workflow",
    desc: "\"So, Donna, distribute this draft and update my logs.\" Your routine moves, handled silently by our automation engine. We guard your precious flow state.",
    align: "left",
    image: "/images/feature_flow.png"
  }
];

export function Features() {
  return (
    <section id="features" className="py-32 px-6 max-w-[1100px] mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-24"
      >
        <h2 className="font-serif text-3xl md:text-[44px] text-white mb-4">
          Why You Need SoDonna
        </h2>
        <p className="font-serif text-2xl md:text-[36px] text-white/60 italic">
          Because I'm always three steps ahead.
        </p>
      </motion.div>

      <div className="flex flex-col gap-20">
        {FEATURES.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: feature.align === 'left' ? -60 : 60 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="glass-panel rounded-[24px] p-8 md:p-16 flex flex-col md:flex-row items-center gap-12"
          >
            {feature.align === 'left' ? (
              <>
                <div className="flex-1 w-full">
                  <div className="rounded-[16px] border border-white/10 overflow-hidden shadow-[0_0_40px_rgba(99,102,241,0.08)] hover:shadow-[0_0_60px_rgba(99,102,241,0.15)] transition-shadow duration-500">
                    <img src={feature.image} alt={feature.title} className="w-full h-auto object-cover aspect-[4/3] hover:scale-[1.02] transition-transform duration-700" />
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="font-serif text-[32px] text-white mb-2">{feature.title}</h3>
                  <p className="font-serif text-lg text-white/40 italic mb-6">{feature.subtitle}</p>
                  <p className="text-lg text-white/60 leading-[1.8] max-w-[420px]">{feature.desc}</p>
                </div>
              </>
            ) : (
              <>
                <div className="flex-1 order-2 md:order-1">
                  <h3 className="font-serif text-[32px] text-white mb-2">{feature.title}</h3>
                  <p className="font-serif text-lg text-white/40 italic mb-6">{feature.subtitle}</p>
                  <p className="text-lg text-white/60 leading-[1.8] max-w-[420px]">{feature.desc}</p>
                </div>
                <div className="flex-1 w-full order-1 md:order-2">
                  <div className="rounded-[16px] border border-white/10 overflow-hidden shadow-[0_0_40px_rgba(99,102,241,0.08)] hover:shadow-[0_0_60px_rgba(99,102,241,0.15)] transition-shadow duration-500">
                    <img src={feature.image} alt={feature.title} className="w-full h-auto object-cover aspect-[4/3] hover:scale-[1.02] transition-transform duration-700" />
                  </div>
                </div>
              </>
            )}
          </motion.div>
        ))}
      </div>
    </section>
  );
}
