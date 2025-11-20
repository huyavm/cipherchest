# 🚀 Deploy CipherChest trên aaPanel

Hướng dẫn deploy Password Manager lên VPS Ubuntu 24.04 với aaPanel.

---

## 📋 Yêu Cầu

- VPS Ubuntu 24.04
- aaPanel đã cài đặt
- Domain đã trỏ về VPS (ví dụ: `password.huynd.click`)
- Python 3.9+
- Node.js 16+

---

## 🎯 Tổng Quan Kiến Trúc

```
Nginx (Reverse Proxy)
  ├── Frontend (Static files) → /www/wwwroot/password.huynd.click/dist
  └── Backend API (/api/*) → http://127.0.0.1:8000
```

---

## 📦 Bước 1: Chuẩn Bị VPS

### 1.1. Kết nối SSH
```bash
ssh root@your-vps-ip
```

### 1.2. Cài đặt Python 3.9+ (nếu chưa có)
```bash
# Kiểm tra version
python3 --version

# Nếu < 3.9, cài đặt:
apt update
apt install -y python3.11 python3.11-venv python3-pip
```

### 1.3. Cài đặt Node.js 18+ (nếu chưa có)
```bash
# Cài Node.js 18 LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Kiểm tra
node --version
npm --version
```

---

## 🌐 Bước 2: Tạo Website trong aaPanel

### 2.1. Đăng nhập aaPanel
Truy cập: `http://your-vps-ip:7800`

### 2.2. Tạo Website mới
1. **Website** → **Add site**
2. Điền thông tin:
   - **Domain**: `password.huynd.click`
   - **Root directory**: `/www/wwwroot/password.huynd.click`
   - **PHP Version**: Không cần (chọn Pure static)
   - **Database**: Không cần (dùng SQLite)
3. Click **Submit**

### 2.3. Cấu hình SSL (Khuyến nghị)
1. **Website** → Chọn site vừa tạo → **SSL**
2. Chọn **Let's Encrypt**
3. Click **Apply**

---

## 📂 Bước 3: Upload Code lên Server

### 3.1. Tạo thư mục project
```bash
cd /www/wwwroot/password.huynd.click
mkdir app
cd app
```

### 3.2. Upload code

**Cách 1: Dùng Git (Khuyến nghị)**
```bash
# Clone repository
git clone https://github.com/your-username/password-manager.git .

# Hoặc nếu đã có Git repo
git init
git remote add origin https://github.com/your-username/password-manager.git
git pull origin main
```

**Cách 2: Dùng aaPanel File Manager**
1. Nén toàn bộ project thành `password-manager.zip`
2. Upload qua **Files** → `/www/wwwroot/password.huynd.click/app`
3. Giải nén

**Cách 3: Dùng SCP/SFTP**
```bash
# Từ máy local
scp -r c:\Antigravity\password-manager root@your-vps-ip:/www/wwwroot/password.huynd.click/app
```

---

## ⚙️ Bước 4: Cấu Hình Backend

### 4.1. Tạo môi trường ảo Python
```bash
cd /www/wwwroot/password.huynd.click/app
python3 -m venv venv
source venv/bin/activate
```

### 4.2. Cài đặt dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4.3. Tạo file .env
```bash
cp .env.example .env
nano .env
```

Sửa các giá trị sau:
```env
APP_NAME=CipherChest
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key-change-this-in-production-12345678
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production-87654321
CSRF_SECRET=your-csrf-secret-change-this-in-production
ENCRYPTION_MASTER_KEY=your-32-character-encryption-key-here-1234567890ab
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
INACTIVITY_LOCK_MINUTES=15
RATE_LIMIT=20/minute
ATTACHMENTS_DIR=attachments
BACKUP_DIR=backups
LOG_FILE=security.log
```

**Lưu ý**: Tạo SECRET_KEY ngẫu nhiên:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4.4. Tạo database
```bash
# Database sẽ tự động được tạo khi chạy app lần đầu
# Hoặc chạy thủ công:
python3 -c "from database.init_db import init_db; init_db()"
```

### 4.5. Tạo thư mục cần thiết
```bash
mkdir -p attachments backups
chmod 755 attachments backups
```

---

## 🎨 Bước 5: Build Frontend

### 5.1. Cài đặt dependencies
```bash
cd frontend
npm install
```

### 5.2. Cấu hình API URL
```bash
nano .env
```

Nội dung:
```env
VITE_API_URL=https://password.huynd.click/api
```

### 5.3. Build production
```bash
npm run build
```

### 5.4. Copy build sang thư mục web root
```bash
cd ..
cp -r frontend/dist/* /www/wwwroot/password.huynd.click/
```

---

## 🔧 Bước 6: Tạo Service cho Backend

### 6.1. Tạo file systemd service
```bash
nano /etc/systemd/system/cipherchest.service
```

Nội dung:
```ini
[Unit]
Description=CipherChest Password Manager Backend
After=network.target

[Service]
Type=simple
User=www
Group=www
WorkingDirectory=/www/wwwroot/password.huynd.click/app
Environment="PATH=/www/wwwroot/password.huynd.click/app/venv/bin"
ExecStart=/www/wwwroot/password.huynd.click/app/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6.2. Enable và start service
```bash
systemctl daemon-reload
systemctl enable cipherchest
systemctl start cipherchest
systemctl status cipherchest
```

### 6.3. Kiểm tra backend
```bash
curl http://127.0.0.1:8000/health
# Kết quả: {"status":"ok"}
```

---

## 🌐 Bước 7: Cấu Hình Nginx

### 7.1. Mở cấu hình Nginx trong aaPanel
1. **Website** → Chọn site → **Config**
2. Hoặc edit trực tiếp:
```bash
nano /www/server/panel/vhost/nginx/password.huynd.click.conf
```

### 7.2. Thay thế nội dung bằng:
```nginx
server {
    listen 80;
    listen 443 ssl http2;
    server_name password.huynd.click;
    
    # SSL Configuration (nếu đã cài SSL)
    ssl_certificate /www/server/panel/vhost/cert/password.huynd.click/fullchain.pem;
    ssl_certificate_key /www/server/panel/vhost/cert/password.huynd.click/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Root directory cho frontend
    root /www/wwwroot/password.huynd.click;
    index index.html;
    
    # Logs
    access_log /www/wwwlogs/password.huynd.click.log;
    error_log /www/wwwlogs/password.huynd.click.error.log;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Backend API proxy
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # API docs
    location /docs {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /redoc {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /openapi.json {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000;
        access_log off;
    }
    
    # Frontend - SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Deny access to sensitive files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location ~ /\.env {
        deny all;
    }
    
    # Force HTTPS redirect
    if ($scheme != "https") {
        return 301 https://$server_name$request_uri;
    }
}
```

### 7.3. Test và reload Nginx
```bash
nginx -t
systemctl reload nginx
```

---

## ✅ Bước 8: Kiểm Tra Deploy

### 8.1. Kiểm tra Backend
```bash
# Health check
curl https://password.huynd.click/health

# API docs
curl https://password.huynd.click/docs
```

### 8.2. Kiểm tra Frontend
Mở browser: `https://password.huynd.click`

### 8.3. Kiểm tra logs
```bash
# Backend logs
journalctl -u cipherchest -f

# Nginx logs
tail -f /www/wwwlogs/password.huynd.click.log
tail -f /www/wwwlogs/password.huynd.click.error.log
```

---

## 🔄 Bước 9: Script Deploy Tự Động

Tạo script để deploy nhanh khi có update:

```bash
nano /www/wwwroot/password.huynd.click/deploy.sh
```

Nội dung:
```bash
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
```

Chmod và chạy:
```bash
chmod +x /www/wwwroot/password.huynd.click/deploy.sh
/www/wwwroot/password.huynd.click/deploy.sh
```

---

## 🛠️ Quản Lý & Bảo Trì

### Restart Backend
```bash
systemctl restart cipherchest
```

### Xem Logs Backend
```bash
journalctl -u cipherchest -f
```

### Xem Logs Nginx
```bash
tail -f /www/wwwlogs/password.huynd.click.log
```

### Backup Database
```bash
cp /www/wwwroot/password.huynd.click/app/app.db /www/backup/app.db.$(date +%Y%m%d_%H%M%S)
```

### Update Code
```bash
cd /www/wwwroot/password.huynd.click/app
git pull
/www/wwwroot/password.huynd.click/deploy.sh
```

---

## 🔒 Bảo Mật

### 1. Firewall
```bash
# Chỉ mở port cần thiết
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 7800/tcp  # aaPanel (nếu cần)
ufw enable
```

### 2. Fail2ban (Tùy chọn)
```bash
apt install fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

### 3. Backup tự động
Tạo cronjob backup database hàng ngày:
```bash
crontab -e
```

Thêm dòng:
```
0 2 * * * cp /www/wwwroot/password.huynd.click/app/app.db /www/backup/app.db.$(date +\%Y\%m\%d) && find /www/backup -name "app.db.*" -mtime +7 -delete
```

---

## ❓ Troubleshooting

### Backend không start
```bash
# Xem logs
journalctl -u cipherchest -n 50

# Kiểm tra port
netstat -tulpn | grep 8000

# Test thủ công
cd /www/wwwroot/password.huynd.click/app
source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Frontend không load
```bash
# Kiểm tra file
ls -la /www/wwwroot/password.huynd.click/index.html

# Kiểm tra Nginx config
nginx -t

# Xem Nginx logs
tail -f /www/wwwlogs/password.huynd.click.error.log
```

### API 502 Bad Gateway
```bash
# Kiểm tra backend đang chạy
systemctl status cipherchest

# Kiểm tra port 8000
curl http://127.0.0.1:8000/health
```

### Database locked
```bash
# Restart backend
systemctl restart cipherchest
```

---

## 📞 Hỗ Trợ

- **Logs Backend**: `journalctl -u cipherchest -f`
- **Logs Nginx**: `/www/wwwlogs/password.huynd.click.error.log`
- **API Docs**: `https://password.huynd.click/docs`

---

**Chúc bạn deploy thành công! 🎉**
