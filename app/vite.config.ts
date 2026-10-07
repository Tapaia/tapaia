import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/api': 'http://127.0.0.1:4417',
      '/ws': { target: 'ws://127.0.0.1:4417', ws: true },
    },
  },
  build: { chunkSizeWarningLimit: 2000, assetsDir: '_app' },
});
