'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { TrakLogo } from '@/components/logo'
import { Button } from '@/components/ui/button'

export default function ProfileSetup() {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    weight: '',
    weightUnit: 'kg',
    height: '',
    heightUnit: 'cm',
    gender: '',
    activityLevel: 3,
  })

  const activityLabels = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active']
  const activityIcons = ['🛋️', '🚶', '🏃', '💪', '⚡']

  const handleSubmit = () => {
    // Calculate BMR and save
    setStep('loading')
  }

  if (step === 'loading') {
    return (
      <div className="min-h-screen bg-dark-bg flex flex-col items-center justify-center px-6">
        <TrakLogo size="lg" className="mb-12" />
        
        <div className="w-full max-w-md space-y-4">
          {['Calculating your BMR…', 'Building your personal baseline…', 'Optimizing for your goals…'].map((text, i) => (
            <motion.div
              key={text}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 1.5 }}
              className="flex items-center gap-4 text-gray-300"
            >
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="w-5 h-5 border-2 border-brand-primary border-t-transparent rounded-full"
              />
              <span>{text}</span>
            </motion.div>
          ))}
        </div>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 5 }}
          className="mt-12"
        >
          <Button size="lg" onClick={() => setStep('done')}>
            Enter Dashboard
          </Button>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark-bg px-6 py-8">
      <div className="max-w-lg mx-auto">
        <TrakLogo size="sm" className="mb-8" />
        
        <motion.div
          key={step}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8"
        >
          <div>
            <h1 className="text-3xl font-bold mb-2">Let's get to know you</h1>
            <p className="text-gray-400">This helps us calculate your daily needs.</p>
          </div>

          {/* Name */}
          <div className="space-y-2">
            <label className="text-sm font-medium">What's your name?</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="Your name"
              className="w-full h-14 px-4 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg focus:outline-none focus:border-brand-primary transition-colors"
            />
          </div>

          {/* Age */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Age</label>
            <input
              type="number"
              value={formData.age}
              onChange={(e) => setFormData({...formData, age: e.target.value})}
              placeholder="Your age"
              className="w-full h-14 px-4 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg focus:outline-none focus:border-brand-primary"
            />
          </div>

          {/* Weight */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Weight</label>
            <div className="flex gap-2">
              <input
                type="number"
                value={formData.weight}
                onChange={(e) => setFormData({...formData, weight: e.target.value})}
                placeholder="Weight"
                className="flex-1 h-14 px-4 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg focus:outline-none focus:border-brand-primary"
              />
              <select
                value={formData.weightUnit}
                onChange={(e) => setFormData({...formData, weightUnit: e.target.value})}
                className="h-14 px-4 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg focus:outline-none"
              >
                <option value="kg">kg</option>
                <option value="lb">lb</option>
              </select>
            </div>
          </div>

          {/* Height */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Height</label>
            <div className="flex gap-2">
              <input
                type="number"
                value={formData.height}
                onChange={(e) => setFormData({...formData, height: e.target.value})}
                placeholder="Height"
                className="flex-1 h-14 px-4 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg focus:outline-none focus:border-brand-primary"
              />
              <select
                value={formData.heightUnit}
                onChange={(e) => setFormData({...formData, heightUnit: e.target.value})}
                className="h-14 px-4 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg"
              >
                <option value="cm">cm</option>
                <option value="in">in</option>
              </select>
            </div>
          </div>

          {/* Gender */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Gender</label>
            <div className="grid grid-cols-3 gap-2">
              {['Male', 'Female', 'Other'].map((g) => (
                <button
                  key={g}
                  onClick={() => setFormData({...formData, gender: g})}
                  className={`h-14 rounded-2xl border-2 transition-all ${
                    formData.gender === g 
                      ? 'border-brand-primary bg-brand-primary/10' 
                      : 'border-dark-bg-tertiary'
                  }`}
                >
                  {g}
                </button>
              ))}
            </div>
          </div>

          {/* Activity Level Slider */}
          <div className="space-y-4">
            <label className="text-sm font-medium">Activity Level</label>
            <div className="pt-4 pb-2">
              <input
                type="range"
                min="1"
                max="5"
                value={formData.activityLevel}
                onChange={(e) => setFormData({...formData, activityLevel: parseInt(e.target.value)})}
                className="w-full h-2 bg-dark-bg-tertiary rounded-lg appearance-none cursor-pointer accent-brand-primary"
              />
              <div className="flex justify-between mt-4">
                {activityLabels.map((label, i) => (
                  <div key={label} className="text-center">
                    <div className="text-2xl mb-1">{activityIcons[i]}</div>
                    <div className={`text-xs ${formData.activityLevel === i + 1 ? 'text-brand-primary' : 'text-gray-500'}`}>
                      {label.split(' ')[0]}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <Button size="xl" className="w-full mt-8" onClick={handleSubmit}>
            Complete Setup
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
