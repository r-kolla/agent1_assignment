import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
  base: '/static/frontend/',           // ensure correct asset paths
  build: {
    outDir: '../static/frontend',
    assetsDir: 'assets',
    emptyOutDir: true,
  },
});

