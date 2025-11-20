# 🎯 Quick Start: Deploy với aaPanel Docker UI

Hướng dẫn nhanh deploy CipherChest sử dụng giao diện Docker trong aaPanel.

---

## 📋 Chuẩn Bị

1. ✅ aaPanel đã cài Docker (như trong ảnh bạn đã có)
2. ✅ Code đã upload lên `/www/wwwroot/password.huynd.click`
3. ✅ Domain đã trỏ về VPS

---

## 🚀 5 Bước Deploy Nhanh

### **Bước 1: Upload Code**

**Qua aaPanel Files:**
1. Vào **Files** trong aaPanel
2. Navigate đến `/www/wwwroot/`
3. Tạo thư mục `password.huynd.click`
4. Upload file `.zip` của project
5. Click chuột phải → **Extract**

**Hoặc qua Terminal:**
```bash
cd /www/wwwroot/password.huynd.click
git clone https://github.com/your-username/password-manager.git .
```

---

### **Bước 2: Cấu Hình Environment**

**Qua aaPanel Files:**
1. Navigate đến `/www/wwwroot/password.huynd.click`
2. Copy `.env.example` → `.env`
3. Click chuột phải `.env` → **Edit**
4. Update các giá trị:
   ```env
   SECRET_KEY=<tạo-key-mới>
   JWT_SECRET_KEY=<tạo-key-mới>
   ENCRYPTION_MASTER_KEY=<32-ký-tự>
   ```
5. Save

**Tạo secret key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Cấu hình Frontend:**
1. Edit `frontend/.env`:
   ```env
   VITE_API_URL=https://password.huynd.click/api
   ```

---

### **Bước 3: Setup SSL**

**Cách 1: Dùng aaPanel SSL Manager**
1. **Website** → **Add site** với domain `password.huynd.click`
2. Click vào site → **SSL** → **Let's Encrypt**
3. Click **Apply**
4. Copy certificate:
   ```bash
   mkdir -p /www/wwwroot/password.huynd.click/ssl
   cp /www/server/panel/vhost/cert/password.huynd.click/fullchain.pem /www/wwwroot/password.huynd.click/ssl/
   cp /www/server/panel/vhost/cert/password.huynd.click/privkey.pem /www/wwwroot/password.huynd.click/ssl/
   ```

**Cách 2: Self-signed (Test)**
```bash
cd /www/wwwroot/password.huynd.click
mkdir ssl
cd ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout privkey.pem -out fullchain.pem -subj "/CN=password.huynd.click"
```

---

### **Bước 4: Deploy với Docker Compose**

#### **Trong aaPanel UI:**

1. Click **Docker** trong sidebar (như ảnh bạn gửi)

2. Click tab **Compose**

3. Click nút **Add** (góc trên bên phải)

4. Điền form:
   - **Project Name**: `cipherchest`
   - **Project Path**: `/www/wwwroot/password.huynd.click`
   - **Compose File**: `docker-compose.yml` (chọn từ dropdown)
   - **Description**: `CipherChest Password Manager`

5. Click **Confirm**

6. Tìm project `cipherchest` trong danh sách

7. Click nút **Start** (▶️ icon)

8. Đợi build và start (có thể mất 2-5 phút lần đầu)

---

### **Bước 5: Kiểm Tra**

#### **Trong aaPanel:**

1. **Docker** → **Compose** → Click vào `cipherchest`

2. Xem status của 3 containers:
   - ✅ `cipherchest-backend` - Should be "Running"
   - ✅ `cipherchest-frontend` - Should be "Running"
   - ✅ `cipherchest-nginx` - Should be "Running"

3. Click **Logs** để xem logs

#### **Test trong Browser:**

1. Mở: `https://password.huynd.click`
2. Mở: `https://password.huynd.click/docs`
3. Mở: `https://password.huynd.click/health` → Kết quả: `{"status":"ok"}`

---

## 🔄 Update Application

### **Khi có code mới:**

#### **Cách 1: Dùng aaPanel UI**

1. **Docker** → **Compose**
2. Chọn project `cipherchest`
3. Click **Stop**
4. Upload code mới (qua Files hoặc Git pull)
5. Click **Rebuild**
6. Click **Start**

#### **Cách 2: Dùng Script (Nhanh hơn)**

```bash
cd /www/wwwroot/password.huynd.click
./docker-deploy.sh
```

---

## 🛠️ Quản Lý Containers

### **Xem Logs:**
1. **Docker** → **Container**
2. Click vào container name (ví dụ: `cipherchest-backend`)
3. Click **Logs**
4. Chọn số dòng (100, 500, 1000)
5. Enable **Auto Refresh** để xem real-time

### **Restart Container:**
1. **Docker** → **Container**
2. Chọn container
3. Click **Restart**

### **Stop/Start:**
1. **Docker** → **Compose**
2. Chọn project `cipherchest`
3. Click **Stop** hoặc **Start**

### **Xem Resource Usage:**
1. **Docker** → **Container**
2. Xem cột CPU%, Memory%

---

## ❓ Troubleshooting

### **Container không start:**

1. **Docker** → **Container**
2. Click vào container bị lỗi
3. Click **Logs**
4. Đọc error message
5. Fix và **Restart**

### **Port 80/443 bị chiếm:**

**Kiểm tra:**
```bash
netstat -tulpn | grep :80
netstat -tulpn | grep :443
```

**Fix:**
```bash
# Stop Nginx của aaPanel nếu conflict
systemctl stop nginx
systemctl disable nginx
```

### **SSL không hoạt động:**

**Kiểm tra files:**
```bash
ls -la /www/wwwroot/password.huynd.click/ssl/
```

Phải có 2 files:
- `fullchain.pem`
- `privkey.pem`

### **Rebuild từ đầu:**

1. **Docker** → **Compose**
2. Chọn `cipherchest`
3. Click **Delete**
4. Chọn **Delete containers only** (giữ volumes/data)
5. Tạo lại project (Bước 4)

---

## 💡 Tips

### **1. Backup Database:**
```bash
docker cp cipherchest-backend:/app/app.db /www/backup/app.db.$(date +%Y%m%d)
```

### **2. Xem Logs Real-time:**
Trong aaPanel: **Docker** → **Container** → Click container → **Logs** → Enable **Auto Refresh**

### **3. Terminal vào Container:**
1. **Docker** → **Container**
2. Click vào container
3. Click **Terminal**
4. Chạy lệnh bên trong container

### **4. Monitor Resources:**
Cài **Monitor** app trong aaPanel để theo dõi CPU, RAM, Disk

---

## 📸 Screenshots Workflow

### **1. Docker → Compose → Add:**
![Add Compose Project](https://i.imgur.com/example1.png)

### **2. Fill Project Info:**
- Project Name: `cipherchest`
- Project Path: `/www/wwwroot/password.huynd.click`
- Compose File: `docker-compose.yml`

### **3. Start Project:**
Click ▶️ button

### **4. Check Status:**
All containers should show "Running" status

---

## 🎯 Checklist

Trước khi deploy, đảm bảo:

- [ ] Code đã upload đầy đủ
- [ ] File `.env` đã cấu hình đúng
- [ ] File `frontend/.env` đã có `VITE_API_URL`
- [ ] SSL certificate đã có trong thư mục `ssl/`
- [ ] Docker đã cài trong aaPanel
- [ ] Domain đã trỏ về VPS
- [ ] Port 80, 443 không bị chiếm

---

## 📞 Hỗ Trợ

**Xem logs:**
- aaPanel: **Docker** → **Container** → Click container → **Logs**
- Terminal: `docker-compose logs -f`

**Xem status:**
- aaPanel: **Docker** → **Container**
- Terminal: `docker-compose ps`

**Restart:**
- aaPanel: **Docker** → **Compose** → Click **Restart**
- Terminal: `docker-compose restart`

---

**Chúc bạn deploy thành công! 🎉**

Nếu gặp vấn đề, hãy:
1. Xem logs trong aaPanel
2. Kiểm tra `.env` configuration
3. Đảm bảo SSL files tồn tại
4. Restart containers
