# 📚 Deployment Documentation Index

Chọn phương pháp deploy phù hợp với nhu cầu của bạn.

---

## 🐳 Deploy với Docker (Khuyến nghị)

**File**: `DEPLOY_DOCKER.md`

### Ưu điểm:
- ✅ Dễ cài đặt và deploy
- ✅ Tách biệt môi trường
- ✅ Dễ dàng rollback
- ✅ Nhất quán giữa dev và production
- ✅ Auto-restart khi server reboot

### Phù hợp cho:
- Production deployment
- Team có nhiều người
- Cần scale dễ dàng
- Muốn CI/CD automation

### Quick Start:
```bash
# 1. Cài Docker trên aaPanel
# 2. Upload code
git clone <repo-url> /www/wwwroot/password.huynd.click
cd /www/wwwroot/password.huynd.click

# 3. Cấu hình
cp .env.example .env
nano .env  # Update secrets

# 4. Deploy
chmod +x docker-deploy.sh
./docker-deploy.sh
```

**Xem chi tiết**: [DEPLOY_DOCKER.md](DEPLOY_DOCKER.md)

---

## 🎨 Deploy với aaPanel Docker UI (Dễ nhất)

**File**: `QUICK_DEPLOY_AAPANEL.md` và `DEPLOY_AAPANEL_DOCKER.md`

### Ưu điểm:
- ✅ Giao diện trực quan, không cần terminal
- ✅ Quản lý containers bằng click chuột
- ✅ Xem logs real-time trong browser
- ✅ Monitor CPU, Memory dễ dàng
- ✅ Phù hợp cho người mới

### Phù hợp cho:
- Người mới bắt đầu với Docker
- Không quen dùng terminal/SSH
- Muốn UI trực quan
- Cần monitor dễ dàng

### Quick Start:
```bash
# 1. Upload code qua aaPanel Files
# 2. Cấu hình .env qua Files Editor
# 3. Vào Docker → Compose → Add
#    - Project Name: cipherchest
#    - Project Path: /www/wwwroot/password.huynd.click
#    - Compose File: docker-compose.yml
# 4. Click Start
```

**Xem chi tiết**: 
- [QUICK_DEPLOY_AAPANEL.md](QUICK_DEPLOY_AAPANEL.md) - Hướng dẫn ngắn gọn
- [DEPLOY_AAPANEL_DOCKER.md](DEPLOY_AAPANEL_DOCKER.md) - Hướng dẫn đầy đủ

---

## 🔧 Deploy Manual (Không dùng Docker)

**File**: `DEPLOY_AAPANEL.md`

### Ưu điểm:
- ✅ Kiểm soát tốt hơn
- ✅ Ít resource hơn
- ✅ Dễ debug
- ✅ Không cần Docker

### Phù hợp cho:
- VPS có resource hạn chế
- Muốn kiểm soát chi tiết
- Đã quen với systemd
- Development/Testing

### Quick Start:
```bash
# 1. Cài Python, Node.js
# 2. Setup Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Build Frontend
cd frontend
npm install
npm run build

# 4. Setup Service
cp cipherchest.service /etc/systemd/system/
systemctl enable cipherchest
systemctl start cipherchest

# 5. Configure Nginx
# Copy nginx.conf vào aaPanel
```

**Xem chi tiết**: [DEPLOY_AAPANEL.md](DEPLOY_AAPANEL.md)

---

## ⚡ Quick Reference

**File**: `DEPLOY_QUICK.md`

Tham khảo nhanh các lệnh deploy cho cả 2 phương pháp.

---

## 📋 So Sánh Phương Pháp

| Tiêu chí | Docker | Manual |
|----------|--------|--------|
| **Dễ cài đặt** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Dễ update** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Resource usage** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Tách biệt** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Debug** | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Rollback** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **CI/CD** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 Khuyến Nghị

### Cho Production:
👉 **Dùng Docker** - Xem `DEPLOY_DOCKER.md`

### Cho Development:
👉 **Dùng Manual** hoặc Docker local

### Cho VPS nhỏ (<2GB RAM):
👉 **Dùng Manual** - Xem `DEPLOY_AAPANEL.md`

---

## 📂 Files Deployment

```
password-manager/
├── DEPLOY_DOCKER.md          # 🐳 Docker deployment (Recommended)
├── DEPLOY_AAPANEL.md         # 🔧 Manual deployment
├── DEPLOY_QUICK.md           # ⚡ Quick reference
├── DEPLOYMENT_INDEX.md       # 📚 This file
│
├── docker-compose.yml        # Docker compose config
├── Dockerfile                # Backend Docker image
├── docker-deploy.sh          # Docker deploy script
├── .dockerignore             # Docker ignore rules
│
├── deploy.sh                 # Manual deploy script
├── nginx.conf                # Nginx config (manual)
├── nginx-proxy.conf          # Nginx proxy (Docker)
├── cipherchest.service       # Systemd service
│
└── frontend/
    ├── Dockerfile            # Frontend Docker image
    └── nginx-docker.conf     # Frontend nginx config
```

---

## 🚀 Bắt Đầu Ngay

### Bước 1: Chọn phương pháp
- **Docker**: Đọc `DEPLOY_DOCKER.md`
- **Manual**: Đọc `DEPLOY_AAPANEL.md`

### Bước 2: Chuẩn bị
- VPS Ubuntu 24.04
- aaPanel đã cài
- Domain đã trỏ về VPS

### Bước 3: Deploy
- Follow hướng dẫn trong file tương ứng
- Chạy script deploy

### Bước 4: Kiểm tra
- Frontend: `https://your-domain.com`
- API Docs: `https://your-domain.com/docs`
- Health: `https://your-domain.com/health`

---

## 💡 Tips

1. **Luôn backup** trước khi deploy:
   ```bash
   # Docker
   docker cp cipherchest-backend:/app/app.db ./backup.db
   
   # Manual
   cp app.db backup.db
   ```

2. **Test local** trước khi deploy production

3. **Dùng Git** để quản lý code

4. **Monitor logs** thường xuyên

5. **Update SSL** trước khi hết hạn

---

## 📞 Hỗ Trợ

### Docker:
```bash
docker-compose logs -f
docker-compose ps
```

### Manual:
```bash
journalctl -u cipherchest -f
systemctl status cipherchest
```

### Nginx:
```bash
nginx -t
tail -f /www/wwwlogs/password.huynd.click.error.log
```

---

**Chúc bạn deploy thành công! 🎉**
