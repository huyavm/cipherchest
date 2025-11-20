# 🐳 Deploy CipherChest với aaPanel Docker Manager

Hướng dẫn deploy Password Manager sử dụng Docker Manager có sẵn trong aaPanel.

---

## 📋 Yêu Cầu

- aaPanel đã cài đặt
- Docker đã được cài qua aaPanel (như trong ảnh bạn đã có)
- Domain đã trỏ về VPS
- Code đã upload lên server

---

## 🚀 Phương Pháp 1: Dùng Docker Compose (Khuyến nghị)

### Bước 1: Upload Code lên Server

#### 1.1. Tạo thư mục project
```bash
mkdir -p /www/wwwroot/password.huynd.click
cd /www/wwwroot/password.huynd.click
```

#### 1.2. Upload code

**Cách 1: Dùng Git**
```bash
git clone https://github.com/your-username/password-manager.git .
```

**Cách 2: Upload qua aaPanel Files**
1. Nén project thành `.zip`
2. Upload qua **Files** → `/www/wwwroot/password.huynd.click`
3. Giải nén

---

### Bước 2: Cấu hình Environment

#### 2.1. Tạo file .env
```bash
cd /www/wwwroot/password.huynd.click
cp .env.example .env
nano .env
```

#### 2.2. Update các giá trị quan trọng
```env
APP_NAME=CipherChest
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CSRF_SECRET=your-csrf-secret-here
ENCRYPTION_MASTER_KEY=your-32-character-key-here
```

**Tạo secret key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 2.3. Cấu hình Frontend
```bash
nano frontend/.env
```

Nội dung:
```env
VITE_API_URL=https://password.huynd.click/api
```

---

### Bước 3: Setup SSL Certificate

#### 3.1. Tạo thư mục SSL
```bash
mkdir -p ssl
```

#### 3.2. Lấy SSL từ aaPanel

1. Vào **Website** → **Add site** với domain `password.huynd.click`
2. **SSL** → **Let's Encrypt** → **Apply**
3. Copy certificate:

```bash
cp /www/server/panel/vhost/cert/password.huynd.click/fullchain.pem ssl/
cp /www/server/panel/vhost/cert/password.huynd.click/privkey.pem ssl/
```

#### 3.3. Hoặc dùng Self-signed (Test)
```bash
cd ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out fullchain.pem \
  -subj "/CN=password.huynd.click"
cd ..
```

---

### Bước 4: Deploy với Docker Compose qua aaPanel

#### 4.1. Vào Docker Manager trong aaPanel

1. Click **Docker** trong sidebar (như trong ảnh)
2. Click tab **Compose**

#### 4.2. Tạo Compose Project mới

1. Click **Add**
2. Điền thông tin:
   - **Project Name**: `cipherchest`
   - **Project Path**: `/www/wwwroot/password.huynd.click`
   - **Compose File**: Chọn `docker-compose.yml` (đã có sẵn trong project)

3. Click **Confirm**

#### 4.3. Start Project

1. Tìm project `cipherchest` trong danh sách
2. Click **Start** (icon play ▶️)
3. Đợi containers build và start

#### 4.4. Xem Logs

1. Click vào project name `cipherchest`
2. Click **Logs** để xem logs của từng container
3. Kiểm tra có lỗi không

---

### Bước 5: Kiểm Tra Deploy

#### 5.1. Kiểm tra containers
Trong aaPanel Docker → Compose → cipherchest, bạn sẽ thấy:
- ✅ `cipherchest-backend` - Running
- ✅ `cipherchest-frontend` - Running  
- ✅ `cipherchest-nginx` - Running

#### 5.2. Test endpoints
```bash
# Health check
curl https://password.huynd.click/health

# Hoặc mở browser:
https://password.huynd.click
https://password.huynd.click/docs
```

---

## 🔧 Phương Pháp 2: Dùng Container Manager (Thủ công)

Nếu không muốn dùng Compose, bạn có thể tạo từng container riêng:

### Bước 1: Build Images

#### 1.1. Vào Docker → Container

1. Click **Container** tab
2. Click **Add**

#### 1.2. Tạo Backend Container

**Cách 1: Build từ Dockerfile**
```bash
cd /www/wwwroot/password.huynd.click
docker build -t cipherchest-backend .
```

**Cách 2: Dùng aaPanel UI**
1. Click **Image** tab → **Build**
2. **Image Name**: `cipherchest-backend`
3. **Dockerfile Path**: `/www/wwwroot/password.huynd.click/Dockerfile`
4. Click **Build**

#### 1.3. Tạo Frontend Container

```bash
cd /www/wwwroot/password.huynd.click/frontend
docker build -t cipherchest-frontend .
```

---

### Bước 2: Tạo Network

1. Click **Network** tab
2. Click **Add**
3. **Network Name**: `cipherchest-network`
4. **Driver**: `bridge`
5. Click **Confirm**

---

### Bước 3: Run Containers

#### 3.1. Run Backend Container

1. Click **Container** tab → **Add**
2. Điền thông tin:
   - **Container Name**: `cipherchest-backend`
   - **Image**: `cipherchest-backend:latest`
   - **Port Mapping**: `8000:8000`
   - **Network**: `cipherchest-network`
   - **Volumes**:
     - `/www/wwwroot/password.huynd.click/attachments:/app/attachments`
     - `/www/wwwroot/password.huynd.click/backups:/app/backups`
     - `/www/wwwroot/password.huynd.click/app.db:/app/app.db`
   - **Environment File**: `/www/wwwroot/password.huynd.click/.env`
   - **Restart Policy**: `unless-stopped`

3. Click **Confirm**

#### 3.2. Run Frontend Container

1. Click **Container** tab → **Add**
2. Điền thông tin:
   - **Container Name**: `cipherchest-frontend`
   - **Image**: `cipherchest-frontend:latest`
   - **Port Mapping**: `5173:80`
   - **Network**: `cipherchest-network`
   - **Restart Policy**: `unless-stopped`

3. Click **Confirm**

#### 3.3. Run Nginx Proxy Container

1. Click **Container** tab → **Add**
2. Điền thông tin:
   - **Container Name**: `cipherchest-nginx`
   - **Image**: `nginx:alpine`
   - **Port Mapping**: 
     - `80:80`
     - `443:443`
   - **Network**: `cipherchest-network`
   - **Volumes**:
     - `/www/wwwroot/password.huynd.click/nginx-proxy.conf:/etc/nginx/conf.d/default.conf:ro`
     - `/www/wwwroot/password.huynd.click/ssl:/etc/nginx/ssl:ro`
   - **Restart Policy**: `unless-stopped`

3. Click **Confirm**

---

## 🎯 Phương Pháp 3: Dùng Terminal (Nhanh nhất)

Nếu bạn quen với terminal:

### Bước 1: SSH vào server
```bash
ssh root@your-vps-ip
```

### Bước 2: Chạy deploy script
```bash
cd /www/wwwroot/password.huynd.click
chmod +x docker-deploy.sh
./docker-deploy.sh
```

**Xong!** Script sẽ tự động:
1. Pull code mới (nếu có Git)
2. Build images
3. Stop containers cũ
4. Start containers mới
5. Kiểm tra health

---

## 🔄 Quản Lý Containers trong aaPanel

### Xem Containers
1. **Docker** → **Container**
2. Xem danh sách containers đang chạy

### Start/Stop/Restart
1. Chọn container
2. Click **Start** / **Stop** / **Restart**

### Xem Logs
1. Click vào container name
2. Click **Logs**
3. Chọn số dòng muốn xem

### Xem Resource Usage
1. **Docker** → **Container**
2. Xem CPU, Memory usage của từng container

### Terminal vào Container
1. Click vào container name
2. Click **Terminal**
3. Chạy lệnh bên trong container

---

## 🔄 Update Application

### Cách 1: Dùng aaPanel UI

1. **Docker** → **Compose**
2. Chọn project `cipherchest`
3. Click **Stop**
4. Upload code mới (qua Files hoặc Git)
5. Click **Rebuild**
6. Click **Start**

### Cách 2: Dùng Script

```bash
cd /www/wwwroot/password.huynd.click
./docker-deploy.sh
```

### Cách 3: Dùng Terminal

```bash
cd /www/wwwroot/password.huynd.click
git pull origin main
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 📊 Monitoring trong aaPanel

### 1. Container Stats
**Docker** → **Container** → Xem CPU, Memory, Network

### 2. Logs
**Docker** → **Container** → Click container → **Logs**

### 3. Images
**Docker** → **Image** → Xem danh sách images và size

### 4. Networks
**Docker** → **Network** → Xem network configuration

### 5. Volumes
**Docker** → **Volume** → Xem persistent data

---

## ❓ Troubleshooting

### Container không start

**Trong aaPanel:**
1. **Docker** → **Container**
2. Click vào container bị lỗi
3. Click **Logs** để xem lỗi
4. Fix lỗi và **Restart**

**Hoặc dùng Terminal:**
```bash
docker-compose logs backend
docker-compose restart backend
```

### Port conflict

**Kiểm tra port:**
```bash
netstat -tulpn | grep :80
netstat -tulpn | grep :443
```

**Fix:**
1. Stop service đang dùng port
2. Hoặc đổi port trong `docker-compose.yml`

### SSL không hoạt động

**Kiểm tra:**
```bash
ls -la /www/wwwroot/password.huynd.click/ssl/
```

**Fix:**
1. Đảm bảo có `fullchain.pem` và `privkey.pem`
2. Restart nginx container

### Database locked

```bash
# Restart backend
docker-compose restart backend
```

### Rebuild từ đầu

**Trong aaPanel:**
1. **Docker** → **Compose**
2. Chọn `cipherchest`
3. Click **Delete** (chọn xóa containers nhưng giữ volumes)
4. Tạo lại project

**Hoặc Terminal:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎯 Workflow Khuyến Nghị

### Lần đầu tiên:

1. ✅ Upload code lên `/www/wwwroot/password.huynd.click`
2. ✅ Cấu hình `.env` và `frontend/.env`
3. ✅ Setup SSL certificate
4. ✅ Vào **Docker** → **Compose** → **Add**
5. ✅ Chọn project path và docker-compose.yml
6. ✅ Click **Start**
7. ✅ Kiểm tra logs và test

### Các lần sau (Update):

**Cách 1: Dùng UI**
1. Stop project
2. Upload code mới
3. Rebuild
4. Start

**Cách 2: Dùng Script** (Nhanh hơn)
```bash
./docker-deploy.sh
```

---

## 💡 Tips

### 1. Backup trước khi update
```bash
docker cp cipherchest-backend:/app/app.db ./backup.db
```

### 2. Xem logs real-time
Trong aaPanel: **Docker** → **Container** → Click container → **Logs** → Enable **Auto Refresh**

### 3. Resource limits
Thêm vào `docker-compose.yml`:
```yaml
backend:
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 512M
```

### 4. Auto-update SSL
Setup cronjob để renew SSL:
```bash
0 0 1 * * certbot renew && cp /etc/letsencrypt/live/password.huynd.click/*.pem /www/wwwroot/password.huynd.click/ssl/ && docker-compose restart nginx
```

### 5. Monitoring
Cài **Monitor** trong aaPanel để theo dõi resource usage

---

## 📞 Hỗ Trợ

### Trong aaPanel:
- **Docker** → **Container** → Xem status
- **Docker** → **Compose** → Xem projects
- **Logs** → Xem system logs

### Terminal:
```bash
# Xem containers
docker ps

# Xem logs
docker-compose logs -f

# Xem resource
docker stats
```

---

## 🎉 Kết Luận

Deploy với **aaPanel Docker Manager** rất tiện lợi vì:

✅ **UI trực quan** - Không cần nhớ lệnh Docker  
✅ **Quản lý dễ dàng** - Start/Stop/Restart bằng click  
✅ **Xem logs** - Real-time logs trong browser  
✅ **Monitoring** - CPU, Memory, Network usage  
✅ **Backup** - Dễ dàng backup containers và volumes  

**Khuyến nghị**: Dùng **Docker Compose** (Phương pháp 1) để quản lý tất cả containers cùng lúc!

---

**Chúc bạn deploy thành công! 🚀**
