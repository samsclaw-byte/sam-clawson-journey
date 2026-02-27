'use client'

import { motion } from 'framer-motion'

interface CalorieRingProps {
  consumed: number
  goal: number
  size?: 'sm' | 'md' | 'lg'
}

export function CalorieRing({ consumed, goal, size = 'lg' }: CalorieRingProps) {
  const percentage = Math.min((consumed / goal) * 100, 100)
  const circumference = 2 * Math.PI * 54 // radius = 54
  
  const sizes = {
    sm: { w: 100, stroke: 6, text: 'text-lg' },
    md: { w: 160, stroke: 10, text: 'text-3xl' },
    lg: { w: 220, stroke: 14, text: 'text-5xl' },
  }
  
  const { w, stroke, text } = sizes[size]

  return (
    <div className="relative" style={{ width: w, height: w }}>
      {/* Background ring */}
      <svg className="w-full h-full -rotate-90">
        <circle
          cx={w/2}
          cy={w/2}
          r={54}
          fill="none"
          stroke="currentColor"
          strokeWidth={stroke}
          className="text-dark-bg-tertiary"
        />
        {/* Progress ring */}
        <motion.circle
          cx={w/2}
          cy={w/2}
          r={54}
          fill="none"
          stroke="url(#gradient)"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: circumference - (percentage / 100) * circumference }}
          transition={{ duration: 1.5, ease: 'easeOut' }}
        />
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#22c55e" />
            <stop offset="100%" stopColor="#4ade80" />
          </linearGradient>
        </defs>
      </svg>
      
      {/* Center text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className={`${text} font-bold text-white`}>
          {consumed.toLocaleString()}
        </span>
        <span className="text-gray-400 text-sm">of {goal.toLocaleString()} cal</span>
      </div>
    </div>
  )
}
