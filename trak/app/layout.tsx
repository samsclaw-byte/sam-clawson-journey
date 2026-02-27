import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Trak - Simple Nutrition Tracking',
  description: 'Simple tracking for busy people who want to win.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-dark-bg text-white antialiased">
        {children}
      </body>
    </html>
  )
}
