# 🐳 Deploy CipherChest với Docker trên aaPanel

Hướng dẫn deploy Password Manager sử dụng Docker và Docker Compose trên aaPanel.

---

## 📋 Yêu Cầu

- VPS Ubuntu 24.04
- aaPanel đã cài đặt
- Docker và Docker Compose
- Domain đã trỏ về VPS (ví dụ: `password.huynd.click`)

---

## 🚀 Bước 1: Cài Đặt Docker trên aaPanel

### 1.1. Cài Docker qua aaPanel

1. Đăng nhập aaPanel: `http://your-vps-ip:7800`
2. **App Store** → Tìm "Docker"
3. Click **Install**
4. Chờ cài đặt hoàn tất

### 1.2. Hoặc cài Docker thủ công

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Start Docker
systemctl start docker
systemctl enable docker

# Install Docker Compose
apt install -y docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 1.3. Thêm user vào Docker group (Tùy chọn)

```bash
usermod -aG docker $USER
newgrp docker
```

---

## 📂 Bước 2: Chuẩn Bị Project

### 2.1. Tạo thư mục project

```bash
mkdir -p /www/wwwroot/password.huynd.click
cd /www/wwwroot/password.huynd.click
```

### 2.2. Upload code

**Cách 1: Dùng Git (Khuyến nghị)**
```bash
git clone https://github.com/your-username/password-manager.git .
```

**Cách 2: Upload qua aaPanel**
1. Nén project thành `password-manager.zip`
2. Upload qua **Files** → `/www/wwwroot/password.huynd.click`
3. Giải nén

**Cách 3: Dùng SCP**
```bash
# Từ máy local
scp -r c:\Antigravity\password-manager root@your-vps-ip:/www/wwwroot/password.huynd.click
```

---

## ⚙️ Bước 3: Cấu Hình Environment

### 3.1. Tạo file .env

```bash
cd /www/wwwroot/password.huynd.click
cp .env.example .env
nano .env
```

### 3.2. Cập nhật các giá trị quan trọng

```env
APP_NAME=CipherChest
DATABASE_URL=sqlite:///./app.db

# QUAN TRỌNG: Tạo secret keys mới cho production
SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
CSRF_SECRET=your-csrf-secret-change-this-in-production
ENCRYPTION_MASTER_KEY=your-32-character-encryption-key-here

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
INACTIVITY_LOCK_MINUTES=15
RATE_LIMIT=20/minute
ATTACHMENTS_DIR=attachments
BACKUP_DIR=backups
LOG_FILE=security.log
```

**Tạo SECRET_KEY ngẫu nhiên:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3.3. Cấu hình Frontend API URL

```bash
nano frontend/.env
```

Nội dung:
```env
VITE_API_URL=https://password.huynd.click/api
```

### 3.4. Tạo thư mục cần thiết

```bash
mkdir -p attachments backups ssl
chmod 755 attachments backups
```

---

## 🔐 Bước 4: Cấu Hình SSL

### 4.1. Lấy SSL Certificate (Let's Encrypt)

**Cách 1: Dùng aaPanel**
1. **Website** → **Add site** với domain `password.huynd.click`
2. **SSL** → **Let's Encrypt** → **Apply**
3. Copy cert files:

```bash
# Copy SSL files từ aaPanel
cp /www/server/panel/vhost/cert/password.huynd.click/fullchain.pem /www/wwwroot/password.huynd.click/ssl/
cp /www/server/panel/vhost/cert/password.huynd.click/privkey.pem /www/wwwroot/password.huynd.click/ssl/
```

**Cách 2: Dùng Certbot**
```bash
apt install -y certbot

# Lấy certificate
certbot certonly --standalone -d password.huynd.click

# Copy vào project
cp /etc/letsencrypt/live/password.huynd.click/fullchain.pem ssl/
cp /etc/letsencrypt/live/password.huynd.click/privkey.pem ssl/
```

### 4.2. Nếu chưa có SSL (Test)

Tạo self-signed certificate tạm thời:
```bash
cd ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out fullchain.pem \
  -subj "/CN=password.huynd.click"
cd ..
```

---

## 🐳 Bước 5: Build và Chạy Docker Containers

### 5.1. Build images

```bash
cd /www/wwwroot/password.huynd.click

# Build tất cả containers
docker-compose build

# Hoặc build từng container
docker-compose build backend
docker-compose build frontend
```

### 5.2. Chạy containers

```bash
# Chạy tất cả containers
docker-compose up -d

# Xem logs
docker-compose logs -f

# Xem logs của container cụ thể
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
```

### 5.3. Kiểm tra containers đang chạy

```bash
docker-compose ps
```

Kết quả mong đợi:
```
NAME                    STATUS          PORTS
cipherchest-backend     Up             
cipherchest-frontend    Up             
cipherchest-nginx       Up             0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

---

## ✅ Bước 6: Kiểm Tra Deploy

### 6.1. Kiểm tra health check

```bash
# Từ server
curl http://localhost/health

# Hoặc từ browser
https://password.huynd.click/health
```

Kết quả: `{"status":"ok"}`

### 6.2. Kiểm tra các endpoints

- **Frontend**: https://password.huynd.click
- **API Docs**: https://password.huynd.click/docs
- **API Redoc**: https://password.huynd.click/redoc
- **Health**: https://password.huynd.click/health

### 6.3. Kiểm tra logs

```bash
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Nginx logs
docker-compose logs nginx

# Theo dõi real-time
docker-compose logs -f
```

---

## 🔄 Bước 7: Quản Lý Containers

### Các lệnh thường dùng

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Restart một container cụ thể
docker-compose restart backend

# Xem logs
docker-compose logs -f

# Xem resource usage
docker stats

# Vào shell của container
docker-compose exec backend bash
docker-compose exec frontend sh

# Rebuild và restart
docker-compose up -d --build

# Xóa tất cả (bao gồm volumes)
docker-compose down -v
```

---

## 🔄 Bước 8: Update & Deploy Mới

### 8.1. Tạo script deploy tự động

```bash
nano /www/wwwroot/password.huynd.click/docker-deploy.sh
```

Nội dung:
```bash
#!/bin/bash

echo "========================================="
echo "CipherChest - Docker Deploy Script"
echo "========================================="
echo ""

cd /www/wwwroot/password.huynd.click

# Pull latest code
echo "[1/5] Pulling latest code..."
git pull origin main

# Rebuild images
echo "[2/5] Rebuilding Docker images..."
docker-compose build

# Stop old containers
echo "[3/5] Stopping old containers..."
docker-compose down

# Start new containers
echo "[4/5] Starting new containers..."
docker-compose up -d

# Wait for health check
echo "[5/5] Waiting for services to be healthy..."
sleep 10

# Check status
docker-compose ps

echo ""
echo "========================================="
echo "Deploy completed!"
echo "========================================="
echo ""
echo "Check status:"
echo "  - Frontend: https://password.huynd.click"
echo "  - Health: https://password.huynd.click/health"
echo "  - Logs: docker-compose logs -f"
echo ""
```

### 8.2. Chạy deploy

```bash
chmod +x docker-deploy.sh
./docker-deploy.sh
```

---

## 🛠️ Bước 9: Cấu Hình aaPanel (Tùy chọn)

### 9.1. Tắt Nginx của aaPanel (nếu conflict port 80/443)

```bash
# Stop nginx của aaPanel
systemctl stop nginx

# Disable auto-start
systemctl disable nginx
```

### 9.2. Hoặc đổi port của Docker nginx

Sửa `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8080:80"
    - "8443:443"
```

Sau đó dùng Nginx của aaPanel làm reverse proxy:
```nginx
server {
    listen 80;
    server_name password.huynd.click;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name password.huynd.click;
    
    ssl_certificate /path/to/ssl/fullchain.pem;
    ssl_certificate_key /path/to/ssl/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📊 Bước 10: Monitoring & Logs

### 10.1. Xem logs real-time

```bash
# Tất cả containers
docker-compose logs -f

# Chỉ backend
docker-compose logs -f backend

# 100 dòng cuối
docker-compose logs --tail=100 backend
```

### 10.2. Kiểm tra resource usage

```bash
# Tất cả containers
docker stats

# Container cụ thể
docker stats cipherchest-backend
```

### 10.3. Inspect container

```bash
docker inspect cipherchest-backend
docker inspect cipherchest-frontend
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

### 2. Backup tự động

Tạo cronjob backup database:
```bash
crontab -e
```

Thêm:
```bash
# Backup database hàng ngày lúc 2 giờ sáng
0 2 * * * docker cp cipherchest-backend:/app/app.db /www/backup/app.db.$(date +\%Y\%m\%d) && find /www/backup -name "app.db.*" -mtime +7 -delete
```

### 3. Auto-restart containers

Containers đã được cấu hình `restart: unless-stopped` trong docker-compose.yml

---

## ❓ Troubleshooting

### Container không start

```bash
# Xem logs
docker-compose logs backend

# Xem chi tiết
docker inspect cipherchest-backend

# Restart
docker-compose restart backend
```

### Port conflict

```bash
# Kiểm tra port đang dùng
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# Stop service đang dùng port
systemctl stop nginx  # Nginx của aaPanel
```

### SSL không hoạt động

```bash
# Kiểm tra SSL files
ls -la ssl/

# Test nginx config
docker-compose exec nginx nginx -t

# Xem nginx logs
docker-compose logs nginx
```

### Database locked

```bash
# Restart backend container
docker-compose restart backend
```

### Rebuild từ đầu

```bash
# Xóa tất cả
docker-compose down -v

# Xóa images
docker rmi $(docker images -q cipherchest*)

# Build lại
docker-compose build --no-cache
docker-compose up -d
```

---

## 📝 Lưu Ý Quan Trọng

1. **Backup database** trước khi update:
   ```bash
   docker cp cipherchest-backend:/app/app.db ./app.db.backup
   ```

2. **Không commit .env** lên Git

3. **Update SSL certificate** trước khi hết hạn (Let's Encrypt: 90 ngày)

4. **Monitor logs** thường xuyên:
   ```bash
   docker-compose logs -f
   ```

5. **Resource limits**: Thêm vào docker-compose.yml nếu cần:
   ```yaml
   backend:
     deploy:
       resources:
         limits:
           cpus: '1'
           memory: 512M
   ```

---

## 🎯 So Sánh: Docker vs Manual Deploy

| Tiêu chí | Docker | Manual |
|----------|--------|--------|
| **Dễ cài đặt** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Dễ update** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Tách biệt** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Resource** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Debug** | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Khuyến nghị** | ✅ Cho production | ✅ Cho development |

---

## 📞 Hỗ Trợ

- **Logs**: `docker-compose logs -f`
- **Status**: `docker-compose ps`
- **Health**: `https://password.huynd.click/health`
- **API Docs**: `https://password.huynd.click/docs`

---

**Chúc bạn deploy thành công với Docker! 🎉**
