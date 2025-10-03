import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 54323,   // port fixe
    strictPort: true  // échoue si le port est déjà utilisé
  }
})