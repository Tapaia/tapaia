import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/api': 'http://localhost:4417',
      '/ws': { target: 'ws://localhost:4417', ws: true },
    },
  },
  build: { chunkSizeWarningLimit: 2000, assetsDir: '_app' },
});
