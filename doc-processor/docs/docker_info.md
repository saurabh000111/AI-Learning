# Docker Commands — FastAPI Development

Quick reference for running **FastAPI + PostgreSQL** locally with Docker Compose.

---

## 1. Initial Setup

### Check Docker installation

```bash
# Shows installed Docker version
docker --version

# Shows Docker Compose version
docker compose version

# Verify Docker Engine is running
docker info
```

### Build the project

```bash
# Build all services defined in compose.yaml
docker compose build

# Rebuild without using cached layers
docker compose build --no-cache
```

Use `--no-cache` when dependencies or Dockerfile changes are not being picked up correctly.

---

## 2. Start Services

```bash
# Start all services in background
docker compose up -d
```

Example services:

```text
FastAPI
PostgreSQL
Redis
```

Start only PostgreSQL:

```bash
# Start only the postgres service
docker compose up -d postgres
```

Start FastAPI and PostgreSQL:

```bash
docker compose up -d api postgres
```

Start and rebuild changed images:

```bash
# Very useful after Dockerfile/dependency changes
docker compose up -d --build
```

---

## 3. Check Running Containers

```bash
# Show services belonging to current Compose project
docker compose ps

# Show all currently running Docker containers
docker ps

# Show running + stopped containers
docker ps -a
```

Use this immediately after `docker compose up` to verify that services actually started.

---

## 4. View Logs

```bash
# Logs for all Compose services
docker compose logs

# Follow logs continuously
docker compose logs -f

# Follow FastAPI logs
docker compose logs -f api

# Follow PostgreSQL logs
docker compose logs -f postgres
```

Show only recent logs:

```bash
docker compose logs --tail=100 api
```

`-f` means **follow**, similar to Linux `tail -f`.

Press:

```text
Ctrl + C
```

to stop following logs. It does **not** stop the container.

---

## 5. Stop Services

```bash
# Stop containers but keep them
docker compose stop
```

Start them again:

```bash
docker compose start
```

Stop and remove Compose containers/networks:

```bash
docker compose down
```

Important difference:

```text
stop  → stop containers, keep them
start → restart stopped containers

down  → stop + remove containers
up    → create/start them again
```

---

## 6. PostgreSQL Data — Important

Normally:

```bash
docker compose down
```

does **not** delete named volumes, so your PostgreSQL data remains.

But:

```bash
docker compose down -v
```

removes the volumes too.

### ⚠️ Development database reset

```bash
# Removes containers AND volumes/database data
docker compose down -v

# Create everything again
docker compose up -d
```

Use `-v` carefully. Your local PostgreSQL data can be permanently deleted.

---

## 7. Restart Services

Restart everything:

```bash
docker compose restart
```

Restart only FastAPI:

```bash
docker compose restart api
```

Restart PostgreSQL:

```bash
docker compose restart postgres
```

---

## 8. Execute Commands Inside Container

Open shell inside FastAPI container:

```bash
docker compose exec api sh
```

If Bash exists:

```bash
docker compose exec api bash
```

Example:

```bash
docker compose exec api python --version
```

Useful for debugging dependencies, environment variables, files, etc.

---

## 9. PostgreSQL Commands

Open PostgreSQL CLI:

```bash
docker compose exec postgres psql -U postgres
```

Connect directly to a database:

```bash
docker compose exec postgres psql -U postgres -d app_db
```

Inside `psql`:

```sql
-- Show databases
\l

-- Show tables
\dt

-- Describe table
\d users

-- Exit PostgreSQL
\q
```

---

## 10. Inspect Containers

Detailed container information:

```bash
docker inspect <container-name>
```

Check container resource usage:

```bash
docker stats
```

Check Docker disk usage:

```bash
docker system df
```

---

## 11. Images

List downloaded images:

```bash
docker images
```

Pull PostgreSQL manually:

```bash
docker pull postgres:16
```

Remove an image:

```bash
docker rmi <image-id>
```

---

## 12. Cleanup Commands

Remove stopped containers:

```bash
docker container prune
```

Remove unused images:

```bash
docker image prune
```

Remove unused Docker resources:

```bash
docker system prune
```

More aggressive:

```bash
docker system prune -a
```

⚠️ Be careful with prune commands, especially on machines containing other development projects.

---

# Daily Development Workflow

### Start working

```bash
# Start project
docker compose up -d

# Verify services
docker compose ps

# Watch API logs
docker compose logs -f api
```

### After Dockerfile/dependency changes

```bash
docker compose up -d --build
```

### Something isn't working

```bash
docker compose ps

docker compose logs --tail=100 api

docker compose logs --tail=100 postgres
```

### End of development

```bash
docker compose stop
```

Or remove the containers:

```bash
docker compose down
```

---

# Most Important Commands to Remember

| Command                                         | Purpose                        |
| ----------------------------------------------- | ------------------------------ |
| `docker info`                                   | Check Docker Engine            |
| `docker compose build`                          | Build images                   |
| `docker compose up -d`                          | Start application              |
| `docker compose up -d --build`                  | Rebuild + start                |
| `docker compose ps`                             | Check service status           |
| `docker compose logs -f`                        | Follow logs                    |
| `docker compose logs -f api`                    | FastAPI logs                   |
| `docker compose logs -f postgres`               | PostgreSQL logs                |
| `docker compose stop`                           | Stop services                  |
| `docker compose start`                          | Start stopped services         |
| `docker compose restart`                        | Restart services               |
| `docker compose down`                           | Stop + remove containers       |
| `docker compose down -v`                        | Remove containers + DB volumes |
| `docker compose exec api sh`                    | Enter API container            |
| `docker compose exec postgres psql -U postgres` | PostgreSQL CLI                 |

---

# Mental Model

```text
Dockerfile
    │
    │ docker compose build
    ▼
Docker Image
    │
    │ docker compose up
    ▼
Container
    │
    ├── FastAPI
    ├── PostgreSQL
    └── Redis

docker compose logs     → See what happened
docker compose exec     → Enter running container
docker compose stop     → Pause containers
docker compose start    → Resume containers
docker compose down     → Remove containers
docker compose down -v  → Remove containers + data
```

## Recommended project file

Save this document as:

```text
docs/
└── docker-commands.md
```

This keeps Docker operational notes separate from the main `README.md`.



## 21 sept 2026 updated
## docker 
docker compose exec postgres psql -U doc_user -d doc_processor