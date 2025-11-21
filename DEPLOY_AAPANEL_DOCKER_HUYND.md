# Deployment Guide for CipherChest on aaPanel (Docker + Nginx)

This guide will help you deploy CipherChest to your VPS running aaPanel with the domain `huynd.click`.

## Prerequisites

- **VPS** with Ubuntu (or similar Linux OS).
- **aaPanel** installed and running.
- **Docker** Manager installed in aaPanel (or Docker installed manually).
- **Domain** `huynd.click` pointed to your VPS IP.

## Step 1: Prepare the Application

1. **Clone the Repository** to your VPS (e.g., in `/www/wwwroot/password.huynd.click`).

   ```bash
   cd /www/wwwroot/password.huynd.click
   git clone <your-repo-url> .
   ```

2. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and update the values.

   ```bash
   cp .env.example .env
   nano .env
   ```

   **Important**:
   - Change `SECRET_KEY`, `JWT_SECRET_KEY`, `ENCRYPTION_MASTER_KEY`.
   - Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` to your desired admin credentials.

## Step 2: Deploy with Docker

We will use Docker Compose to run both the backend and frontend. The frontend will be built automatically inside a Docker container, so you don't need Node.js installed on your VPS.

1. **Build and Run**:

   ```bash
   docker-compose up -d --build
   ```

   This command will:
   - Build the backend image.
   - Build the frontend image (compile React/Vite app).
   - Start the database (SQLite file in `./data`).
   - Expose the application on port `8080`.

2. **Verify**:
   Check if the containers are running:

   ```bash
   docker-compose ps
   ```

## Step 3: Configure aaPanel Nginx Reverse Proxy

Now we need to tell aaPanel to forward traffic from `huynd.click` to our Docker container running on port `8080`.

1. **Add Site in aaPanel**:
   - Go to **Website** > **Add Site**.
   - Domain: `huynd.click`
   - PHP Version: **Static** (we don't need PHP).
   - Click **Submit**.

2. **Set up Reverse Proxy**:
   - Click on the site name `huynd.click` to open settings.
   - Go to **Reverse Proxy** > **Add Reverse Proxy**.
   - **Name**: `CipherChest`
   - **Target URL**: `http://127.0.0.1:8080`
   - **Sent Domain**: `$host`
   - Click **Submit**.

3. **SSL Certificate** (Optional but Recommended):
   - Go to **SSL** tab in site settings.
   - Select **Let's Encrypt**.
   - Select your domain and click **Apply**.
   - Enable **Force HTTPS**.

## Step 4: Verify Deployment

- Open `https://huynd.click` in your browser.
- You should see the CipherChest login page.
- Log in with the admin credentials you set in `.env`.

## Troubleshooting

- **Logs**: Check logs if something goes wrong.

  ```bash
  docker-compose logs -f
  ```

- **Permissions**: Ensure the `data`, `attachments`, and `backups` directories are writable.

  ```bash
  chmod -R 755 data attachments backups
  ```
