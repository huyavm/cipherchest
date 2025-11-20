# 🚀 Quick Deploy Guide

## 📋 Files Hướng Dẫn

- **DEPLOY_AAPANEL.md** - Hướng dẫn deploy chi tiết trên aaPanel
- **README.md** - Tổng quan về project
- **deploy.sh** - Script tự động deploy
- **nginx.conf** - Cấu hình Nginx mẫu
- **cipherchest.service** - Systemd service file mẫu

## ⚡ Deploy Nhanh trên aaPanel

### 1. Upload code lên server
```bash
cd /www/wwwroot/password.huynd.click/app
git clone <your-repo-url> .
```

### 2. Cài đặt Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Sửa SECRET_KEY, JWT_SECRET_KEY, ENCRYPTION_MASTER_KEY
```

### 3. Build Frontend
```bash
cd frontend
npm install
nano .env  # VITE_API_URL=https://password.huynd.click/api
npm run build
cp -r dist/* /www/wwwroot/password.huynd.click/
```

### 4. Tạo Service
```bash
cp cipherchest.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable cipherchest
systemctl start cipherchest
```

### 5. Cấu hình Nginx
Copy nội dung từ `nginx.conf` vào cấu hình site trong aaPanel

### 6. Deploy lần sau
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📖 Chi Tiết

Xem **DEPLOY_AAPANEL.md** để biết hướng dẫn đầy đủ.
