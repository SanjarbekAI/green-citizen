# Green Citizen - Docker Quick Start Guide

## 🚀 Before You Start

Make sure you have Docker and Docker Compose installed on your system:
- **Docker**: https://docs.docker.com/get-docker/
- **Docker Compose**: https://docs.docker.com/compose/install/

Verify installation:
```bash
docker --version
docker-compose --version
```

---

## 📝 Development Setup (Local)

### 1️⃣ **Create Environment File**

```bash
# Copy the docker environment template
cp .env.docker .env
```

Edit `.env` file and update your values:
```dotenv
TELEGRAM_BOT_TOKEN=your_actual_token
TELEGRAM_CHANNEL_ID=your_actual_channel_id
SECRET_KEY=your-secure-secret-key
```

### 2️⃣ **Start All Services**

```bash
# Build and start all services
docker-compose up -d

# Or with logs visible
docker-compose up
```

Expected output:
```
✅ Creating green-citizen-db ...
✅ Creating green-citizen-redis ...
✅ Creating green-citizen-web ...
✅ Creating green-citizen-celery-worker ...
✅ Creating green-citizen-celery-beat ...
```

### 3️⃣ **Check Services**

```bash
# View running services
docker-compose ps

# View logs
docker-compose logs -f          # All services
docker-compose logs -f web      # Django only
docker-compose logs -f db       # Database only
docker-compose logs -f redis    # Redis only
```

### 4️⃣ **Create Superuser**

```bash
# Interactive mode
docker-compose exec web python manage.py createsuperuser

# Or with flags
docker-compose exec web python manage.py createsuperuser --username admin --email admin@example.com
```

### 5️⃣ **Access Your Application**

Open your browser and navigate to:

| Service | URL |
|---------|-----|
| **Django API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/api/schema/swagger/ |
| **Admin Panel** | http://localhost:8000/admin |
| **PostgreSQL** | postgres://postgres:postgres@localhost:5432/green_citizen |
| **Redis** | redis://localhost:6379 |

---

## 🛑 Stop Services

```bash
# Stop all services (keep data)
docker-compose down

# Stop and remove all data (⚠️ WARNING: deletes database!)
docker-compose down -v

# Stop specific service
docker-compose stop web
```

---

## 🔧 Development Workflow

### Run Django Commands

```bash
# Migrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations

# Create test data
docker-compose exec web python manage.py shell

# Run management commands
docker-compose exec web python manage.py [command]
```

### Access Database

```bash
# PostgreSQL shell
docker-compose exec db psql -U postgres -d green_citizen

# Redis CLI
docker-compose exec redis redis-cli
```

### View Application Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f db
```

### Hot Reload

Code changes are automatically detected due to volume mounting. Just modify your files, and Django will reload!

---

## 📦 Production Setup

### 1️⃣ **Create Production Environment**

```bash
# Copy production environment template
cp .env.prod .env.prod.local

# Edit with your production values
nano .env.prod.local
```

### 2️⃣ **Generate SSL Certificates**

For development/testing (self-signed):
```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

For production, use Let's Encrypt with Certbot (see DOCKER.md for details).

### 3️⃣ **Deploy with Production Compose**

```bash
# Using production compose file
docker-compose -f docker-compose.prod.yml --env-file .env.prod.local up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 4️⃣ **Access Production Services**

| Service | URL |
|---------|-----|
| **Application** | https://yourdomain.com |
| **API Documentation** | https://yourdomain.com/api/schema/swagger/ |
| **Admin** | https://yourdomain.com/admin |

---

## 🐛 Troubleshooting

### ❌ Port Already in Use

```yaml
# Edit docker-compose.yml to use different ports:
services:
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

### ❌ Database Connection Failed

```bash
# Check if database is running
docker-compose ps db

# View database logs
docker-compose logs db

# Test connection
docker-compose exec web python -c "
import psycopg2
conn = psycopg2.connect('dbname=green_citizen user=postgres password=postgres host=db')
print('✅ Connected!')
"
```

### ❌ Redis Connection Failed

```bash
# Check if redis is running
docker-compose ps redis

# Test redis connection
docker-compose exec redis redis-cli ping
```

### ❌ Static Files Not Loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --no-input

# Clear and rebuild
docker-compose down -v
docker-compose up -d
```

### ❌ Migrations Not Applied

```bash
# Manual migration
docker-compose exec web python manage.py migrate

# Check migration status
docker-compose exec web python manage.py showmigrations
```

---

## 📚 Common Commands Reference

| Command | Purpose |
|---------|---------|
| `docker-compose up -d` | Start all services in background |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f [service]` | View service logs |
| `docker-compose exec web bash` | SSH into web container |
| `docker-compose exec web python manage.py [cmd]` | Run Django commands |
| `docker-compose build` | Rebuild images |
| `docker-compose ps` | List running services |
| `docker-compose restart [service]` | Restart specific service |

---

## 🔗 Useful Resources

- **Full Documentation**: See `DOCKER.md` for detailed guide
- **Django Docs**: https://docs.djangoproject.com/
- **Docker Docs**: https://docs.docker.com/
- **Docker Compose Docs**: https://docs.docker.com/compose/

---

## ✅ Verification Checklist

After starting Docker, verify everything works:

- [ ] All services running: `docker-compose ps` (all showing "Up")
- [ ] Web accessible: http://localhost:8000
- [ ] Database connected: `docker-compose exec web python manage.py dbshell`
- [ ] Redis working: `docker-compose exec redis redis-cli ping` returns "PONG"
- [ ] Static files served: Visit http://localhost:8000/admin/
- [ ] Celery worker active: `docker-compose logs celery_worker` shows "ready to accept tasks"
- [ ] Celery beat active: `docker-compose logs celery_beat` shows scheduler is running

---

## 🎉 You're Ready!

Your Green Citizen application is now running in Docker. Happy developing! 🚀

For more detailed information, see `DOCKER.md`

