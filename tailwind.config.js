/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./main/templates/**/*.html", "./main/static/**/*.ts"],
  theme: {
    extend: {},
  },
  plugins: [require('@tailwindcss/forms')],
}

