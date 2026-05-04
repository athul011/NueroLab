# Docker Setup Guide

## Quick Start

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will:
- Build and start the FastAPI backend on `http://localhost:8000`
- Build and start the Next.js frontend on `http://localhost:3000`

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Individual Service Commands

### Build Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Run Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Image Details

### Backend Image
- **Base Image**: `python:3.11.9-slim-bullseye`
- **Size**: Optimized slim variant (~200MB)
- **Security**: Runs as non-root user (appuser)
- **Health Check**: Included

### Frontend Image
- **Build Stage**: `node:20.13-alpine`
- **Runtime Stage**: `node:20.13-alpine`
- **Size**: Multi-stage build optimized (~150MB)
- **Security**: Runs as non-root user (appuser)
- **Health Check**: Included

## Best Practices Implemented

✅ Pinned base image versions (no :latest tags)
✅ Pinned all Python and Node.js dependency versions
✅ Multi-stage build for frontend (smaller production image)
✅ Used `--no-install-recommends` for minimal dependencies
✅ Non-root user for security
✅ Health checks for both services
✅ Layer caching optimization (dependencies copied first)
✅ .dockerignore for smaller context

## Production Deployment

For production, consider:

1. **Use Docker registry** to store pinned images by digest:
   ```bash
   docker build --tag myregistry/neuro-backend:v1.0.0 ./Backend
   docker push myregistry/neuro-backend:v1.0.0
   ```

2. **Reference by digest** in docker-compose or orchestration:
   ```yaml
   image: myregistry/neuro-backend@sha256:abc123...
   ```

3. **Environment variables**: Use `.env` file for production secrets:
   ```bash
   docker-compose --env-file .env.production up
   ```

## Troubleshooting

### Backend service not connecting
- Check if backend is healthy: `docker-compose ps`
- View logs: `docker-compose logs backend`

### Frontend cannot reach backend
- Ensure backend service name is `backend` in requests
- Verify `NEXT_PUBLIC_API_URL` environment variable

### Port already in use
```bash
# Change ports in docker-compose.yml or run on different port
docker-compose -p myapp up
```

## Cleanup

```bash
# Remove containers and networks
docker-compose down

# Remove images too
docker-compose down --rmi all

# Remove volumes
docker-compose down -v
```
