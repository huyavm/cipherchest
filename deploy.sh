#!/bin/bash

echo "========================================="
echo "CipherChest - Quick Deploy Script"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
APP_DIR="/www/wwwroot/password.huynd.click/app"
WEB_ROOT="/www/wwwroot/password.huynd.click"
SERVICE_NAME="cipherchest"

cd $APP_DIR

# Step 1: Pull latest code
echo -e "${YELLOW}[1/7]${NC} Pulling latest code from Git..."
git pull origin main
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Git pull failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

# Step 2: Update backend dependencies
echo -e "${YELLOW}[2/7]${NC} Updating backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt --upgrade
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Backend dependencies update failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Backend dependencies updated${NC}"
echo ""

# Step 3: Update frontend dependencies
echo -e "${YELLOW}[3/7]${NC} Updating frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Frontend dependencies update failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Frontend dependencies updated${NC}"
echo ""

# Step 4: Build frontend
echo -e "${YELLOW}[4/7]${NC} Building frontend..."
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Frontend build failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Frontend built successfully${NC}"
echo ""

# Step 5: Deploy frontend
echo -e "${YELLOW}[5/7]${NC} Deploying frontend..."
cd ..
rm -rf $WEB_ROOT/*.html $WEB_ROOT/assets
cp -r frontend/dist/* $WEB_ROOT/
echo -e "${GREEN}✓ Frontend deployed${NC}"
echo ""

# Step 6: Restart backend service
echo -e "${YELLOW}[6/7]${NC} Restarting backend service..."
systemctl restart $SERVICE_NAME
sleep 2
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✓ Backend service restarted${NC}"
else
    echo -e "${RED}✗ Backend service failed to start!${NC}"
    systemctl status $SERVICE_NAME
    exit 1
fi
echo ""

# Step 7: Reload Nginx
echo -e "${YELLOW}[7/7]${NC} Reloading Nginx..."
nginx -t && systemctl reload nginx
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Nginx reload failed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Nginx reloaded${NC}"
echo ""

# Success
echo "========================================="
echo -e "${GREEN}✓ Deploy completed successfully!${NC}"
echo "========================================="
echo ""
echo "Application is running at:"
echo "  - Frontend: https://password.huynd.click"
echo "  - API Docs: https://password.huynd.click/docs"
echo "  - Health: https://password.huynd.click/health"
echo ""

# Check health
echo "Checking health..."
sleep 2
curl -s https://password.huynd.click/health
echo ""
