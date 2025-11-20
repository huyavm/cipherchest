#!/bin/bash

echo "========================================="
echo "CipherChest - Docker Deploy Script"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to project directory
cd "$(dirname "$0")"

# Step 1: Pull latest code (if using git)
echo -e "${YELLOW}[1/6]${NC} Pulling latest code from Git..."
if [ -d .git ]; then
    git pull origin main
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Git pull failed!${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Code updated${NC}"
else
    echo -e "${YELLOW}⚠ Not a git repository, skipping...${NC}"
fi
echo ""

# Step 2: Check .env file
echo -e "${YELLOW}[2/6]${NC} Checking environment configuration..."
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env file not found!${NC}"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please update .env with your secrets before continuing!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Environment configured${NC}"
echo ""

# Step 3: Build Docker images
echo -e "${YELLOW}[3/6]${NC} Building Docker images..."
docker-compose build
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Docker build failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Images built successfully${NC}"
echo ""

# Step 4: Stop old containers
echo -e "${YELLOW}[4/6]${NC} Stopping old containers..."
docker-compose down
echo -e "${GREEN}✓ Old containers stopped${NC}"
echo ""

# Step 5: Start new containers
echo -e "${YELLOW}[5/6]${NC} Starting new containers..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to start containers!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Containers started${NC}"
echo ""

# Step 6: Wait and check health
echo -e "${YELLOW}[6/6]${NC} Waiting for services to be healthy..."
sleep 10

# Check container status
echo ""
echo "Container Status:"
docker-compose ps
echo ""

# Try health check
echo "Checking health endpoint..."
sleep 2
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health 2>/dev/null || echo "000")

if [ "$HEALTH_CHECK" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${YELLOW}⚠ Health check returned: $HEALTH_CHECK${NC}"
    echo "Check logs with: docker-compose logs -f"
fi

# Success
echo ""
echo "========================================="
echo -e "${GREEN}✓ Deploy completed!${NC}"
echo "========================================="
echo ""
echo "Application is running at:"
echo "  - Frontend: https://password.huynd.click"
echo "  - API Docs: https://password.huynd.click/docs"
echo "  - Health: https://password.huynd.click/health"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop: docker-compose down"
echo "  - Restart: docker-compose restart"
echo "  - Status: docker-compose ps"
echo ""
