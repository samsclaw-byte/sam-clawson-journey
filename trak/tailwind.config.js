/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#22c55e',
          'primary-dark': '#16a34a',
          'primary-light': '#4ade80',
        },
        dark: {
          bg: '#0f172a',
          'bg-secondary': '#1e293b',
          'bg-tertiary': '#334155',
        },
        accent: {
          sunset: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
          warm: '#fef3c7',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Georgia', 'serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out',
        'slide-up': 'slideUp 0.6s ease-out',
        'scale-in': 'scaleIn 0.4s ease-out',
        'ring-fill': 'ringFill 1.5s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        ringFill: {
          '0%': { strokeDashoffset: '100' },
          '100%': { strokeDashoffset: 'var(--ring-progress)' },
        },
      },
    },
  },
  plugins: [],
}
