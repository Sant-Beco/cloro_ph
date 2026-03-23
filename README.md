## Registro de pH y cloro (Granjas e incubación)

Backend API para registrar mediciones de **pH** y **cloro** en 3 sedes:

- Granja Esperanza
- Granja La Fe
- Planta de incubación

### Stack

- Python 3.11+
- FastAPI + Uvicorn
- PostgreSQL 15+
- SQLAlchemy 2.0 + Alembic
- Poetry
- pytest + coverage
- loguru + Sentry
- Docker + Docker Compose

## Inicio rápido

### 1) Instalar dependencias

```bash
poetry install
```

### 2) Configurar variables de entorno

Crear `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/cloro_ph
LOG_LEVEL=INFO
SENTRY_DSN=
```

### 3) Levantar PostgreSQL con Docker

```bash
docker compose up -d db
```

### 4) Ejecutar migraciones

```bash
poetry run alembic upgrade head
```

### 5) Cargar sedes iniciales

```bash
poetry run python -m src.seed
```

### 6) Ejecutar API

```bash
poetry run uvicorn src.main:app --reload
```

Documentación interactiva:

- http://127.0.0.1:8000/docs

## Endpoints clave

- `GET /health`
- `GET /sites`
- `POST /measurements`
- `GET /measurements`

Campos de cada medición:

- `site_id`
- `sampled_at`
- `ph_value`
- `chlorine_value`
- `area` (opcional)
- `observation` (opcional)

## Testing

```bash
poetry run pytest -q
```
