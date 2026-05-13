// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://rahulproduct08.github.io',
  base: '/VibeCodePrototypes',
  vite: {
    plugins: [tailwindcss()]
  }
});
