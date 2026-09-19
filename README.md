# StudentDesk 🎓

**Student Management System** — ek complete DevOps pipeline ke saath.
`Developer → Git → CI (Jenkins / GitHub Actions) → Build & Test → Docker Image → Deploy → Monitoring`

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![Tests](https://img.shields.io/badge/tests-33%20passed-brightgreen)
![Docker](https://img.shields.io/badge/Docker-enabled-2496ED)

---

## ✨ Features

| Module | Details |
|---|---|
| 🔐 Login | Simple session-based admin login (`admin` / `admin123`) |
| 📊 Dashboard | Total students, active count, pass rate, average marks, course distribution |
| 👨‍🎓 Student CRUD | Add / Edit / Delete / Search / Filter by course |
| 🧮 Auto Grade | Marks se grade (A+ … F) aur PASS/FAIL result |
| 🔌 REST API | `/api/students`, `/api/students/<id>`, `/api/stats` |
| ❤️ Health Check | `/health` — Docker healthcheck, Jenkins smoke test, Prometheus ke liye |
| ✅ 33 Tests | Unit + Integration (UI) + API tests, `pytest` se |

---

## 🛠️ Tech Stack

- **Language / Framework:** Python 3.12 + Flask
- **Database:** SQLite (SQLAlchemy ORM) — zero setup
- **Testing:** pytest
- **Version Control:** Git + GitHub
- **CI/CD:** Jenkins (Jenkinsfile) **aur** GitHub Actions
- **Container:** Docker + Docker Compose
- **Server:** Gunicorn
- **Config Mgmt:** Ansible
- **Monitoring:** Prometheus + Grafana + Node Exporter
- **Logs:** Docker logs / Loki (optional)

---

## 🚀 Quick Start (Local)

```bash
# 1. Repo clone karo
git clone https://github.com/YOUR_USERNAME/studentdesk.git
cd studentdesk

# 2. Virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 4. App chalao
python run.py
```

Ab browser me kholo → **http://localhost:5000**
Login: `admin` / `admin123`

### Tests chalana

```bash
pytest -v                      # sab tests
pytest tests/test_unit.py -v   # sirf unit tests
```

---

## 🐳 Docker

```bash
# Image build
docker build -t studentdesk:1.0.0 .

# Container run
docker run -d --name studentdesk -p 5000:5000 studentdesk:1.0.0

# Check
curl http://localhost:5000/health
docker logs -f studentdesk

# Band karna
docker stop studentdesk && docker rm studentdesk
```

### Docker Compose (app + monitoring ek saath)

```bash
docker compose up -d app                             # sirf app
docker compose --profile monitoring up -d            # app + Prometheus + Grafana
docker compose ps
docker compose logs -f
docker compose down
```

---

## 🔁 Jenkins Pipeline

`Jenkinsfile` repo ke root me hai. Stages:

```
Checkout → Setup Python Env → Build → Unit Tests → App & API Tests
        → Docker Build → Smoke Test → Docker Push → Deploy
```

Setup ke complete steps: [`docs/JENKINS_SETUP.md`](docs/JENKINS_SETUP.md)

---

## 📁 Project Structure

```
studentdesk/
├── app/
│   ├── __init__.py            # Flask app factory
│   ├── config.py              # Environment based config
│   ├── models.py              # Student, User (SQLAlchemy)
│   ├── seed.py                # Sample data
│   ├── routes/
│   │   ├── main.py            # Pages (dashboard, students, CRUD)
│   │   ├── auth.py            # Login / Logout
│   │   └── api.py             # JSON REST API
│   ├── templates/             # Jinja2 HTML
│   └── static/css/style.css   # UI styling
├── tests/
│   ├── conftest.py            # pytest fixtures
│   ├── test_unit.py           # Grade logic tests
│   ├── test_app.py            # UI / route tests
│   └── test_api.py            # REST API tests
├── jenkins/Jenkinsfile.docker # Jenkins ko Docker me chalane ka compose
├── ansible/                   # VM provisioning + deploy playbook
├── monitoring/                # Prometheus + Grafana config
├── .github/workflows/         # GitHub Actions CI/CD
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
├── run.py
└── docs/                      # Step-by-step guides
```

---

## 📚 Documentation

| File | Kya hai |
|---|---|
| ⭐ [`docs/GUIDE_HINGLISH.md`](docs/GUIDE_HINGLISH.md) | **MAIN GUIDE** — zero se complete pipeline, step-by-step Hinglish (~2900 lines) |
| [`docs/QUICKSTART.md`](docs/QUICKSTART.md) | 15-minute fast start (cheat sheet) |
| [`docs/JENKINS_SETUP.md`](docs/JENKINS_SETUP.md) | Jenkins install + pipeline + troubleshooting |
| [`docs/ANSIBLE_SETUP.md`](docs/ANSIBLE_SETUP.md) | Ansible playbooks + idempotency + vault |
| [`docs/MONITORING.md`](docs/MONITORING.md) | Prometheus + Grafana + Loki + logs |
| [`docs/REPORT_TEMPLATE.md`](docs/REPORT_TEMPLATE.md) | College report ka ready-to-fill template |
| [`docs/SCREENSHOT_CHECKLIST.md`](docs/SCREENSHOT_CHECKLIST.md) | 43 screenshots ki checklist |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | Har possible error + fix |
| [`docs/VIVA_QUESTIONS.md`](docs/VIVA_QUESTIONS.md) | Viva/demo revision sheet |

## ⚡ Quick Commands

```bash
bash setup.sh --run          # venv + deps + tests + app start
make help                    # saare available commands
make test                    # pytest
make docker                  # image build
make compose-monitoring      # app + Prometheus + Grafana
make jenkins-up              # Jenkins in Docker
make ansible-all             # provision + deploy + monitoring
```

---

## 👤 Demo Credentials

| | |
|---|---|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ Ye sirf demo ke liye hai. Real deployment me strong password + `.env` file use karo.

---

## 📄 License

MIT — education purpose ke liye free to use.
