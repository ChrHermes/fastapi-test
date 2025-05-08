// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  // Kompatibilitätsmodus für zukünftige Nuxt-Versionen
  compatibilityDate: '2024-11-01',

  // Aktiviert die Nuxt Devtools (Shift + Alt + D im Browser)
  devtools: { enabled: true },

  // Nuxt-Module (siehe https://modules.nuxt.com)
  modules: [
    '@nuxt/ui',              // UI-Komponenten und Themes
    '@nuxt/icon',            // Icon-Komponenten
    '@nuxt/fonts',           // Font Management
    'shadcn-nuxt',           // ShadCN UI Integration
    '@nuxtjs/color-mode',    // Dark/Light Mode Handling
  ],

  // Globale CSS-Dateien
  css: [
    '@/assets/css/tailwind.css', // Tailwind Basis
    '@/assets/css/theme.css',    // Eigene Theme-Anpassungen
  ],

  // Vite-Konfiguration (z. B. zusätzliche Plugins)
  vite: {
    plugins: [tailwindcss()],
  },

  // App-spezifische Einstellungen
  app: {
    baseURL: '/', // Basis-URL der App

    // Globale <head>-Einträge (z. B. Fonts, Icons)
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

  // Komponenten
  components: [
    {
      path: '~/components',
      pathPrefix: true,
    },
  ],

  // ShadCN UI Konfiguration
  shadcn: {
    prefix: '', // keine Namenspräfixe für Komponenten
    componentDir: './components/ui', // Zielverzeichnis für UI-Komponenten
  },

  // Konfigurierbare Umgebungsvariablen (z. B. für das Backend)
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api', // API-Endpunkt für dein FastAPI-Backend
      // Alternativ dynamisch mit .env: apiBase: process.env.API_BASE || 'http://localhost:8000/api'
    },
  },

  // Rendering-Einstellungen
  ssr: false, // Client-Side Rendering aktivieren (SPA-Modus)

  // Nitro Build-Konfiguration (hier: statisches Deployment)
  nitro: {
    preset: 'static', // erstellt ein vollständig statisches Frontend
  },
})
