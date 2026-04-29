# Green Citizen - Docker Setup Guide

## 📋 Prerequisites

Make sure you have Docker and Docker Compose installed:
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## 🚀 Quick Start

### 1. Environment Configuration

Copy and customize the Docker environment file:

```bash
cp .env.docker .env
```

Update the`.env` file with your configuration:

```dotenv
TELEGRAM_BOT_TOKEN=your_actual_token
TELEGRAM_CHANNEL_ID=your_actual_channel_id
SECRET_KEY=your-secure-secret-key
```

### 2. Build and Run

Start all services with Docker Compose:

```bash
docker-compose up -d
```

The `-d` flag runs services in the background. To see logs:

```bash
docker-compose logs -f
```

### 3. Access the Application

- **Django API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/schema/swagger/
- **Database**: postgres://postgres:postgres@localhost:5432/green_citizen

### 4. Create a Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

Or access the admin:
```
http://localhost:8000/admin
```

## 📦 Services

The `docker-compose.yml` includes:

### 1. **PostgreSQL (db)**
- Port: 5432
- Database: green_citizen
- User: postgres
- Password: postgres (development only!)
- Volume: `postgres_data` (persists data)

### 2. **Redis (redis)**
- Port: 6379
- Used for: Caching and Celery broker
- Volume: `redis_data` (persists data)

### 3. **Django Web App (web)**
- Port: 8000
- Auto-reloads on code changes
- Runs migrations automatically on startup
- Collects static files on startup

### 4. **Celery Worker (celery_worker)**
- Processes async tasks
- Depends on: db, redis, web

### 5. **Celery Beat (celery_beat)**
- Schedules periodic tasks
- Depends on: db, redis, web

## 🛠️ Common Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f db
```

### Database Management

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Access database shell
docker-compose exec db psql -U postgres -d green_citizen
```

### Celery Management

```bash
# View worker logs
docker-compose logs -f celery_worker

# View beat logs
docker-compose logs -f celery_beat
```

### Rebuild Images

```bash
# Rebuild all services
docker-compose build

# Rebuild specific service
docker-compose build web
docker-compose build --no-cache web  # Force rebuild without cache
```

### Stop Services

```bash
# Stop all running services
docker-compose down

# Stop and remove volumes (delete data!)
docker-compose down -v
```

## 🔧 Development Workflow

### Hot Reload

Code changes are automatically reflected due to volume mounting. Django's development server (`--reload` flag in Gunicorn) watches for changes.

### Shell Access

```bash
# Django shell
docker-compose exec web python manage.py shell

# Interactive bash
docker-compose exec web bash
```

### Run Custom Commands

```bash
docker-compose exec web python manage.py [command]
```

## 📋 Environment Variables

Key environment variables in `.env`:

```dotenv
# Django
DJANGO_SETTINGS_MODULE=core.settings.dev
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,web

# Database
DB_NAME=green_citizen
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/2
CELERY_RESULT_BACKEND=django-db

# Telegram
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=your_channel_id
```

## 🐛 Troubleshooting

### Port Already in Use

If ports 8000, 5432, or 6379 are already in use, modify `docker-compose.yml`:

```yaml
  web:
    ports:
      - "8001:8000"  # Use 8001 instead

  db:
    ports:
      - "5433:5432"  # Use 5433 instead

  redis:
    ports:
      - "6380:6379"  # Use 6380 instead
```

### Database Connection Issues

```bash
# Check if db is running
docker-compose ps

# Check db logs
docker-compose logs db

# Verify connectivity
docker-compose exec web python -c "
import psycopg2
conn = psycopg2.connect('dbname=green_citizen user=postgres password=postgres host=db')
print('✅ Database connected!')
"
```

### Redis Connection Issues

```bash
# Check if redis is running
docker-compose ps

# Test redis connection
docker-compose exec web redis-cli -h redis ping
```

### Clear Cache/Reset Database

```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild and start fresh
docker-compose build --no-cache
docker-compose up -d

# Create new superuser
docker-compose exec web python manage.py createsuperuser
```

## 🚢 Production Deployment

For production, create a separate `docker-compose.prod.yml`:

```yaml
# Use core.settings.prod instead of dev
# Set DEBUG=False
# Use proper SECRET_KEY
# Configure ALLOWED_HOSTS
# Use stronger database credentials
# Disable auto-reload
# Use multiple gunicorn workers
# Add reverse proxy (nginx)
# Use SSL certificates
```

## 📚 Resources

- Django Documentation: https://docs.djangoproject.com/
- Docker Documentation: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- PostgreSQL: https://www.postgresql.org/
- Redis: https://redis.io/
- Celery: https://docs.celeryproject.io/

## 💡 Tips

1. **Always backup your database** before running `docker-compose down -v`
2. **Use `.env` for secrets**, never commit it to git
3. **Check logs** first when something doesn't work: `docker-compose logs -f [service]`
4. **Use `docker-compose exec`** to run one-off commands
5. **Restart services** when changing `.env`: `docker-compose restart`

---

Enjoy your development with Docker! 🐳

