import { useState } from 'react';
import { motion } from 'motion/react';
import { Check, Loader2 } from 'lucide-react';

export function Footer() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      setStatus('error');
      setTimeout(() => setStatus('idle'), 2000);
      return;
    }

    setStatus('loading');
    // Simulate API call
    setTimeout(() => {
      setStatus('success');
      setTimeout(() => {
        setStatus('idle');
        setEmail('');
      }, 3000);
    }, 1500);
  };

  return (
    <footer className="py-32 px-6 flex flex-col items-center text-center relative">
      <div className="absolute bottom-0 left-0 right-0 h-[50vh] bg-gradient-to-t from-[#7C3AED]/10 to-transparent pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-3xl mx-auto relative z-10"
      >
        {/* Donna portrait */}
        <div className="mb-10">
          <img
            src="/images/donna_footer.png"
            alt="Donna"
            className="w-[200px] h-[200px] object-cover rounded-full border-2 border-white/10 mx-auto shadow-[0_0_40px_rgba(124,58,237,0.1)]"
          />
        </div>

        <p className="font-serif text-[28px] md:text-[36px] italic text-white/70 mb-12">
          "I'm Donna. I know everything.<br />
          And I've already taken care of it."
        </p>

        <div className="w-12 h-[1px] bg-white/10 mx-auto mb-12" />

        <p className="text-xl text-white/50 mb-10">
          Ready to meet your perfect partner?<br />
          The first wave of "1.1 Companies" is assembling now.
        </p>

        <form onSubmit={handleSubmit} className="mb-24">
          <motion.div
            animate={status === 'error' ? { x: [-10, 10, -10, 10, 0] } : {}}
            transition={{ duration: 0.4 }}
            className={`flex flex-col sm:flex-row items-center p-1.5 rounded-full border transition-colors duration-300 ${
              status === 'success' ? 'border-[#10B981] bg-[#10B981]/10' :
              status === 'error' ? 'border-red-500/50 bg-red-500/10' :
              'border-white/10 bg-white/5 focus-within:border-white/25'
            }`}
          >
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={status === 'loading' || status === 'success'}
              className="w-full sm:w-[300px] bg-transparent border-none text-white px-6 py-3.5 outline-none placeholder:text-white/30 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={status === 'loading' || status === 'success'}
              className={`w-full sm:w-auto px-7 py-3.5 rounded-full font-semibold transition-all duration-300 flex items-center justify-center min-w-[160px] ${
                status === 'success' ? 'bg-[#10B981] text-white' : 'bg-white text-[#09090B] hover:bg-white/90 active:scale-95'
              }`}
            >
              {status === 'loading' ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : status === 'success' ? (
                <span className="flex items-center gap-2">
                  <Check className="w-5 h-5" /> You're on the list
                </span>
              ) : (
                'Join the Waitlist'
              )}
            </button>
          </motion.div>
        </form>

        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between text-sm text-white/30 w-full">
          <span>SoDonna · 2026</span>
          <div className="flex gap-4 mt-4 sm:mt-0">
            <a href="#" className="hover:text-white/60 transition-colors">Twitter</a>
            <a href="#" className="hover:text-white/60 transition-colors">LinkedIn</a>
          </div>
        </div>
      </motion.div>
    </footer>
  );
}
