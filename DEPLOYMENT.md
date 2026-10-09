# Despliegue de Django

La configuración recomendada actualmente para este proyecto es Render, definida
en [`render.yaml`](./render.yaml) y explicada en
[`RENDER_DEPLOY.md`](./RENDER_DEPLOY.md). El servicio usa PostgreSQL persistente
de Supabase; Render Free puede suspender instancias inactivas.

## Alternativa: Google Cloud Run

El contenedor también está preparado para Cloud Run. No se desplegó porque
requiere un proyecto de Google Cloud con facturación configurada.

## Configuración requerida

- `DJANGO_SECRET_KEY`: secreto largo y aleatorio, distinto de la clave local.
- `DATABASE_URL`: URL de conexión a PostgreSQL persistente con SSL. No usar
  SQLite en Cloud Run: su disco de escritura es efímero.
- `DJANGO_ALLOWED_HOSTS`: nombres de host permitidos, separados por comas.
- `DJANGO_CSRF_TRUSTED_ORIGINS`: orígenes HTTPS adicionales, separados por
  comas, solo si se usan formularios Django desde otros dominios.

Guardar `DJANGO_SECRET_KEY` y `DATABASE_URL` en Secret Manager antes del
despliegue y conceder a la cuenta de servicio de Cloud Run permiso para
leerlos. No ponerlos en el código, en GitHub ni en la imagen del contenedor.
La base de datos no se crea automáticamente: aplicar las migraciones antes de
recibir tráfico.

## Despliegue

Instalar Google Cloud CLI, seleccionar un proyecto con facturación activa y
autenticarse con `gcloud auth login`. Luego, desde la carpeta del proyecto:

```powershell
gcloud config set project ID_DEL_PROYECTO
gcloud run deploy eni-django-api --source . --region us-east1 --set-secrets "DJANGO_SECRET_KEY=django-secret:latest,DATABASE_URL=eni-database-url:latest"
```

En el comando, `django-secret` y `eni-database-url` son nombres de ejemplo:
crear esos secretos previamente o sustituirlos por los nombres reales. La
primera implementación puede solicitar habilitar las API necesarias. Consultar
la guía oficial de [configuración de secretos en
Cloud Run](https://cloud.google.com/run/docs/configuring/services/secrets).

El comando deja el servicio privado. La API Django requiere autenticación para
leer, crear, editar o eliminar convocatorias. Las páginas de GitHub Pages
actualmente se conectan directamente a Supabase y no necesitan acceso público
al backend Django.

Ejecutar `python manage.py migrate` contra la misma base PostgreSQL antes de
enviar tráfico. Para ello, usar un entorno administrativo temporal que tenga
los mismos secretos y dependencias del servicio; no ejecutar migraciones
concurrentemente desde cada instancia de Cloud Run.

## Comprobación local del contenedor

Con Docker instalado y las variables de producción configuradas, se puede
construir y ejecutar localmente:

```powershell
docker build -t eni-django-api .
docker run --rm -p 8080:8080 --env-file .env eni-django-api
```

El archivo `.env` es solo local y está excluido del contexto Docker.
