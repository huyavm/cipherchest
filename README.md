# CipherChest Password Manager

A secure password vault built with FastAPI, SQLAlchemy, Tailwind CSS, and React. It supports granular tagging, AES-256 encryption for sensitive records, JWT auth with refresh tokens, CSRF protection, and extensive tooling (password generator, TOTP QR builder, HaveIBeenPwned check, CSV export, encrypted backups, and more).

## Features

- 🔐 **Security-first backend**: hashed passwords (bcrypt), AES-256 encryption for credentials, attachments, and backups. Master password verification included.
- 🔑 **Auth stack**: FastAPI + JWT access/refresh tokens, CSRF double-submit header, auto logout after inactivity (frontend + backend) and per-IP rate limiting.
- 📥 **Account manager**: CRUD for Gmail/email, SaaS/web, hosting/cloud, payment/social accounts with tagging, metadata, notes, expiration tracking, and encrypted attachment uploads.
- 🧰 **Security tools**: strong password generator, TOTP secret + QR builder, HaveIBeenPwned lookup.
- 💾 **Backup/Import**: encrypted JSON backup, CSV export per account type, restore workflow.
- 📊 **Dashboard**: KPI cards (totals, expiring accounts, accounts without 2FA, category distribution).
- 🧱 **Clean architecture**: dedicated `/api`, `/models`, `/schemas`, `/services`, `/database`, `/security`, `/utils`, `/frontend` folders.

## Project Structure

```
.
├── api/                # FastAPI routers
├── database/           # DB session utilities + schema definition
├── models/             # SQLAlchemy models (users, accounts, attachments, logs...)
├── schemas/            # Pydantic schemas
├── security/           # Hashing, JWT, CSRF, AES, rate limiter
├── services/           # Business logic (accounts, auth, backups, dashboard)
├── utils/              # Settings, password generator, TOTP, HIBP, file crypto
├── frontend/           # React + Tailwind UI
├── attachments/        # Encrypted upload storage (gitignored)
├── backups/            # Encrypted backup output (gitignored)
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

## Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # adjust secrets + DB path
touch app.db
python database/init_db.py
uvicorn main:app --reload
```

The API becomes available at `http://localhost:8000`. Interactive docs live at `/docs`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev # http://localhost:5173 with proxy to the API
```

## Docker

### Development
```bash
cp .env.example .env
docker-compose up --build
```

### Production (aaPanel)
See **DEPLOY_DOCKER.md** for detailed instructions.

Quick start:
```bash
chmod +x docker-deploy.sh
./docker-deploy.sh
```

Access:
- Frontend: `https://your-domain.com`
- Backend API: `https://your-domain.com/api`
- API Docs: `https://your-domain.com/docs`

## Deployment

- **DEPLOY_DOCKER.md** - Deploy with Docker on aaPanel (Recommended)
- **DEPLOY_AAPANEL.md** - Manual deploy on aaPanel
- **DEPLOY_QUICK.md** - Quick reference guide

## Environment Variables

See `.env.example` for all tunables (JWT keys, AES key, rate limit, inactivity timeout, attachment paths, SMTP/Telegram hooks).

## Database Schema

`database/schema.sql` contains the SQL definition for all tables. The runtime app uses SQLAlchemy to create/update tables automatically via `database/init_db.py`.

## Testing The Flow

1. Register or login (default admin: `admin@local` / `ChangeMe123!`).
2. Add Gmail/hosting/payment accounts with tags, notes, and sensitive fields.
3. Upload encrypted invoices/SSH keys via the attachment modal.
4. Generate passwords/TOTP or run HaveIBeenPwned checks inside **Tools**.
5. Export encrypted JSON backup (Backup tab) and CSV per account type.
6. Restore backups using the passphrase you defined.

## Security Notes

- Sensitive JSON payloads and file attachments are encrypted with AES-256 GCM using the master key from `.env`.
- JWT access tokens are short-lived; refresh tokens tracked via `token_sessions` table with revoke-on-logout.
- CSRF header (`csrf-token`) is required for mutating requests. The frontend stores+injects it automatically.
- Inactivity lock is enforced on both client (auto logout) and server (backend denies if last activity exceeded `INACTIVITY_LOCK_MINUTES`).
- Rate limiter blocks abusive IPs per the `RATE_LIMIT` window (default `20/minute`).
- Security events (login/logout/register) recorded in `security_logs` for audit/alert integrations.

## Backup & Import

- `/api/backup/export` → returns base64 AES blob (store offline).
- `/api/backup/import` → restore from blob + passphrase.
- `/api/backup/csv/{type}` → CSV view for a specific account class (email/web/cloud/payment/other).

## Frontend UX Highlights

- Sidebar navigation + dark mode aesthetic.
- Dashboard cards & analytics, filterable accounts table, responsive layout optimized for mobile.
- Modal-driven create/edit/delete flows with confirmation prompts.
- Backup, restore, password generator, TOTP QR, and breach checker from a dedicated Tools view.

## Logging & Monitoring

Security logs saved in DB (and optionally file/Telegram/email hooks via `.env`). Extend `services/security_log_service` to route alerts to your SOC tooling.
