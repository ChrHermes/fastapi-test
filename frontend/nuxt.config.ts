// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
    compatibilityDate: '2024-11-01',
    devtools: { enabled: true },
    modules: ['@nuxt/ui', '@nuxt/icon', '@nuxt/fonts', 'shadcn-nuxt', '@nuxtjs/color-mode'],
    css: [
        '@/assets/css/tailwind.css',
        '@/assets/css/theme.css',
        // '@/assets/css/layout.css',
        // '@/assets/css/components.css',
        // '@/assets/css/theme.css',
    ],
    vite: {
        plugins: [tailwindcss()],
    },
    app: {
        head: {
            link: [
                {
                    rel: 'stylesheet',
                    href: 'https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;700&display=swap',
                },
                {
                    rel: 'stylesheet',
                    href: 'https://fonts.googleapis.com/icon?family=Material+Icons',
                },
            ],
        },
    },
    shadcn: {
        prefix: '',
        componentDir: './components/ui',
    },
})
