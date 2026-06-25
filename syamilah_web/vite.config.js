import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react'; // 1. Import plugin react

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.jsx'], // 2. Ubah app.js menjadi app.jsx
            refresh: true,
        }),
        react(), // 3. Pasang plugin react di sini
    ],
});
