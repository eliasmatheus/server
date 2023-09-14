/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.tsx', './index.html'],
  theme: {
    // fontFamily: {
    //   sans: ['Inter', 'sans-serif'],
    // },
    extend: {
      typography(theme) {
        return {
          DEFAULT: {
            css: {
              maxWidth: '100ch',
            },
          },
          dark: {
            css: {
              color: theme('colors.slate.400'),
              '[class~="lead"]': { color: theme('colors.slate.400') },
              a: { 
                color: theme('colors.slate.200'), 
                borderBottomColor: theme('colors.sky.400'),
                textDecoration: 'none',
                borderBottom: 'theme("borderWidth.DEFAULT") solid theme("colors.sky.400")',
              },
              'a:hover': {
                color: theme('colors.slate.100'),
                borderBottomWidth: '2px',
                borderBottomColor: theme('colors.sky.300'),
              },
              strong: { color: theme('colors.slate.100') },
              'ul > li::before': { backgroundColor: theme('colors.slate.700') },
              hr: { borderColor: theme('colors.slate.800') },
              blockquote: {
                color: theme('colors.slate.100'),
                borderLeftColor: theme('colors.slate.800'),
              },
              h1: { color: theme('colors.slate.100') },
              h2: { color: theme('colors.slate.100') },
              h3: { color: theme('colors.slate.100') },
              h4: { color: theme('colors.slate.100') },
              code: { color: theme('colors.slate.100') },
              'a code': { color: theme('colors.slate.100') },
              pre: {
                color: theme('colors.slate.200'),
                backgroundColor: theme('colors.slate.800'),
              },
              thead: {
                color: theme('colors.slate.100'),
                borderBottomColor: theme('colors.slate.700'),
              },
              'tbody tr': { borderBottomColor: theme('colors.slate.800') },
            },
          },
        };
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
