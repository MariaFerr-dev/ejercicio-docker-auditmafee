# Ejercicio Docker Audit — versión corregida

Proyecto académico para practicar auditoría, arquitectura Docker, CI/CD y despliegue.

## Fases

1. Auditoría
2. Arquitectura
3. Pipeline
4. Despliegue en EC2

## Ejecución local

```bash
cp .env.example .env
nano .env
docker compose build
docker compose up -d
docker compose ps
curl http://localhost:5050/health
```

La API escucha en `5050`, Dozzle en `8080` y Uptime Kuma en `3001`. La base de datos no se publica fuera de la red de Compose.

Si el puerto `5050` ya está ocupado en desarrollo, puedes iniciar la API en otro puerto externo: `$env:API_PORT=5051; docker compose up -d --build`.

## Pruebas

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
bandit -r app.py -f txt -o auditoria_bandit.txt
```

El archivo `.env` contiene secretos y no debe subirse al repositorio.

## Arquitectura y despliegue en EC2

La arquitectura local usa cuatro servicios: API Flask, MySQL, Dozzle y Uptime Kuma. En EC2, Nginx se instala en el host y reenvía estos subdominios:

| Subdominio | Archivo | Servicio local |
|---|---|---|
| `api.TU-DOMINIO.com` | `nginx/api.conf.example` | `127.0.0.1:5050` |
| `docker.TU-DOMINIO.com` | `nginx/docker.conf.example` | `127.0.0.1:8080` |
| `kuma.TU-DOMINIO.com` | `nginx/kuma.conf.example` | `127.0.0.1:3001` |

Con el dominio DuckDNS actual se usa `nginx/desplieguea.conf.example`: la API queda en `/`, Dozzle en `/docker/` y Uptime Kuma en `/kuma/`.

En la instancia EC2:

1. Copia `.env.example` a `.env` y cambia todas las contraseñas.
2. Ejecuta `docker compose up -d --build`.
3. Instala Nginx, copia los tres ejemplos a `sites-available`, reemplaza `TU-DOMINIO.com` y activa los sitios.
4. Abre solo `80` y `443` en el Security Group; restringe SSH a tu IP.
5. Ejecuta Certbot para emitir certificados HTTPS y recarga Nginx.

Para este dominio concreto:

```bash
sudo cp nginx/desplieguea.conf.example /etc/nginx/sites-available/desplieguea.conf
sudo ln -sf /etc/nginx/sites-available/desplieguea.conf /etc/nginx/sites-enabled/desplieguea.conf
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d despliegueaudi.duckdns.org
```

En AWS Security Group permite TCP `80` y `443` desde `0.0.0.0/0`; mantén `3306`, `5050`, `8080` y `3001` sin exposición pública.

El workflow de GitHub Actions despliega automáticamente al hacer push a `main` cuando existen los secretos `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY` y `EC2_APP_PATH`.
