Carpeta de assets para el modulo web.

Para compilar la app de javascript
 
- `coffee -cj ./static/js/app.js ./app/*` 
- `coffee -wcj ./static/js/app.js ./app/*` (dev)

Para compilar sass en css

- `sass ./app/sass:./static/css/app.css`
- `sass --watch ./app/sass/app.scss:./static/css`