import type { Config } from 'tailwindcss'

export default {
  content: [
    './index.html',
    './src/**/*.{vue,ts,tsx,js,jsx}'
  ],
  theme: {
    extend: {
      colors: {
        parchment: '#f5f0e6'
      },
      fontFamily: {
        serif: ['"Times New Roman"', 'serif']
      }
    }
  },
  plugins: []
} satisfies Config

