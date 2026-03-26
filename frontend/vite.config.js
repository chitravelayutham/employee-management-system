/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
  globals: true,          // <-- this enables `describe`, `it`, `beforeEach` globally
  environment: 'jsdom',   // <-- needed for React DOM
  setupFiles: './src/tests/setup.js',
  deps: {
    inline: ['react', 'react-dom'],
  },
},
})

