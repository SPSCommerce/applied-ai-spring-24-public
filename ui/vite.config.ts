import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const proxyConfig = {
  '/api': {
    target: 'http://api:8000', // for local development when using docker
    // target: 'http://localhost:8000', // for local development when NOT using docker
    rewrite: (path: string) => path.replace(/^\/api/, '')
  }
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: proxyConfig
  }
})
