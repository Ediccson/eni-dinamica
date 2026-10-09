# Desplegar en Render

El archivo `render.yaml` configura un servicio Django gratuito de Render. Su
base de datos se conecta a PostgreSQL de Supabase para que las convocatorias no
dependan del disco efímero del servicio. El nivel gratuito de Render puede
detener el servicio tras inactividad, por lo que la primera petición posterior
puede tardar.

## Conectar el repositorio

1. En Render, crear un **Blueprint** y conectar el repositorio
   `Ediccson/eni-dinamica`.
2. Al solicitar `DATABASE_URL`, usar en Supabase **Connect → Session pooler** y
   copiar la URI de PostgreSQL. Render necesita el pooler IPv4. Sustituir el
   marcador de contraseña por la contraseña de la base de datos y codificar
   caracteres reservados de la contraseña para URL.
3. No compartir ni guardar la URI con la contraseña en GitHub, en este archivo
   ni en el chat. `DJANGO_SECRET_KEY` se genera automáticamente.
4. Aplicar el Blueprint y esperar a que finalicen la instalación, los archivos
   estáticos y las migraciones.

La migración enlaza el modelo Django con la tabla existente
`public.convocatorias`; la aplicación reconoce la tabla y conserva las filas
que ya tenga. No usar SQLite en Render.

## Acceso a la API

La URL del servicio Render sirve las páginas, pero todas las operaciones de
`/api/convocatorias/` requieren autenticación. El sitio de GitHub Pages continúa
usando Supabase directamente. Esta protección es intencional: no exponer datos
de convocatorias mediante lecturas anónimas, que evitaría la política RLS de
Supabase. El nivel gratuito no ofrece una garantía de disponibilidad y puede
tener arranques en frío.
