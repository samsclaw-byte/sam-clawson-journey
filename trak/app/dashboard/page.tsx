'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { TrakLogo } from '@/components/logo'
import { CalorieRing } from '@/components/calorie-ring'
import { Button } from '@/components/ui/button'

const mealTypes = [
  { id: 'breakfast', label: 'Breakfast', emoji: '🌅' },
  { id: 'lunch', label: 'Lunch', emoji: '☀️' },
  { id: 'dinner', label: 'Dinner', emoji: '🌙' },
  { id: 'snacks', label: 'Snacks', emoji: '🍿' },
]

const sampleMeals = [
  { type: 'breakfast', desc: 'Two multigrain toast with Lurpak and beans', cal: 450, time: '8:30 AM' },
  { type: 'snack', desc: 'Green shake', cal: 280, time: '11:00 AM' },
]

const macros = [
  { label: 'Protein', value: 45, max: 150, color: '#22c55e' },
  { label: 'Carbs', value: 120, max: 200, color: '#f97316' },
  { label: 'Fat', value: 35, max: 70, color: '#ec4899' },
]

export default function Dashboard() {
  const [selectedMeal, setSelectedMeal] = useState<string | null>(null)
  const [mealInput, setMealInput] = useState('')
  const [todayCal] = useState(1450)
  const [goalCal] = useState(2200)

  return (
    <div className="min-h-screen bg-dark-bg pb-24">
      {/* Header */}
      <header className="px-6 py-6 flex items-center <TrakLogo justify-between">
        size="sm" />
        <div className="text-sm text-gray-400">Feb 26</div>
      </header>

      {/* Calorie Ring */}
      <div className="flex justify-center mb-8">
        <CalorieRing consumed={todayCal} goal={goalCal} size="lg" />
      </div>

      {/* Meal Quick Add */}
      <div className="px-6 mb-8">
        <h2 className="text-sm font-medium text-gray-400 mb-4">Quick Add</h2>
        <div className="grid grid-cols-4 gap-2">
          {mealTypes.map((meal) => (
            <motion.button
              key={meal.id}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedMeal(meal.id)}
              className={`py-4 rounded-2xl border-2 transition-all ${
                selectedMeal === meal.id
                  ? 'border-brand-primary bg-brand-primary/10'
                  : 'border-dark-bg-tertiary bg-dark-bg-secondary'
              }`}
            >
              <div className="text-2xl mb-1">{meal.emoji}</div>
              <div className="text-xs text-gray-400">{meal.label}</div>
            </motion.button>
          ))}
        </div>
      </div>

      {/* Meal Input */}
      <AnimatePresence>
        {selectedMeal && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="px-6 mb-8"
          >
            <textarea
              value={mealInput}
              onChange={(e) => setMealInput(e.target.value)}
              placeholder="What did you eat?"
              className="w-full h-24 px-4 py-3 bg-dark-bg-secondary border border-dark-bg-tertiary rounded-2xl text-lg resize-none focus:outline-none focus:border-brand-primary"
            />
            <div className="flex gap-2 mt-3">
              <Button className="flex-1">Add Meal</Button>
              <Button variant="secondary" onClick={() => setSelectedMeal(null)}>Cancel</Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Macros */}
      <div className="px-6 mb-8">
        <h2 className="text-sm font-medium text-gray-400 mb-4">Today's Macros</h2>
        <div className="space-y-3">
          {macros.map((macro) => (
            <div key={macro.label} className="flex items-center gap-4">
              <div className="w-20 text-sm text-gray-400">{macro.label}</div>
              <div className="flex-1 h-3 bg-dark-bg-tertiary rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(macro.value / macro.max) * 100}%` }}
                  transition={{ duration: 1, delay: 0.3 }}
                  className="h-full rounded-full"
                  style={{ backgroundColor: macro.color }}
                />
              </div>
              <div className="w-16 text-sm text-right">{macro.value}g</div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Meals */}
      <div className="px-6">
        <h2 className="text-sm font-medium text-gray-400 mb-4">Today's Meals</h2>
        <div className="space-y-3">
          {sampleMeals.map((meal, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              className="p-4 bg-dark-bg-secondary rounded-2xl flex justify-between items-center"
            >
              <div>
                <div className="text-sm text-gray-400 capitalize">{meal.type}</div>
                <div className="font-medium">{meal.desc}</div>
              </div>
              <div className="text-right">
                <div className="font-bold text-brand-primary">{meal.cal} cal</div>
                <div className="text-xs text-gray-500">{meal.time}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Bottom Nav Placeholder */}
      <div className="fixed bottom-0 left-0 right-0 h-20 bg-dark-bg-secondary border-t border-dark-bg-tertiary flex justify-around items-center px-6">
        <button className="text-brand-primary">🏠</button>
        <button className="text-gray-500">🥤</button>
        <button className="text-gray-500">📊</button>
        <button className="text-gray-500">👤</button>
      </div>
    </div>
  )
}
