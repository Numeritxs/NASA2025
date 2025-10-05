# NASA 2025 Exoplanet Application - Docker Setup

This document explains how to run the NASA 2025 Exoplanet Application using Docker.

## Architecture

The application consists of two main services:

- **Backend**: FastAPI-based machine learning API for exoplanet prediction
- **Frontend**: Next.js React application with 3D visualization

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB of available RAM
- Ports 3000 and 8000 available

## Quick Start

### Option 1: Using the startup script (Recommended)

```bash
./start_docker.sh
```

### Option 2: Manual Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

## Services

### Backend API
- **URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Port**: 8000

### Frontend Application
- **URL**: http://localhost:3000
- **Port**: 3000

## Docker Network

Both services run on a custom Docker network called `nasa-network`, allowing them to communicate with each other using service names:
- Frontend can reach Backend at `http://backend:8000`
- Backend can reach Frontend at `http://frontend:3000`

## Environment Variables

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

### Backend
- `PYTHONPATH`: Python path for the application

## Useful Commands

```bash
# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f frontend
docker-compose logs -f backend

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild and restart
docker-compose up --build --force-recreate

# Check service status
docker-compose ps
```

## Troubleshooting

### Port Already in Use
If you get port conflicts, you can modify the ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Frontend on port 3001
  - "8001:8000"  # Backend on port 8001
```

### Services Not Starting
1. Check if Docker is running: `docker info`
2. Check logs: `docker-compose logs`
3. Ensure model files exist in `Backend/modelos/`
4. Try rebuilding: `docker-compose up --build --force-recreate`

### Frontend Can't Connect to Backend
1. Verify CORS configuration in `Backend/main.py`
2. Check if both services are on the same network: `docker network ls`
3. Test backend directly: `curl http://localhost:8000/health`

## Development

For development with hot reload:

```bash
# Backend development
cd Backend
docker-compose up

# Frontend development (separate terminal)
cd Frontend
npm run dev
```

## Production Deployment

For production deployment, consider:
1. Using environment-specific configuration files
2. Setting up proper secrets management
3. Using a reverse proxy (nginx)
4. Setting up monitoring and logging
5. Using Docker Swarm or Kubernetes for orchestration
