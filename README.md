```bash
# Crear el ambiente virtual

python3 -m venv .venv

# Activar el ambiente virtual
source .venv/bin/activate

#Para desactivarlo

deactivate

#Instalar requerimientos

pip install -r requirements.txt

# levantar contenedores (postgres + pgadmin)
docker compose up -d --build

# ver estado
docker compose ps

# logs de pgadmin
docker logs -f pgadmin-container
```

Accesos:

- pgAdmin: http://localhost:5050
- PostgreSQL host: localhost
- PostgreSQL port: 5433
- user: app_user
- password: app_password
- db: app_db
