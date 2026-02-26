import { motion } from 'motion/react';

const FEATURES = [
  {
    title: "过目不忘的数字外脑",
    subtitle: "The Photographic Memory",
    desc: "你只管随口输出灵感。所有的决策背景、语音备忘、客户日志，SoDonna 都会自动为你归档、打标签，随时等你检索。",
    align: "left",
    image: "/images/feature_brain.png"
  },
  {
    title: "化繁为简的指挥中心",
    subtitle: "The Command Center",
    desc: "告别混乱的书签栏。我们将你最关心的核心指标（流量、转化、财务）整合在一个极简的控制面板中。每天只需 5 分钟，掌控全局健康度。",
    align: "right",
    image: "/images/feature_dashboard.png"
  },
  {
    title: "无缝衔接的工具流",
    subtitle: "The Seamless Executor",
    desc: "\"So, Donna, 帮我把这篇草稿分发出去并更新日志。\" 你的标准动作，由我通过自动化引擎无声完成。帮你死死守住最宝贵的\"心流\"状态。",
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
          为什么你需要 SoDonna？
        </h2>
        <p className="font-serif text-2xl md:text-[36px] text-white/60 italic">
          因为我永远比你提前三步。
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
