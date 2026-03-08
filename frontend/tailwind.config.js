/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: '#000000', // Pure obsidian
                surface: '#09090b',    // Zinc 950
                borderclr: '#27272a',  // Zinc 800
                primary: '#fafafa',    // Zinc 50
                secondary: '#a1a1aa',  // Zinc 400
                accent: '#3b82f6',     // High-intensity electric blue (rare highlights)
                error: '#ef4444',      // Crisp red
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
            },
            animation: {
                'scanline': 'scanline 2s linear infinite',
                'pulse-glow': 'pulseGlow 3s ease-in-out infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                scanline: {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(100%)' },
                },
                pulseGlow: {
                    '0%, 100%': { opacity: '0.4', filter: 'blur(40px)' },
                    '50%': { opacity: '0.8', filter: 'blur(60px)' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            }
        },
    },
    plugins: [],
}
