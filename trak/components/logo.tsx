'use client'

import { motion } from 'framer-motion'

export function TrakLogo({ className = '', size = 'md' }: { className?: string; size?: 'sm' | 'md' | 'lg' | 'xl' }) {
  const sizes = {
    sm: { width: 80, fontSize: '2rem' },
    md: { width: 120, fontSize: '3rem' },
    lg: { width: 180, fontSize: '4rem' },
    xl: { width: 280, fontSize: '6rem' },
  }

  const { width, fontSize } = sizes[size]

  return (
    <div 
      className={`inline-flex items-center font-bold tracking-tight ${className}`}
      style={{ width, fontSize }}
    >
      {/* trak text */}
      <span className="text-white">tra</span>
      
      {/* k with animated arrow */}
      <span className="relative">
        <span className="text-brand-primary">k</span>
        
        {/* Arrow rising from bottom of k */}
        <motion.div
          className="absolute -right-2 -bottom-1"
          initial={{ opacity: 0, y: 10, scale: 0.5 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ 
            duration: 0.8, 
            delay: 0.5,
            ease: [0.34, 1.56, 0.64, 1] // Cinematic ease
          }}
        >
          <svg 
            width={size === 'xl' ? 32 : size === 'lg' ? 24 : 16}
            height={size === 'xl' ? 32 : size === 'lg' ? 24 : 16}
            viewBox="0 0 24 24" 
            fill="none"
            className="text-brand-primary"
          >
            <motion.path
              d="M5 12h14M13 6l6 6-6 6"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.6, delay: 0.8, ease: "easeInOut" }}
            />
          </svg>
        </motion.div>
      </span>
    </div>
  )
}
