import { useEffect, useState } from 'react';
import { motion } from 'motion/react';

export function BackgroundOrbs() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: e.clientX,
        y: e.clientY,
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-[-1]">
      <motion.div
        className="absolute w-[50vw] h-[50vw] rounded-full opacity-30 blur-[80px]"
        style={{
          background: 'radial-gradient(circle, rgba(124,58,237,0.3) 0%, rgba(37,99,235,0.15) 40%, transparent 70%)',
        }}
        animate={{
          x: mousePosition.x * 0.02,
          y: mousePosition.y * 0.02,
          scale: [1, 1.05, 1],
        }}
        transition={{
          scale: { duration: 8, repeat: Infinity, ease: "easeInOut" },
          x: { type: "spring", stiffness: 50, damping: 20 },
          y: { type: "spring", stiffness: 50, damping: 20 }
        }}
      />
      <motion.div
        className="absolute right-0 top-[20%] w-[40vw] h-[40vw] rounded-full opacity-20 blur-[80px]"
        style={{
          background: 'radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 50%)',
        }}
        animate={{
          x: -mousePosition.x * 0.01,
          y: -mousePosition.y * 0.01,
        }}
        transition={{
          x: { type: "spring", stiffness: 50, damping: 20 },
          y: { type: "spring", stiffness: 50, damping: 20 }
        }}
      />
    </div>
  );
}
