# Docker Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Database Connection Issues

#### Issue: "psycopg2 error: could not connect to server"

**Causes:**
- Database service isn't running
- Database isn't ready yet
- Incorrect database credentials
- Port conflict

**Solutions:**

```bash
# 1. Check if database is running
docker-compose ps db

# 2. View database logs
docker-compose logs db

# 3. Test connection from web container
docker-compose exec web python -c "
import psycopg2
try:
    conn = psycopg2.connect('dbname=green_citizen user=postgres password=postgres host=db port=5432')
    print('✅ Connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Connection failed: {e}')
"

# 4. Restart database
docker-compose restart db

# 5. Check database logs for errors
docker-compose logs db --tail 50
```

#### Issue: "database "green_citizen" does not exist"

**Solution:**

```bash
# The database should be created automatically, but if not:
docker-compose exec db psql -U postgres -c "CREATE DATABASE green_citizen;"

# Or restart everything fresh
docker-compose down -v
docker-compose up -d
```

---

### 🔴 Redis Connection Issues

#### Issue: "Error 111: Connection refused"

**Causes:**
- Redis service isn't running
- Redis isn't ready yet
- Port conflict

**Solutions:**

```bash
# 1. Check if Redis is running
docker-compose ps redis

# 2. Test Redis connection
docker-compose exec redis redis-cli ping
# Should return: PONG

# 3. View Redis logs
docker-compose logs redis

# 4. Restart Redis
docker-compose restart redis

# 5. Access Redis CLI
docker-compose exec redis redis-cli
```

---

### 🔴 Port Already in Use

#### Issue: "bind: address already in use"

**Causes:**
- Port 8000, 5432, or 6379 already in use by another service
- Previous Docker containers not fully stopped

**Solutions:**

```bash
# 1. Find what's using the port (on Linux/Mac)
lsof -i :8000
lsof -i :5432
lsof -i :6379

# 2. On Windows, use:
netstat -ano | findstr :8000
netstat -ano | findstr :5432
netstat -ano | findstr :6379

# 3. Stop conflicting service
# Kill the process or close the application using the port

# 4. Change ports in docker-compose.yml:
# Original:
#  ports:
#    - "8000:8000"
# 
# Change to:
#  ports:
#    - "8001:8000"

# 5. Restart Docker Compose
docker-compose down
docker-compose up -d
```

---

### 🔴 Django Migration Issues

#### Issue: "no such table" or migration errors

**Causes:**
- Migrations not applied
- Database corrupted
- Entrypoint script didn't run

**Solutions:**

```bash
# 1. Check migration status
docker-compose exec web python manage.py showmigrations

# 2. Apply migrations manually
docker-compose exec web python manage.py migrate

# 3. Create new migrations
docker-compose exec web python manage.py makemigrations

# 4. Reset database completely
docker-compose down -v
docker-compose up -d
# Wait for services to be healthy

# 5. If still failing, check entrypoint script
docker-compose logs web | grep -i "migrate"
```

---

### 🔴 Static Files Not Loading

#### Issue: 404 errors for /static/ or /media/

**Causes:**
- Static files not collected
- Nginx misconfigured (production only)
- Volume mount issue

**Solutions:**

```bash
# 1. Collect static files
docker-compose exec web python manage.py collectstatic --no-input

# 2. Check static files location
docker-compose exec web ls -la /app/staticfiles/

# 3. Verify volume mounts
docker-compose exec web ls -la /app/

# 4. Clear and rebuild everything
docker-compose down
docker volume prune -f
docker-compose up -d
docker-compose exec web python manage.py collectstatic --no-input

# 5. Check permissions
docker-compose exec web ls -la /app/staticfiles/
```

---

### 🔴 Celery Worker Issues

#### Issue: "Celery tasks not executing"

**Causes:**
- Celery worker crashed
- Redis broker connection failed
- Tasks not properly defined

**Solutions:**

```bash
# 1. Check if celery worker is running
docker-compose ps celery_worker

# 2. View celery worker logs
docker-compose logs celery_worker

# 3. Restart celery worker
docker-compose restart celery_worker

# 4. Check Redis connection
docker-compose exec celery_worker python -c "from celery import current_app; print(current_app.connection())"

# 5. Test a simple task
docker-compose exec web python -c "
from apps.users.utils.verification_code import hello
result = hello.delay()
print(result)
"

# 6. Monitor celery activity
docker-compose exec celery_worker celery -A core inspect active

# 7. Check celery beat schedule
docker-compose exec celery_beat celery -A core inspect scheduled
```

---

### 🔴 Memory/Performance Issues

#### Issue: "Killed" processes, slow performance

**Causes:**
- Docker containers running out of memory
- Too many worker processes
- Memory leak in application

**Solutions:**

```bash
# 1. Check container resource usage
docker stats

# 2. View container memory
docker-compose ps
docker top green-citizen-web
docker top green-citizen-celery-worker

# 3. Reduce worker processes in docker-compose.yml
# Change from:
# command: celery -A core worker -l info
# To:
# command: celery -A core worker -l info --concurrency=2

# 4. Limit container resources in docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

# 5. Restart and monitor
docker-compose down
docker-compose up -d
docker stats
```

---

### 🔴 Permission Denied Errors

#### Issue: "Permission denied" when accessing files

**Causes:**
- File ownership issues
- Volume mount permission issues
- Running as wrong user

**Solutions:**

```bash
# 1. Check file ownership
docker-compose exec web ls -la /app/

# 2. Fix ownership (inside container)
docker-compose exec -u root web chown -R django:django /app/

# 3. Fix permissions
docker-compose exec -u root web chmod -R 755 /app/
docker-compose exec -u root web chmod -R 755 /app/staticfiles/
docker-compose exec -u root web chmod -R 755 /app/media/

# 4. On Windows, this might be WSL2 issue
# Ensure WSL2 is properly configured for Docker
```

---

### 🔴 Build Issues

#### Issue: "Error building image"

**Causes:**
- Dependency conflicts
- Python package compilation errors
- Docker disk space issue

**Solutions:**

```bash
# 1. Force rebuild with verbose output
docker-compose build --no-cache web 2>&1 | tail -100

# 2. Check Docker disk space
docker system df

# 3. Clean up dangling images and containers
docker system prune -a
docker volume prune -f

# 4. Increase Docker disk limit (if using Docker Desktop)
# Docker Desktop > Preferences > Resources > Disk image size

# 5. Try rebuilding specific service
docker-compose build --no-cache db
docker-compose build --no-cache redis
docker-compose build --no-cache web

# 6. View build logs
docker-compose build --no-cache web --verbose 2>&1 | head -200
```

---

### 🔴 Network Issues

#### Issue: "network not found" or cross-container connectivity failing

**Causes:**
- Services not on same network
- Docker daemon networking issue
- Firewall blocking

**Solutions:**

```bash
# 1. Check networks
docker network ls
docker network inspect green-citizen_green-network

# 2. Test connectivity between containers
docker-compose exec web ping db
docker-compose exec web ping redis

# 3. Test service discovery (DNS)
docker-compose exec web nslookup db
docker-compose exec web getent hosts redis

# 4. Restart Docker daemon
# Docker Desktop > Restart
# Or: sudo systemctl restart docker

# 5. Recreate networks
docker-compose down
docker network prune -f
docker-compose up -d
```

---

### 🔴 Environment Variable Issues

#### Issue: "KeyError" or missing environment variables

**Causes:**
- .env file not found
- .env not loaded properly
- Variable name typo

**Solutions:**

```bash
# 1. Check if .env exists
ls -la .env
ls -la .env.docker

# 2. Verify .env is being read
docker-compose config | grep TELEGRAM_BOT_TOKEN

# 3. Check environment in running container
docker-compose exec web env | grep TELEGRAM

# 4. Verify variable formatting in .env
# Correct: KEY=value
# Incorrect: KEY = value (spaces cause issues)

# 5. Reload environment
docker-compose down
cp .env.docker .env
# Edit .env with actual values
docker-compose up -d

# 6. Test specific variable
docker-compose exec web python -c "import os; print(os.getenv('TELEGRAM_BOT_TOKEN'))"
```

---

### 🔴 Application Won't Start

#### Issue: Container keeps restarting or exits immediately

**Causes:**
- Python syntax errors
- Import errors
- Configuration errors
- Port binding failure

**Solutions:**

```bash
# 1. Check logs immediately
docker-compose logs web --tail 100

# 2. Try running manually
docker-compose run --rm web python manage.py check

# 3. Check for syntax errors
docker-compose exec web python -m py_compile apps/

# 4. Test imports
docker-compose exec web python -c "import django; django.setup()"

# 5. Verify settings
docker-compose exec web python -c "from django.conf import settings; print(settings.INSTALLED_APPS)"

# 6. Run migrations
docker-compose exec web python manage.py migrate

# 7. Start in foreground to see errors
docker-compose down
docker-compose up web  # Don't use -d, see output directly
```

---

### 🔴 Superuser Creation Issues

#### Issue: "User already exists" or creation fails

**Causes:**
- User already created
- Database issue
- Permission denied

**Solutions:**

```bash
# 1. Try interactive creation
docker-compose exec web python manage.py createsuperuser

# 2. Create with flags
docker-compose exec web python manage.py createsuperuser \
  --username admin \
  --email admin@example.com \
  --noinput \
  --password securepassword

# 3. If user exists, change password
docker-compose exec web python manage.py changepassword admin

# 4. Delete and recreate
docker-compose exec web python manage.py shell
# Inside shell:
# >>> from django.contrib.auth import get_user_model
# >>> User = get_user_model()
# >>> User.objects.filter(username='admin').delete()
# >>> exit()

# 5. Try full reset
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔍 Debugging Techniques

### Enable verbose logging
```bash
# Docker Compose verbose
docker-compose -f docker-compose.yml up --verbose

# Django debug
docker-compose exec web python -c "
import django
django.setup()
from django.conf import settings
print('Debug:', settings.DEBUG)
print('Allowed Hosts:', settings.ALLOWED_HOSTS)
"
```

### Interactive shell debugging
```bash
# Access Python shell
docker-compose exec web python manage.py shell

# Inside shell, test things:
>>> from django.conf import settings
>>> from django.db import connection
>>> connection.ensure_connection()
>>> print("DB OK")
```

### Monitor in real-time
```bash
# Watch logs continuously
docker-compose logs -f

# Watch specific service
docker-compose logs -f web --tail 50

# Follow multiple services
docker-compose logs -f web db redis
```

---

## 📞 When to Reset Everything

If nothing else works:

```bash
# Complete reset (⚠️ WARNING: Deletes all data!)
docker-compose down -v
docker system prune -af
docker volume prune -f

# Rebuild everything
docker-compose build --no-cache

# Start fresh
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

---

## 🆘 Getting More Help

1. Check container logs: `docker-compose logs [service] --tail 100`
2. Check Docker events: `docker events --filter type=container`
3. Test locally: `python manage.py runserver` (without Docker)
4. Review system resources: `docker stats`
5. Check Docker version: `docker --version && docker-compose --version`

---

Good luck! 🍀

