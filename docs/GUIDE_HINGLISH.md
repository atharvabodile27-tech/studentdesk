# 🎓 StudentDesk — Complete DevOps Project Guide (Hinglish, Beginner Friendly)

> **TAE-II Submission Deadline: 28 September 2026**
>
> Ye guide padh ke tum **zero se lekar working end-to-end DevOps pipeline** tak jaoge.
> Har step me bataya gaya hai — **kahan jaana hai, kya karna hai, kaise karna hai, aur kaise verify karna hai.**

---

## 📑 Table of Contents

| # | Section | Kya seekhoge | Time |
|---|---------|--------------|------|
| 0 | [Project kya banana hai](#0-project-kya-banana-hai) | Scope, tools, accounts | 10 min |
| 1 | [Environment Setup](#1-environment-setup) | Git, Python, Docker install | 45 min |
| 2 | [Application samjho & local pe chalao](#2-application-samjho--local-pe-chalao) | Flask app run karna | 20 min |
| 3 | [Tests chalao](#3-tests-chalao) | pytest, 35 tests | 15 min |
| 4 | [Git & GitHub](#4-git--github) | Repo banana, push karna | 40 min |
| 5 | [Docker](#5-docker) | Image build, container run | 45 min |
| 6 | [Jenkins Pipeline](#6-jenkins-pipeline) | CI/CD automation | 90 min |
| 7 | [GitHub Actions](#7-github-actions-free-wala-cicd) | Free CI/CD | 30 min |
| 8 | [Cloud Deployment](#8-cloud-deployment) | VM pe deploy | 60 min |
| 9 | [Ansible](#9-ansible) | Config management | 60 min |
| 10 | [Monitoring & Logs](#10-monitoring--log-management) | Prometheus + Grafana | 45 min |
| 11 | [Screenshots & Report](#11-screenshots--report) | Submission material | 45 min |
| 12 | [Viva Questions](#12-viva--demo-questions) | Answer taiyaari | 30 min |
| 13 | [Troubleshooting](#13-troubleshooting) | Errors fix | as needed |
| 14 | [Day-wise Plan](#14-day-wise-plan-aaj-se-28-september-tak) | Schedule | 5 min |

---

## 0. Project kya banana hai

### 0.1 Ek line me

Ek **Student Management System** (web app) banani hai aur usko ek **automated DevOps pipeline** pe chalana hai:

```
Developer (tum)
    ↓ code likha
Git Repository (GitHub)
    ↓ push kiya
CI Server (Jenkins / GitHub Actions)
    ↓ automatically
Build & Test (pytest — 35 tests)
    ↓ sab pass hue
Docker Image (container banaya)
    ↓ registry pe push
Deployment (VM / Cloud)
    ↓ app live
Monitoring (Prometheus + Grafana)
```

### 0.2 Kaun-kaun se tools chahiye

| Tool | Kaam | Cost | Install kahan |
|---|---|---|---|
| **Git + GitHub** | Version control, code hosting | Free | Apna laptop |
| **Python 3.11+** | App language | Free | Apna laptop |
| **Docker Desktop** | Containerization | Free (personal) | Apna laptop |
| **Jenkins** | CI/CD automation (build + test) | Free/Open source | Docker container **ya** VM |
| **Ansible** | Config management + deploy | Free/Open source | Apna laptop |
| **Cloud VM** | Deployment target | Free tier available | Oracle / AWS / VirtualBox |
| **Prometheus + Grafana** | Monitoring + dashboards | Free/Open source | VM (Docker me) |

### 0.3 Accounts bana lo (sab free hain) — 15 minute ka kaam

> ⚠️ **Sab accounts ke liye ek hi email use karo** — college wali email best rahegi.

**1. GitHub** → https://github.com/signup
- Username simple rakho (jaise `rahul-sharma-dev`) — ye report me jayega
- Email verify karo
- 2FA (two-factor auth) enable kar lo — authenticator app se

**2. Docker Hub** → https://hub.docker.com/signup
- Username = GitHub username hi rakho (confusion nahi hoga)
- Free account me **1 public repository unlimited** milta hai — hamare liye kaafi hai

**3. Jenkins** — account nahi chahiye, ye software hai. Section 6 me install karenge.

**4. Cloud VM (koi ek choose karo):**

| Option | Free kya milta hai | Difficulty | Recommendation |
|---|---|---|---|
| **Oracle Cloud Free Tier** | 2 AMD VMs (1/8 OCPU, 1GB RAM) — **hamesha free** | Medium | ⭐⭐⭐⭐⭐ Best |
| **AWS EC2** | t2.micro — 12 mahine free, 750 hrs/month | Medium | ⭐⭐⭐⭐ |
| **GitHub Codespaces** | 120 core-hours/month free | Easy | ⭐⭐⭐⭐ |
| **VirtualBox (apne laptop pe)** | Unlimited | Easy | ⭐⭐⭐ (agar internet/cloud me dikkat ho) |
| **Render / Railway** | Free web hosting (Docker support) | Very Easy | ⭐⭐⭐⭐ (agar VM na mile) |

> 💡 **Mera suggestion:** Oracle Cloud ya AWS EC2 pe Ubuntu 22.04/24.04 VM lo. Agar credit card dene me problem ho to **VirtualBox** me Ubuntu VM bana lo — pipeline same hi rahega, sirf IP change hoga.

### 0.4 Folder structure jo hum banayenge

Tumhare laptop pe ek folder banao, jaise `~/DevOps-Project/`. Iske andar ye sab hoga:

```
DevOps-Project/
└── studentdesk/              ← ye pura project (tumhe ready-made mil gaya hai)
    ├── app/                  ← Flask application code
    ├── tests/                ← 35 pytest tests
    ├── docs/                 ← ye saari guides
    ├── ansible/              ← Ansible playbooks
    ├── monitoring/           ← Prometheus + Grafana config
    ├── jenkins/              ← Jenkins ko Docker me chalane ka compose
    ├── .github/workflows/    ← GitHub Actions CI/CD
    ├── Dockerfile            ← Container recipe
    ├── docker-compose.yml    ← Multi-container setup
    ├── Jenkinsfile           ← Jenkins pipeline
    ├── requirements.txt      ← Python dependencies
    └── run.py                ← App entry point
```

---

## 1. Environment Setup

> Ye section **ek hi baar** karna hai. Windows / Mac / Linux — teeno ke commands diye hain.

### 1.1 Git install karo

**Windows:**
1. Jao → https://git-scm.com/download/win
2. Download apne aap shuru ho jayega. Installer chalao.
3. Har screen pe **default options** rakho, bas "Next Next Next Finish".
4. Install ke baad **Git Bash** open karo (Start menu me search karo).

**Mac:**
```bash
# Terminal kholo aur ye likho
git --version
# Agar install nahi hai to Xcode Command Line Tools ka popup aayega → "Install" dabao
# Ya Homebrew se:
brew install git
```

**Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install -y git curl
```

**Verify (teeno OS pe):**
```bash
git --version
# Output: git version 2.4x.x
```

**Git ko apne naam se configure karo** (ye bahut zaroori hai — commit me naam dikhega):
```bash
git config --global user.name "Tumhara Naam"
git config --global user.email "tumhari-email@example.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input      # Mac/Linux
# Windows pe:  git config --global core.autocrlf true

# Check karo
git config --list | grep user
```

### 1.2 Python install karo

**Windows:**
1. Jao → https://www.python.org/downloads/
2. "Download Python 3.12.x" dabao
3. ⚠️ **SABSE ZAROORI:** Installer ke pehle screen pe **"Add python.exe to PATH"** checkbox **TICK karo**. Ye bhool gaye to sab kuch fail hoga.
4. "Install Now" dabao.

**Mac:**
```bash
brew install python@3.12
# ya python.org se installer download karo
```

**Linux:**
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
```

**Verify:**
```bash
python --version      # Windows
python3 --version     # Mac / Linux
# Output: Python 3.12.x

pip --version         # Windows
pip3 --version        # Mac / Linux
```

> 📝 **Note:** Linux/Mac pe hamesha `python3` aur `pip3` likhna. Windows pe `python` aur `pip` chalta hai. Is guide me main `python3` likhunga — Windows wale `python` samajh lena.

### 1.3 Docker Desktop install karo

**Windows / Mac:**
1. Jao → https://www.docker.com/products/docker-desktop/
2. "Download for Windows" ya "Download for Mac"
3. Installer chalao, default options.
4. Install ke baad **Docker Desktop app kholo** aur wait karo jab tak neeche-left corner me green "Engine running" na aa jaye.

> ⚠️ **Windows pe:** Docker Desktop ko **WSL 2** chahiye. Agar error aaye to:
> - PowerShell **as Administrator** kholo → `wsl --install` chalao → PC restart karo
> - Phir Docker Desktop install karo

> ⚠️ **Mac (M1/M2/M3 chip):** "Apple Silicon" wala version download karo.

**Linux:**
```bash
# Official Docker script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Apne user ko docker group me daalo (sudo ke bina docker chalane ke liye)
sudo usermod -aG docker $USER
newgrp docker        # ya logout/login karo

# Service start
sudo systemctl enable --now docker
```

**Verify:**
```bash
docker --version
# Docker version 27.x.x

docker run hello-world
# "Hello from Docker!" message aana chahiye
```

### 1.4 VS Code install karo (editor)

1. Jao → https://code.visualstudio.com/
2. Install karo.
3. Open karke ye **extensions** install karo (left sidebar ke squares icon → search):

| Extension | Kyun |
|---|---|
| **Python** (Microsoft) | Python support, run/debug |
| **Docker** (Microsoft) | Dockerfile editing, container management |
| **GitLens** | Git history dekhna |
| **YAML** (Red Hat) | docker-compose / Ansible files |
| **Ansible** (Red Hat) | Ansible syntax highlighting |
| **Jinja** | Flask templates |

### 1.5 Ansible install karo

> ⚠️ **Ansible Windows pe natively nahi chalta.** Windows users ke liye 3 options:
> - **WSL2** (recommended) — Windows ke andar Linux
> - **Git Bash** me pip se install (kuch cheezein fail ho sakti hain)
> - **VM ke andar se hi** Ansible chalao

**Mac / Linux / WSL:**
```bash
# Option 1: pip se (sabse easy)
pip3 install ansible

# Option 2: apt se (Ubuntu)
sudo apt install -y ansible

# Verify
ansible --version
# ansible [core 2.1x.x]
```

**Windows pe WSL install karna:**
```powershell
# PowerShell (Administrator) me
wsl --install -d Ubuntu
# Restart karo, Ubuntu open karo, username/password set karo
# Ab Ubuntu terminal ke andar: sudo apt update && sudo apt install -y ansible python3-pip
```

### 1.6 Sab kuch ek saath verify karo

Terminal kholo aur ye chalao:

```bash
echo "=== Meri DevOps Toolchain ==="
git --version
python3 --version
docker --version
docker compose version
ansible --version | head -1
echo "=============================="
```

Agar sab versions print hue → **Section 1 complete! 🎉**

---

## 2. Application samjho & local pe chalao

### 2.1 Project folder lo

Tumhare paas 2 options hain:

**Option A — Project ready-made copy hai (tumhare workspace me):**
```bash
cd ~/DevOps-Project      # ya jahan rakhna hai
cp -r /path/to/studentdesk .
cd studentdesk
```

**Option B — Khud scratch se banao (seekhne ke liye best):**
Naya folder banao aur `docs/` ke saath saath files copy karo. Har file ka matlab niche samjhaya hai.

### 2.2 Virtual environment banao

> **Virtual environment kyun?** Har project ki apni dependencies hoti hain. Venv se wo system Python se alag rehti hain — conflicts nahi hote.

```bash
cd studentdesk

# Venv banao
python3 -m venv venv

# Activate karo:
source venv/bin/activate          # Mac / Linux / Git Bash
venv\Scripts\activate             # Windows CMD
venv\Scripts\Activate.ps1         # Windows PowerShell

# Agar PowerShell me error aaye "scripts cannot be loaded":
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# phir dobara activate karo
```

Activate hone ke baad prompt me `(venv)` dikhega:
```
(venv) rahul@laptop:~/studentdesk$
```

### 2.3 Dependencies install karo

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Kya install hua:**

| Package | Kaam |
|---|---|
| `Flask` | Web framework (Python me web app banane ka tarika) |
| `Flask-SQLAlchemy` | Database ORM (SQL query likhne ki zaroorat nahi) |
| `SQLAlchemy` | Database engine |
| `Werkzeug` | Password hashing, WSGI utilities |
| `gunicorn` | Production web server (Docker me yahi chalega) |
| `pytest` | Testing framework |
| `prometheus_client` | Monitoring metrics |

### 2.4 App chalao! 🚀

```bash
python run.py
```

Output aisa dikhega:
```
 * Serving Flask app 'run'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.5:5000
Press CTRL+C to quit
```

**Browser me kholo → http://localhost:5000**

Login karo:
- Username: `admin`
- Password: `admin123`

### 2.5 App me kya kya kar sakte ho (ek baar try karke dekho)

| Page | Kya karo |
|---|---|
| **Dashboard** | Stats dekho — total students, pass rate, average marks |
| **Students** | 6 sample students ki list. Search box me "Aarav" type karo. Course filter try karo. |
| **+ Add Student** | Naya student add karo. Roll No `TEST001`, marks `95` daalo → Grade A+ aayega |
| **Edit** | Kisi student ke marks change karo → grade apne aap badal jayega |
| **Delete** | Ek student delete karo (confirm popup aayega) |
| **API** (navbar) | JSON data dikhega — `/api/students` |
| **Health** (navbar) | `{"status": "ok", ...}` — ye endpoint Docker/Jenkins ke liye hai |

### 2.6 Validation check karo (ye tests ke liye important hai)

Try karo aur dekho app sahi behave karti hai:
- Marks me `150` daalo → error flash hona chahiye: *"Marks 0 se 100 ke beech hone chahiye"*
- Same Roll No dobara daalo → *"Ye Roll Number pehle se exist karta hai"*
- Marks me `abc` daalo → error
- Bina login ke `/students` kholo → login page pe redirect

App band karna: terminal me **Ctrl+C** dabao.

### 2.7 Code kaise kaam karta hai (viva ke liye zaroori)

```
run.py                     ← Entry point. create_app() call karta hai
  └── app/__init__.py      ← App factory: DB init, blueprints register, /health, /metrics
        ├── config.py      ← Environment variables se settings (SECRET_KEY, DATABASE_URL)
        ├── models.py      ← Student + User tables, grade()/result() logic
        ├── seed.py        ← 6 sample students + admin user
        ├── metrics.py     ← Prometheus metrics (/metrics endpoint)
        └── routes/
              ├── main.py  ← HTML pages (dashboard, list, add, edit, delete)
              ├── auth.py  ← Login / Logout
              └── api.py   ← JSON REST API (/api/...)
```

**3 concepts jo viva me poochenge:**

1. **App Factory Pattern** — `create_app()` function se app banti hai. Fayda: tests me alag config (`TestConfig`) ke saath dusri app bana sakte ho bina global state ke.

2. **Blueprint** — Flask me routes ko modules me baantne ka tarika. `main_bp`, `auth_bp`, `api_bp` — teeno alag files me, phir `register_blueprint()` se app me jod diye.

3. **Environment variables** — Code me password/secret hardcode nahi karte. `os.environ.get("SECRET_KEY")` se padhte hain. Isse same image dev/staging/prod me chal sakti hai, sirf env vars badalte hain. Ye **12-Factor App** principle hai.

---

## 3. Tests chalao

> **DevOps ka golden rule:** Agar test nahi hai to automation nahi ho sakta. Jenkins isi ko check karke aage badhta hai.

### 3.1 Tests run karo

```bash
# Venv activate hona chahiye
pytest -v
```

Output:
```
tests/test_unit.py::TestGradeCalculation::test_grade_a_plus PASSED
tests/test_unit.py::TestGradeCalculation::test_grade_a PASSED
...
tests/test_metrics.py::test_metrics_contains_app_data_when_available PASSED
==================================== 35 passed in 3.70s ====================================
```

### 3.2 Teen tarah ke tests hain — samjho

| File | Type | Kya test karta hai | Count |
|---|---|---|---|
| `test_unit.py` | **Unit Test** | `grade()` aur `result()` logic — DB/web nahi chahiye | 12 |
| `test_app.py` | **Integration Test** | HTML pages, login, form submit, search, delete | 13 |
| `test_api.py` | **API Test** | JSON endpoints — 200/201/400/404/409 status codes | 9 |
| `test_metrics.py` | **Feature Test** | `/metrics` endpoint graceful hai | 2 |

**Total: 35 tests** ✅ (exact count thoda alag ho sakta hai)

### 3.3 Fixtures kya hoti hain (`conftest.py`)

```python
@pytest.fixture(scope="function")
def app():
    app = create_app(TestConfig)      # in-memory SQLite DB
    with app.app_context():
        _db.create_all()
        yield app                     # test ko app de diya
        _db.session.remove()
        _db.drop_all()                # test ke baad saaf
```

- **`TestConfig`** use hoti hai → DB `sqlite:///:memory:` — matlab RAM me. Real DB file gandi nahi hoti.
- **`scope="function"`** → har test ko fresh DB milti hai. Ek test ka data dusre ko affect nahi karta.
- **`auth_client`** fixture → pehle login kar deta hai, phir test chalata hai.

### 3.4 Test report generate karo (Jenkins isi ko padhta hai)

```bash
mkdir -p reports
pytest -v --junitxml=reports/results.xml

# Report dekho
cat reports/results.xml | head -20
```

Ye **JUnit XML format** hai — Jenkins, GitHub Actions, GitLab CI sab isi ko samajhte hain.

### 3.5 Jaan-boojh kar test fail karo (demo ke liye best trick!)

Viva/demo me dikhana ki "pipeline failure detect karta hai" — ye karo:

```bash
# models.py me grade() function kholo aur 90 ko 95 kar do
# (ya koi bhi ek value badal do)
pytest tests/test_unit.py -v
# Output: FAILED  tests/test_unit.py::TestGradeCalculation::test_grade_a_plus
```

Phir `git commit` karke push karo → **Jenkins/GitHub Actions build FAIL ho jayega**. Screenshot lo, phir code wapas theek kar do → build PASS.

> 💡 **Ye screenshot report me sabse zyada marks dilata hai** — kyunki isse prove hota hai ki pipeline actually kuch check kar rahi hai, sirf "green tick" nahi dikha rahi.

---

## 4. Git & GitHub

### 4.1 Git ke 5 commands jo 95% kaam karte hain

```bash
git status              # kya change hua
git add .               # sab changes stage karo
git commit -m "message" # snapshot lo
git push                # GitHub pe bhejo
git pull                # GitHub se lao
```

### 4.2 GitHub pe repository banao

1. Jao → https://github.com/new
2. Fill karo:
   - **Repository name:** `studentdesk` (ya `devops-student-management`)
   - **Description:** `Student Management System with complete DevOps pipeline — Git, Jenkins, Docker, Ansible, Prometheus & Grafana`
   - **Visibility:** **Public** ✅ (submission ke liye link dena hai; private rakha to professor access nahi kar payenge)
   - ⚠️ **IMPORTANT:** "Add a README file", ".gitignore", "license" — **kuch bhi tick MAT karo**. Repo bilkul khali honi chahiye, warna conflict aayega.
3. **Create repository** dabao.

Tumhe ek page dikhega jisme commands honge. Wahan se **repo URL** copy karo:
```
https://github.com/YOUR_USERNAME/studentdesk.git
```

### 4.3 Local repo banao aur push karo

```bash
cd studentdesk

# 1. Git repo initialize karo
git init
git branch -M main

# 2. Check karo kya kya jayega
git status

# 3. Sab add karo
git add .

# 4. Pehla commit
git commit -m "feat: initial StudentDesk app with Flask, tests, Docker and CI/CD config"

# 5. Remote (GitHub) connect karo  ← apna URL daalo!
git remote add origin https://github.com/YOUR_USERNAME/studentdesk.git

# 6. Push karo
git push -u origin main
```

**Push ke time login kaise hoga?**
- Popup aayega → "Sign in with your browser" choose karo
- Ya **Personal Access Token** use karo:
  GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token → `repo` scope tick → token copy
  Password ki jagah wo token paste karo.

### 4.4 Verify karo

Browser me apni repo kholo. Ye sab dikhna chahiye:
- `app/`, `tests/`, `docs/`, `ansible/`, `monitoring/` folders
- `Dockerfile`, `Jenkinsfile`, `docker-compose.yml`, `README.md`
- Right side me "1 Commit", "main branch"

⚠️ **Check karo ki ye files NAHI gayi:** `venv/`, `instance/*.db`, `__pycache__/`, `.env`
Agar chali gayi hain:
```bash
git rm -r --cached venv instance __pycache__
git commit -m "chore: remove accidentally committed files"
git push
```

### 4.5 Branch strategy (thoda professional banao)

Sirf `main` pe kaam karna theek hai college project ke liye, lekin **ek feature branch** bana ke dikhao to extra marks:

```bash
# Naya feature branch
git checkout -b feature/add-attendance-module

# Kuch change karo (jaise README me ek line add karo)
echo "- Attendance tracking (planned)" >> README.md

git add README.md
git commit -m "docs: add attendance to roadmap"
git push -u origin feature/add-attendance-module
```

Ab GitHub pe jao → repo me ek yellow banner dikhega: **"Compare & pull request"** → dabao → **Create pull request**.

PR page pe GitHub Actions automatically tests chala dega (Section 7). Green tick aane ke baad **Merge pull request** dabao.

```bash
# Local pe merge sync karo
git checkout main
git pull
git branch -d feature/add-attendance-module
```

### 4.6 Commit message convention (report me achha lagta hai)

| Prefix | Kab use karo | Example |
|---|---|---|
| `feat:` | Naya feature | `feat: add student search filter` |
| `fix:` | Bug fix | `fix: marks validation for negative values` |
| `docs:` | Documentation | `docs: add Jenkins setup guide` |
| `test:` | Tests | `test: add API error case coverage` |
| `chore:` | Config/misc | `chore: update Dockerfile base image` |
| `ci:` | Pipeline changes | `ci: add CodeQL security scan` |

### 4.7 Useful Git commands (zaroorat padne par)

```bash
git log --oneline --graph -10      # history dekho
git diff                            # unstaged changes
git diff --staged                   # staged changes
git checkout -- file.py             # ek file wapas lao
git reset --soft HEAD~1             # last commit undo (changes rakho)
git stash                           # changes temporarily side me rakho
git stash pop                       # wapas lao
git clone <url>                     # dusri machine pe repo lao
```

---

## 5. Docker

### 5.1 Docker kya hai — 2 line me

Docker tumhari app ko ek **container** me pack kar deta hai — code + Python + libraries + OS ke zaroori hisse, sab ek saath. Phir wo container **kahin bhi same chalega**: tumhara laptop, Jenkins, VM, cloud. "Mere machine pe to chal raha tha" wali problem khatam.

```
Dockerfile  --(docker build)-->  Image  --(docker run)-->  Container
  (recipe)                        (pakka hua khana)          (serve ho raha khana)
```

### 5.2 Hamara Dockerfile samjho (line by line)

`studentdesk/Dockerfile` kholo. Ye hai:

```dockerfile
FROM python:3.12-slim
```
→ **Base image.** Already Python 3.12 installed Linux (Debian slim). `slim` = chhota size (~130MB vs full ~900MB). Chhoti image = fast build, fast push, fast deploy.

```dockerfile
LABEL maintainer="student@example.com"
LABEL app="studentdesk"
LABEL version="1.0.0"
```
→ Metadata. `docker inspect` se dikhta hai.

```dockerfile
WORKDIR /app
```
→ Container ke andar ka working folder. Ab sab commands `/app` me chalengi. (`cd /app` + `mkdir -p /app` ek saath).

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```
→ **LAYER CACHING ka trick — viva question!**
Pehle sirf `requirements.txt` copy kiya, dependencies install ki, **uske baad** code copy karenge.
Fayda: Agar tum sirf `app/models.py` badlo, to Docker cache se pichhla layer use karega — **pip install dobara nahi chalega**. Build 3 minute se 15 second pe aa jayega.

`--no-cache-dir` → pip ka download cache image me nahi rakhta → image chhoti hoti hai.

```dockerfile
COPY . .
```
→ Ab baaki code. (`.dockerignore` wali files nahi aayengi.)

```dockerfile
RUN mkdir -p /app/instance && chmod -R 777 /app/instance
```
→ SQLite DB file ke liye folder + write permission.

```dockerfile
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser
```
→ **Security best practice.** Container root ke andar nahi chalega. Agar koi attacker container me ghus bhi jaye to uske paas root nahi hoga. Ye line report me highlight karna.

```dockerfile
EXPOSE 5000
```
→ Documentation: "app 5000 port pe sunegi". (Actual port mapping `docker run -p` se hoti hai.)

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=4).status==200 else 1)"
```
→ Docker khud har 30 second me `/health` hit karega. Fail hua to container status `(unhealthy)` dikhega. `--start-period=10s` → shuru ke 10 second me fail count nahi hoga (app ko boot hone ka time).

```dockerfile
ENV FLASK_APP=run.py PORT=5000 PYTHONUNBUFFERED=1
```
→ `PYTHONUNBUFFERED=1` **bahut zaroori hai** — isse logs turant dikhte hain, buffer me nahi rukte. Warna `docker logs` me output late aayega.

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", \
     "--access-logfile", "-", "--error-logfile", "-", "run:app"]
```
→ **Container start hone pe kya chalega.**
- `gunicorn` = production WSGI server (Flask ka built-in server sirf development ke liye hai)
- `--workers 2 --threads 4` = 8 concurrent requests handle kar sakta hai
- `--access-logfile -` = logs **stdout** pe jao (Docker inhe capture karta hai — ye 12-factor logging hai)
- `run:app` = `run.py` file ka `app` object

### 5.3 Image build karo

```bash
cd studentdesk

docker build -t studentdesk:1.0.0 .
```

⚠️ **End ka `.` (dot) bhoolna mat** — wo build context hai (kaunsa folder Docker ko bhejna hai).

Output:
```
[+] Building 45.2s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [1/6] FROM docker.io/library/python:3.12-slim
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt .
 => [4/6] RUN pip install ...
 => [5/6] COPY . .
 => [6/6] RUN useradd ...
 => exporting to image
 => => naming to docker.io/library/studentdesk:1.0.0
```

**Verify:**
```bash
docker images | grep studentdesk
# studentdesk   1.0.0   a1b2c3d4e5f6   2 minutes ago   245MB
```

> 💡 **Dobara build karoge to fast hoga** (cache ki wajah se). Ye dekh ke layer caching samajh aayega:
> ```bash
> docker build -t studentdesk:1.0.0 .
> # => [4/6] RUN pip install ...  CACHED
> ```

### 5.4 Container chalao

```bash
docker run -d --name studentdesk -p 5000:5000 studentdesk:1.0.0
```

| Flag | Matlab |
|---|---|
| `-d` | detached — background me chalega, terminal free rahega |
| `--name studentdesk` | Container ka naam (baad me `docker stop studentdesk` kar sakte ho) |
| `-p 5000:5000` | Port mapping — **host:container**. Laptop ka 5000 → container ka 5000 |

**Verify (4 tarike):**

```bash
# 1. Container chal raha hai?
docker ps
# CONTAINER ID   IMAGE              STATUS                    PORTS                    NAMES
# abc123...      studentdesk:1.0.0  Up 10 seconds (healthy)   0.0.0.0:5000->5000/tcp   studentdesk

# 2. Health check
curl http://localhost:5000/health
# {"app":"StudentDesk","status":"ok","version":"1.0.0"}

# 3. Logs dekho (gunicorn access logs dikhenge)
docker logs -f studentdesk
# Ctrl+C se bahar aao

# 4. Container ke andar jhanko
docker exec -it studentdesk sh
ls -la
python --version
exit
```

**Browser me kholo → http://localhost:5000** — same app, ab container me chal rahi hai 🎉

### 5.5 Container lifecycle commands (ye yaad kar lo)

```bash
docker ps                        # chalte hue containers
docker ps -a                     # sab (band bhi)
docker logs -f studentdesk       # live logs
docker logs --tail 50 studentdesk # last 50 lines
docker stop studentdesk          # gracefully band
docker start studentdesk         # wapas start
docker restart studentdesk       # restart
docker rm -f studentdesk         # force remove
docker stats studentdesk         # live CPU/RAM usage
docker inspect studentdesk       # full JSON details
docker exec -it studentdesk sh   # container ke andar shell
```

### 5.6 Environment variables ke saath chalao

```bash
docker run -d --name studentdesk \
  -p 5000:5000 \
  -e SECRET_KEY="mera-super-secret-key" \
  -e APP_VERSION="2.0.0" \
  studentdesk:1.0.0

curl http://localhost:5000/health
# {"app":"StudentDesk","status":"ok","version":"2.0.0"}   ← version badal gaya!
```

**Ye prove karta hai:** ek hi image, alag config. **Same image dev → test → production** ja sakti hai. Ye DevOps ka core principle hai.

### 5.7 Data persist karo (volumes)

Container delete karne par andar ka data bhi chala jata hai. SQLite DB bachane ke liye **volume**:

```bash
docker rm -f studentdesk

# Named volume ke saath
docker run -d --name studentdesk \
  -p 5000:5000 \
  -v studentdesk_data:/app/instance \
  studentdesk:1.0.0

# Volume list
docker volume ls
docker volume inspect studentdesk_data
```

Ab container delete karke dobara banao — students ka data bacha rahega:
```bash
docker rm -f studentdesk
docker run -d --name studentdesk -p 5000:5000 -v studentdesk_data:/app/instance studentdesk:1.0.0
curl http://localhost:5000/api/stats
# purana data wahi hai ✅
```

### 5.8 Docker Compose — sab kuch ek command me

Compose = multiple containers ko ek YAML file se manage karna.

```bash
# Sirf app
docker compose up -d app

# App + Prometheus + Grafana + Node Exporter (pura monitoring stack)
docker compose --profile monitoring up -d

# Kya chal raha hai
docker compose ps

# Logs
docker compose logs -f
docker compose logs -f app

# Band karo
docker compose down

# Volumes bhi delete karke band karo (fresh start)
docker compose down -v
```

Compose up hone ke baad:

| URL | Kya hai | Login |
|---|---|---|
| http://localhost:5000 | App | admin / admin123 |
| http://localhost:9090 | Prometheus | — |
| http://localhost:3000 | Grafana | admin / admin123 |
| http://localhost:9100/metrics | Node Exporter | — |

### 5.9 Image Docker Hub pe push karo

**Step 1: Docker Hub pe login (terminal se)**
```bash
docker login
# Username: tumhara Docker Hub username
# Password: tumhara Docker Hub password (ya Access Token)
# "Login Succeeded" aana chahiye
```

**Step 2: Image ko tag karo**
```bash
# Format: dockerhub-username/image-name:tag
docker tag studentdesk:1.0.0 YOUR_DOCKERHUB_USERNAME/studentdesk:1.0.0
docker tag studentdesk:1.0.0 YOUR_DOCKERHUB_USERNAME/studentdesk:latest
```

**Step 3: Push karo**
```bash
docker push YOUR_DOCKERHUB_USERNAME/studentdesk:1.0.0
docker push YOUR_DOCKERHUB_USERNAME/studentdesk:latest
```

**Step 4: Verify** → https://hub.docker.com/r/YOUR_USERNAME/studentdesk
Image dikhegi, "Public", tags `1.0.0` aur `latest`.

> 🎓 **Ye screenshot report me zaroor daalo** — Docker Hub pe tumhari image ka page.

**Ab koi bhi machine pe sirf ye command se app chal jayegi:**
```bash
docker run -d -p 5000:5000 YOUR_DOCKERHUB_USERNAME/studentdesk:latest
```

> 💡 **Alternative: GitHub Container Registry (ghcr.io)** — Docker Hub ki rate limit se bachne ke liye. GitHub Actions workflow me already configured hai (Section 7).

### 5.10 Multi-stage build (bonus — extra marks ke liye)

Agar image aur chhoti karni ho. `Dockerfile.multistage` banao:

```dockerfile
# ---- Stage 1: Builder ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Stage 2: Runtime (sirf zaroori cheezein) ----
FROM python:3.12-slim AS runtime
WORKDIR /app
RUN useradd --create-home appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]
```

```bash
docker build -f Dockerfile.multistage -t studentdesk:slim .
docker images | grep studentdesk
# Normal:  245MB
# slim:    ~180MB   ← chhoti!
```

---

## 6. Jenkins Pipeline

> **Jenkins = automation ka boss.** Jab bhi tum GitHub pe code push karoge, Jenkins apne aap:
> code layega → dependencies install karega → tests chalega → Docker image banayega → deploy karega.
> Aur agar koi test fail hua to **deployment rok dega** aur tumhe bata dega.

### 6.1 Jenkins install karo — 2 tarike

#### 🟢 TARIKA A: Docker me (Sabse aasan — 5 minute) ⭐ Recommended

Project me `jenkins/docker-compose.yml` already hai.

```bash
cd studentdesk/jenkins
docker compose up -d
```

Ab **initial admin password** nikalo:
```bash
docker logs jenkins 2>&1 | grep -A 2 "initialAdminPassword"
# Ya directly file se:
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Ek 32-character ka password print hoga, jaise:
```
8f3a9c2e1b7d4a6f0e5c8b2a9d4f1e7c
```
**Isko copy karke rakho.**

**Browser me kholo → http://localhost:8080**

#### 🔵 TARIKA B: Direct install (Ubuntu VM pe — production jaisa)

```bash
# Java install (Jenkins ko Java chahiye)
sudo apt update
sudo apt install -y openjdk-17-jdk curl
java -version

# Jenkins repository add karo
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
  sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install
sudo apt update
sudo apt install -y jenkins

# Start + enable
sudo systemctl enable --now jenkins
sudo systemctl status jenkins      # "active (running)" aana chahiye

# Firewall
sudo ufw allow 8080/tcp
sudo ufw allow OpenSSH

# Initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

**Browser → http://VM_IP:8080**

### 6.2 Jenkins Setup Wizard (pehli baar)

1. **Unlock Jenkins** screen → jo password copy kiya tha wo paste karo → **Continue**
2. **Customize Jenkins** → **"Install suggested plugins"** dabao
   - Ye install karega: Git, Pipeline, Credentials, Blue Ocean, etc.
   - Wait karo 3-5 minute (coffee piyo ☕)
3. **Koi plugin fail ho jaye to** → "Retry" dabao. Ya skip karke baad me manually install karo.
4. **Create First Admin User:**
   - Username: `admin` (ya apna naam)
   - Password: strong password (likh ke rakho!)
   - Name / Email: bharo
   - **Save and Continue**
5. **Instance Configuration** → URL wahi rehne do (`http://localhost:8080/`) → **Save and Finish**
6. **Start using Jenkins** → Dashboard aa jayega 🎉

### 6.3 Plugins install karo (Jenkinsfile ke liye zaroori)

**Manage Jenkins → Plugins → Available plugins** — ye search karke install karo:

| Plugin | Kyun zaroori hai |
|---|---|
| **Docker** | Jenkins ko Docker commands chalane ke liye |
| **Docker Pipeline** | Pipeline me `docker.build()`, `docker.image()` |
| **Pipeline** | Jenkinsfile support (suggested me aa jata hai) |
| **Git** | GitHub se code lane ke liye (suggested me aa jata hai) |
| **JUnit** | Test reports dikhane ke liye |
| **Credentials Binding** | Secrets (Docker Hub password) handle karne ke liye |
| **Workspace Cleanup** | `cleanWs()` ke liye |
| **Timestamper** | Console output me time dikhega |
| **SSH Agent** | Remote VM pe deploy karne ke liye |
| **Blue Ocean** *(optional)* | Sundar pipeline visualization |
| **GitHub Integration** | Webhook se auto-trigger |

Install ke baad → **"Restart Jenkins when installation is complete and no jobs are running"** tick karo.

### 6.4 Global Tools Configuration

**Manage Jenkins → Tools:**

- **Git:** Path = `git` (auto-detect ho jayega)
- **JDK:** Agar Java auto-detect na ho to add karo — Name `jdk17`, `JAVA_HOME` ka path
- **Docker:** Path = `docker`

**Save** dabao.

### 6.5 Docker access Jenkins ko do

Agar Jenkins Docker me chal raha hai (Tarika A), to `jenkins/docker-compose.yml` me already ye line hai:
```yaml
- /var/run/docker.sock:/var/run/docker.sock
- /usr/bin/docker:/usr/bin/docker
```
Isse Jenkins container **host ka Docker** use kar sakta hai. Verify:
```bash
docker exec jenkins docker --version
# Docker version 27.x.x  ← aa gaya to perfect
```

Agar `docker: not found` aaye to:
```bash
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y docker.io"
docker restart jenkins
```

Agar Jenkins directly VM pe installed hai (Tarika B):
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
sudo -u jenkins docker ps     # test karo
```

### 6.6 Credentials add karo (secrets)

**Manage Jenkins → Credentials → System → Global credentials → Add Credentials**

**Credential 1 — Docker Hub:**
| Field | Value |
|---|---|
| Kind | **Username with password** |
| Scope | Global |
| Username | tumhara Docker Hub username |
| Password | tumhara Docker Hub password **ya Access Token** |
| ID | `dockerhub-creds` ⚠️ **exact yahi likho — Jenkinsfile isi ko dhundhta hai** |
| Description | Docker Hub login for pushing images |

> 💡 **Access Token better hai:** Docker Hub → Account Settings → Personal Access Tokens → Generate → `Read & Write` permission.

**Credential 2 — VM SSH key (remote deploy ke liye, optional):**
| Field | Value |
|---|---|
| Kind | **SSH Username with private key** |
| Username | `ubuntu` (ya tumhara VM user) |
| Private Key | Enter directly → apni `.pem` file ka content paste karo |
| ID | `vm-ssh-key` |

### 6.7 Pipeline Job banao

1. **Dashboard → New Item**
2. **Item name:** `studentdesk-pipeline`
3. Neeche **Pipeline** select karo → **OK**
4. Configuration page pe:
   - **Description:** `StudentDesk CI/CD — Build, Test, Docker, Deploy`
   - **GitHub project:** `https://github.com/YOUR_USERNAME/studentdesk/` *(GitHub plugin install ho to)*
   - **Pipeline** section:
     - **Definition:** `Pipeline script from SCM` ← **ye choose karna zaroori hai**
     - **SCM:** `Git`
     - **Repository URL:** `https://github.com/YOUR_USERNAME/studentdesk.git`
     - **Credentials:** public repo hai to none theek hai; private hai to GitHub token add karo
     - **Branch Specifier:** `*/main`
     - **Script Path:** `Jenkinsfile`
   - **Save** dabao

> 🎓 **"Pipeline script from SCM" kyun, "Pipeline script" kyun nahi?**
> Kyunki pipeline ka code **repo ke andar** (`Jenkinsfile`) hona chahiye. Isse:
> - Pipeline bhi version control me hai — history dekh sakte ho
> - Code aur pipeline ek saath change hote hain
> - Ye best practice hai, viva me ye point bolo

### 6.8 Pehla build chalao! 🚀

**Job kholo → left me "Build Now" dabao**

Neeche **"Build History"** me ek entry aayegi: `#1` with a spinner 🔄

**Click karo → "Console Output"** — live logs dekho:

```
Started by user admin
Running as SYSTEM
Building in workspace /var/jenkins_home/workspace/studentdesk-pipeline
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/jenkins_home/workspace/studentdesk-pipeline
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
=== Stage 1: Code checkout ===
Cloning repository https://github.com/YOUR_USERNAME/studentdesk.git
 > git fetch --tags --force ...
Commit: a1b2c3d | Author: Tumhara Naam | Msg: feat: initial StudentDesk app
[Pipeline] }
[Pipeline] stage
[Pipeline] { (Setup Python Env)
=== Stage 2: Virtual environment + dependencies ===
+ python3 -m venv venv
+ pip install -r requirements.txt -r requirements-dev.txt
...
[Pipeline] { (Unit Tests)
=== Stage 4: pytest (unit + integration + API) ===
tests/test_unit.py::TestGradeCalculation::test_grade_a_plus PASSED
...
============================= 12 passed in 1.23s ==============================
Recording test results
...
[Pipeline] { (Docker Build)
=== Stage 6: Docker image build ===
+ docker build -t studentdesk:1-abc1234 .
Successfully built 9f8e7d6c5b4a
...
[Pipeline] { (Deploy)
=== Stage 9: Deployment ===
{"app":"StudentDesk","status":"ok","version":"1.0.0"} <- DEPLOYED OK
[Pipeline] End of Pipeline
Finished: SUCCESS
```

**Green ✅ SUCCESS** → Mubarak ho, tumhara CI/CD pipeline chal gaya!

### 6.9 Pipeline visualization dekho

**Job page → "Pipeline Steps"** ya **"Stage View"** — ek table dikhega:

```
┌──────────┬─────────────┬───────┬───────────┬──────────────┬───────────┬────────────┬────────────┬────────┐
│ Checkout │ Setup Env   │ Build │ Unit Test │ App/API Test │ Docker    │ Smoke Test │ Push       │ Deploy │
│  2.1s    │  45.3s      │ 1.2s  │  8.4s     │  12.7s       │ 38.9s     │  11.2s     │  25.6s     │ 6.3s   │
└──────────┴─────────────┴───────┴───────────┴──────────────┴───────────┴────────────┴────────────┴────────┘
```

Har box pe click karke us stage ka log dekh sakte ho. **Iska screenshot lo** — report me best dikhta hai.

### 6.10 Test results dekho

Job page pe **"Test Result"** ya **"Latest Test Result"** link dikhega (JUnit plugin ki wajah se).

Andar jaake:
- Total tests, passed, failed
- Har test ka naam aur duration
- Fail hone par stack trace

### 6.11 Auto-trigger setup karo (GitHub Webhook)

Abhi tumhe manually "Build Now" dabana padta hai. **Automatic** karte hain:

**Jenkins side:**
1. Job → **Configure**
2. **Build Triggers** section
3. ✅ **"GitHub hook trigger for GITScm polling"** tick karo
4. Save

**GitHub side:**
1. Repo → **Settings** → **Webhooks** → **Add webhook**
2. Fill karo:
   - **Payload URL:**
     - Jenkins Docker me local pe hai: `http://<TUMHARA-LAN-IP>:8080/github-webhook/`
     - Jenkins VM pe hai: `http://<VM_PUBLIC_IP>:8080/github-webhook/`
   - **Content type:** `application/json`
   - **Secret:** khali chhod do (ya Jenkins me configure karo)
   - **Which events:** ✅ **Just the push event**
3. **Add webhook**
4. Webhook list me **"Recent Deliveries"** → green tick ✅ aana chahiye

> ⚠️ **`localhost` payload URL me kaam NAHI karega** — GitHub ka server tumhare laptop ke `localhost` tak nahi pahunch sakta. Options:
> - Jenkins ko VM pe install karo (public IP milega) ← **best**
> - **ngrok** use karo: `ngrok http 8080` → jo URL mile (`https://abc123.ngrok-free.app`) wo + `/github-webhook/` use karo
> - Ya fallback: **"Poll SCM"** → Schedule `H/2 * * * *` (har 2 minute me check karega)

**Test:**
```bash
echo "# webhook test" >> README.md
git add README.md && git commit -m "ci: test webhook trigger" && git push
```
Jenkins dashboard dekho → build apne aap start ho jayegi 🎉

### 6.12 Jaan-boojh kar build FAIL karo (demo ke liye)

Ye dikhana zaroori hai ki pipeline sirf decoration nahi hai:

```bash
# app/models.py kholo, grade() me 90 ko 95 kar do
git add app/models.py
git commit -m "test: intentionally break a test to demo pipeline failure"
git push
```

Jenkins me build **RED ❌** ho jayega. Console Output me:
```
tests/test_unit.py::TestGradeCalculation::test_grade_a_plus FAILED
    def test_grade_a_plus(self):
>       assert make_student(95).grade() == "A+"
E       AssertionError: assert 'A' == 'A+'
```

Aur **Docker Build / Deploy stages SKIP ho jayenge** — kyunki test fail hua. Screenshot lo!

Phir theek karo:
```bash
git revert HEAD          # ya manually 95 wapas 90 karo
git push
```
Ab build green ✅.

### 6.13 Jenkinsfile ke stages — viva me ye poochenge

| Stage | Kya karta hai | Fail hone par |
|---|---|---|
| **Checkout** | GitHub se code clone karta hai | Code hi nahi milega |
| **Setup Python Env** | venv + pip install | Build ruk jayega |
| **Build** | `compileall` — syntax check | Syntax error pakda jayega |
| **Unit Tests** | Business logic tests (grade calculation) | Deploy nahi hoga |
| **App & API Tests** | Routes + REST API tests | Deploy nahi hoga |
| **Docker Build** | Image banata hai | Image nahi banegi |
| **Smoke Test** | Container chalake `/health` hit karta hai | Broken image deploy nahi hogi |
| **Docker Push** | Registry pe image bhejta hai | Deploy purani image se hoga |
| **Deploy** | Container restart + health verify | Rollback karna padega |

**`post` block:**
```groovy
post {
    success { echo "✅ PIPELINE SUCCESS" }
    failure { echo "❌ PIPELINE FAILED" }
    always  { archiveArtifacts artifacts: 'reports/*.xml'; cleanWs() }
}
```
- `always` = chahe pass ho ya fail, ye chalega (test reports archive + workspace clean)

**`when { branch 'main' }`** = Docker Push aur Deploy sirf `main` branch pe honge. Feature branch pe sirf tests chalenge. Ye **branch protection** ka idea hai.

### 6.14 Email notification (optional, achha lagta hai)

**Manage Jenkins → System → Extended E-mail Notification:**
- SMTP server: `smtp.gmail.com`, Port `587`, Use SSL ✅
- Credentials: Gmail **App Password** (Google Account → Security → 2-Step Verification → App passwords)
- Job → Configure → **Post-build Actions → Editable Email Notification**
  - Project Recipient List: `tumhari-email@example.com`
  - Advanced → Triggers → **Failure** aur **Success** add karo

Ab build fail hote hi email aa jayega 📧

---

## 7. GitHub Actions (Free wala CI/CD)

> **Kyun dono?** Jenkins college syllabus me hai (isliye zaroori), lekin GitHub Actions:
> - **Bilkul free** hai (koi server nahi chahiye)
> - **GitHub ke andar hi** chalta hai — koi setup nahi
> - Public repos pe **unlimited minutes**
>
> Report me dono dikhao — "humne Jenkins use kiya, aur GitHub Actions ko modern alternative ke roop me bhi configure kiya" — ye extra marks dilayega.

### 7.1 Kaise kaam karta hai

Repo me `.github/workflows/ci-cd.yml` file hoti hai (already bana diya hai). GitHub use padhta hai aur **apne servers pe** (runners) job chalata hai.

### 7.2 Already configured hai — bas enable karo

Tumhari repo me ye files hain:
```
.github/workflows/ci-cd.yml       ← main CI/CD (test + docker + deploy)
.github/workflows/codeql.yml      ← security scan
.github/dependabot.yml            ← dependency updates
```

**Kuch nahi karna!** Bas push karo aur dekho.

### 7.3 Actions tab check karo

1. GitHub repo kholo
2. Upar **"Actions"** tab dabao
3. Left me workflows dikhenge: `CI/CD Pipeline`, `CodeQL Security Scan`
4. Kisi run pe click karo → jobs dikhege → step-by-step logs

```
CI/CD Pipeline
  ✅ Build & Test (3.11)          2m 14s
  ✅ Build & Test (3.12)          2m 08s
  ✅ Docker Build & Push          1m 45s
  ⏭️ Deploy to VM                 skipped (secrets nahi hain)
```

### 7.4 Deploy job ke secrets add karo (agar VM hai)

Repo → **Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|---|---|
| `DEPLOY_HOST` | VM ka public IP |
| `DEPLOY_USER` | `ubuntu` (ya `opc` for Oracle, `ec2-user` for AWS) |
| `DEPLOY_SSH_KEY` | `.pem` file ka **poora content** (-----BEGIN... se -----END... tak) |
| `APP_SECRET_KEY` | koi bhi random string |

Secrets add hone ke baad next push pe deploy job bhi chalega.

> 💡 **Secrets kabhi logs me print nahi hote** — GitHub unhe `***` se mask kar deta hai. Ye security feature viva me batao.

### 7.5 Deploy job hata do agar VM nahi hai

Agar tumne cloud VM nahi liya to deploy job hamesha fail hogi (secrets missing). 2 options:

**Option A — workflow me condition add karo** (`.github/workflows/ci-cd.yml` me `deploy:` job ke andar):
```yaml
  deploy:
    name: Deploy to VM
    runs-on: ubuntu-latest
    needs: docker
    if: github.event_name == 'push' && github.ref == 'refs/heads/main' && vars.DEPLOY_ENABLED == 'true'
```
Phir **Settings → Secrets and variables → Actions → Variables → New repository variable** → Name `DEPLOY_ENABLED`, Value `true` (jab VM ready ho).

**Option B — deploy job ko comment out kar do** (poora `deploy:` block `#` se).

### 7.6 Branch protection rules (professional touch)

Repo → **Settings → Branches → Add branch protection rule**

- **Branch name pattern:** `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging → `Build & Test (3.11)`, `Build & Test (3.12)` search karke add karo
- ✅ Require branches to be up to date
- ✅ Do not allow force pushes
- **Create**

Ab koi bhi `main` pe directly push nahi kar sakta jab tak tests pass na ho. **Ye DevOps ka "quality gate" hai.**

### 7.7 Jenkins vs GitHub Actions (viva question!)

| | **Jenkins** | **GitHub Actions** |
|---|---|---|
| Hosting | Apna server chahiye (self-hosted) | GitHub ke servers (managed) |
| Cost | Software free, par server/maintenance ka kharcha | Public repo = free unlimited; private = 2000 min/month |
| Config file | `Jenkinsfile` (Groovy) | `.github/workflows/*.yml` (YAML) |
| Setup time | Zyada (plugins, Java, Docker access) | Bilkul zero |
| Flexibility | Bahut zyada — 1800+ plugins, kuch bhi kar sakte ho | Marketplace actions, par self-hosted runners bhi milte hain |
| Learning curve | Steeper | Easy |
| Kab use karo | On-premise, air-gapped, complex legacy pipelines, **college syllabus** 😄 | Modern cloud-native projects, open source |
| Security | Apni zimmedari | GitHub manage karta hai, secrets masking built-in |

**Best answer:** "Dono ka use case alag hai. Jenkins tab jab control aur customization chahiye ya on-premise infrastructure ho. GitHub Actions jab speed aur zero-maintenance chahiye. Hamne project me dono implement kiye taaki comparison samajh aaye."

---

## 8. Cloud Deployment

> Ab tak sab kuch laptop pe tha. Ab app ko **internet pe live** karenge taaki professor link khol ke dekh sakein.

### 8.1 Kaunsa option chunna hai?

| Scenario | Recommendation |
|---|---|
| Credit card hai, full DevOps (Ansible + monitoring) dikhana hai | **Oracle Cloud / AWS EC2 VM** ⭐ |
| Credit card nahi hai, par VM jaisa experience chahiye | **VirtualBox pe Ubuntu VM** |
| Sirf app live karni hai, jaldi | **Render / Railway** (Docker deploy) |
| GitHub Actions ko hi deploy karne dena hai | **GitHub Codespaces** ya VM + Actions |

---

### 8.2 OPTION 1 — Oracle Cloud Free Tier (best, permanently free)

#### Step 1: Account banao
1. Jao → https://www.oracle.com/cloud/free/
2. **"Start for free"** → Sign up
3. Details bharo:
   - **Country:** India
   - **Home Region:** `India West (Mumbai)` ← **Mumbai choose karo, latency kam hogi**
   - Email verify karo
4. **Payment verification:** Credit/Debit card lagana padega — **₹100 hold hoga, phir refund**. Free tier me charge nahi hota.
   - 💡 Debit card sometimes fail hota hai → **credit card best hai**. Agar bilkul nahi hai to Option 3 (VirtualBox) pe jao.

#### Step 2: VM Instance banao
1. Login ke baad → **Compute → Instances → Create instance**
2. Fill karo:

| Field | Value |
|---|---|
| **Name** | `studentdesk-vm` |
| **Placement** | Default rehne do |
| **Image** | **Change** → Ubuntu → **Canonical Ubuntu 24.04** → Select |
| **Shape** | **Change** → **Specialty and previous generation** → **VM.Standard.E2.1.Micro** (1 OCPU, 1GB RAM) — **ye "Always Free" eligible hai** ✅ |
| | *Ya* **Ampere A1** (ARM, 4 OCPU + 24GB RAM free) — powerful par ARM architecture hai |
| **Networking** | **Create new VCN** — sab defaults |
| ✅ **Assign a public IPv4 address** | Tick karna **zaroori** hai! |
| **SSH keys** | **"Save private key"** aur **"Save public key"** — **dono download karo** aur safe jagah rakho! |

3. **Create** dabao.
4. ~1 minute me state **"PROVISIONING" → "RUNNING"** ho jayega (green).
5. **Public IP address** copy karo, jaise `140.245.12.34`

#### Step 3: SSH se connect karo

```bash
# Jahan .pem download hui thi wahan jao (Downloads folder)
cd ~/Downloads
chmod 600 ssh-key-2026-*.key        # permission fix — warna SSH error dega

# Ubuntu image ka default user = "ubuntu"
ssh -i ssh-key-2026-*.key ubuntu@140.245.12.34

# Agar Oracle Linux image liya hota to user "opc" hota
```

Pehli baar poochega:
```
The authenticity of host '140.245.12.34' can't be established.
Are you sure you want to continue connecting (yes/no)?
```
→ `yes` likho.

Agar ye dikhe to **VM ke andar ho**:
```
ubuntu@studentdesk-vm:~$
```

> ⚠️ **SSH connection timeout ho raha hai?** Oracle ke security list me port open karna padta hai:
> **Networking → Virtual cloud networks → tumhara VCN → Subnet → Security List → Add Ingress Rules**
> - Source CIDR: `0.0.0.0/0`, Protocol: TCP, Port: `22`
> - Same karo `5000`, `8080`, `9090`, `3000` ke liye
>
> Aur VM ke **andar** bhi firewall: `sudo iptables -I INPUT -p tcp --dport 5000 -j ACCEPT`
> (Ubuntu image me Oracle ne default iptables rules rakhe hote hain jo sirf 22 allow karte hain — ye common trap hai!)
> Permanent karne ke liye:
> ```bash
> sudo netfilter-persistent save
> ```

#### Step 4: Key ko `~/.ssh` me daalo (baar-baar path likhne se bachne ke liye)

```bash
mkdir -p ~/.ssh
mv ~/Downloads/ssh-key-2026-*.key ~/.ssh/oracle-studentdesk.pem
chmod 600 ~/.ssh/oracle-studentdesk.pem

# Ab sirf:
ssh -i ~/.ssh/oracle-studentdesk.pem ubuntu@140.245.12.34
```

**Aur bhi aasan — `~/.ssh/config` file banao:**
```
Host studentdesk
    HostName 140.245.12.34
    User ubuntu
    IdentityFile ~/.ssh/oracle-studentdesk.pem
    ServerAliveInterval 60
```
Ab sirf: `ssh studentdesk` 🎉

---

### 8.3 OPTION 2 — AWS EC2 (12 mahine free)

1. Jao → https://aws.amazon.com/console/ → **Create an AWS account**
2. Credit card + phone verification hoga. **Free Tier** select karo.
3. Console → **EC2 → Launch Instance**

| Field | Value |
|---|---|
| **Name** | `studentdesk-vm` |
| **AMI** | **Ubuntu Server 24.04 LTS (HVM), SSD Volume Type** — "Free tier eligible" label dekho |
| **Instance type** | **t2.micro** (1 vCPU, 1GB) — Free tier eligible ✅ |
| **Key pair** | **Create new key pair** → Name `studentdesk-key` → Type `.pem` → **Download** |
| **Network settings** | **Edit** → ✅ **Allow SSH traffic from: My IP** → ✅ **Allow HTTP traffic from the internet** |
| | Custom security group → Add rule: Type **Custom TCP**, Port `5000`, Source `0.0.0.0/0` |
| **Configure storage** | 8GB default theek hai (ya 15GB kar lo) |

4. **Launch instance** → **View all instances**
5. State `running` hone par **Public IPv4 address** copy karo

```bash
chmod 600 ~/Downloads/studentdesk-key.pem
ssh -i ~/Downloads/studentdesk-key.pem ubuntu@<PUBLIC_IP>
```

> 💡 **AWS me free tier 12 mahine ka hai** — 750 hours/month = ek VM poori mahine chala sakte ho.
> ⚠️ **Submission ke baad instance TERMINATE karna mat bhoolna**, warna 13ve mahine bill aayega!
> **Billing → Budgets** me ek $0 budget + alert laga lo (safety ke liye).

---

### 8.4 OPTION 3 — VirtualBox (apne laptop pe VM, bilkul free, koi card nahi)

1. Download → https://www.virtualbox.org/wiki/Downloads (platform: Windows hosts)
2. Ubuntu ISO → https://ubuntu.com/download/server (**Ubuntu Server 24.04 LTS**)
3. VirtualBox → **New**:
   - Name: `ubuntu-devops`, Type: Linux, Version: Ubuntu (64-bit)
   - RAM: **4096 MB** (kam se kam 2GB)
   - Hard disk: **25 GB**
4. Settings → **Network** → Adapter 1: **Bridged Adapter** ← isse VM ko tumhare WiFi ka real IP milega
5. Settings → **System → Processor**: 2 CPU
6. **Start** → ISO select karo → Ubuntu installer chalega
   - Language: English → Keyboard: English → Install Ubuntu Server
   - Network: DHCP accept karo
   - Profile: naam, server name `studentdesk-vm`
   - ✅ **Install OpenSSH server** ← **ye tick karna MUST hai**
   - Install complete → Reboot

7. VM ke andar IP pata karo:
```bash
ip addr show | grep inet
# inet 192.168.1.42/24   ← ye tumhara VM IP hai
```

8. Laptop se connect:
```bash
ssh tumhara-username@192.168.1.42
```

> 💡 **Snapshots lo** (Machine → Take Snapshot) — "clean-base" naam se. Kuch gadbad ho jaye to wapas aa sakte ho.

---

### 8.5 VM pe manual deployment (pehle manually, phir Ansible se)

> **Pehle manually karke dekho — tabhi samajh aayega ki Ansible kya automate kar raha hai.**

#### Step 1: System update + Docker install

VM pe SSH karke:

```bash
sudo apt update && sudo apt upgrade -y

# Docker install (official script — sabse easy)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Apne user ko docker group me daalo
sudo usermod -aG docker $USER
newgrp docker        # ya logout karke wapas login karo

# Verify
docker --version
docker compose version
docker run hello-world
```

#### Step 2: Code lao

```bash
sudo apt install -y git

cd ~
git clone https://github.com/YOUR_USERNAME/studentdesk.git
cd studentdesk
```

#### Step 3: Image build + container run

```bash
docker build -t studentdesk:1.0.0 .

docker run -d \
  --name studentdesk \
  --restart unless-stopped \
  -p 5000:5000 \
  -v studentdesk_data:/app/instance \
  -e SECRET_KEY="$(openssl rand -hex 32)" \
  studentdesk:1.0.0

# Verify (VM ke andar se)
curl http://localhost:5000/health
docker ps
docker logs studentdesk
```

#### Step 4: Firewall kholo

```bash
sudo ufw allow OpenSSH
sudo ufw allow 5000/tcp
sudo ufw --force enable
sudo ufw status
```

#### Step 5: Bahar se access karo

Apne **laptop** ke browser me:
```
http://VM_PUBLIC_IP:5000
```

🎉 **App internet pe LIVE hai!** Ye link report me daalo.

Terminal se bhi test:
```bash
curl http://VM_PUBLIC_IP:5000/health
curl http://VM_PUBLIC_IP:5000/api/stats
```

> ⚠️ **Access nahi ho raha?** Checklist:
> 1. Cloud console ke **Security Group / Ingress Rules** me port 5000 open hai? (sabse common galti)
> 2. Oracle hai to VM ke andar `sudo iptables -L INPUT -n` dekho — Oracle ke apne rules hote hain
> 3. `sudo ufw status` → `5000/tcp ALLOW` dikh raha hai?
> 4. `docker ps` → container `Up` hai? `-p 5000:5000` mapping dikh rahi hai?
> 5. VM ke andar `curl localhost:5000/health` chal raha hai?
> 6. `-p 5000:5000` hi hai na, `-p 127.0.0.1:5000:5000` to nahi? (wo sirf localhost pe bind karta hai)

---

### 8.6 OPTION 4 — Render.com (VM nahi chahiye, 5 minute me live)

Agar VM nahi mil paya to ye best fallback hai:

1. Jao → https://render.com → GitHub se **Sign up**
2. **New + → Web Service**
3. Repo connect karo → `studentdesk` select karo
4. Fill karo:

| Field | Value |
|---|---|
| **Name** | `studentdesk` |
| **Region** | Singapore (India ke closest) |
| **Runtime** | **Docker** ← ye choose karo |
| **Dockerfile Path** | `./Dockerfile` |
| **Instance Type** | **Free** |
| **Health Check Path** | `/health` |
| **Environment Variables** | `SECRET_KEY` = koi random string |

5. **Create Web Service**
6. 3-5 minute me build hoga → **URL milega**: `https://studentdesk.onrender.com`

> ⚠️ **Render free tier:** app 15 minute idle rehne par **sleep** ho jati hai. Pehli request pe 30-50 second lagenge (cold start). Ye normal hai — professor ko bata dena.
> ⚠️ Render free me **persistent disk nahi** milta → SQLite data restart pe reset ho jayega. Demo ke liye theek hai.

**Render pe auto-deploy:** GitHub pe push karte hi Render khud rebuild kar dega. **Settings → Auto-Deploy = Yes**.

---

### 8.7 Nginx reverse proxy + HTTPS (bonus, extra marks)

VM pe production-jaisa setup:

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

`/etc/nginx/sites-available/studentdesk` banao:
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN.com;      # ya VM ka public IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/studentdesk /etc/nginx/sites-enabled/
sudo nginx -t                      # config test
sudo systemctl reload nginx

# Free HTTPS certificate (domain chahiye - duckdns.org free hai)
sudo certbot --nginx -d YOUR_DOMAIN.com
```

Ab `https://YOUR_DOMAIN.com` pe app chalegi with SSL 🔒

---

## 9. Ansible

### 9.1 Ansible kya hai — simple bhasha me

Ansible = **"ek saath bahut saare servers pe commands chalane ka tarika, YAML me likh ke."**

Bina Ansible:
```bash
ssh ubuntu@server1
sudo apt update && sudo apt install docker.io
sudo usermod -aG docker ubuntu
exit
ssh ubuntu@server2
# ... wahi sab dobara 😫
```

Ansible ke saath:
```bash
ansible-playbook provision.yml     # 100 servers pe ek saath, 2 minute me ✅
```

**3 key concepts:**

| Term | Matlab | Hamare project me |
|---|---|---|
| **Inventory** | Servers ki list (kaun-kaun se machines pe kaam karna hai) | `ansible/inventory/hosts.ini` |
| **Playbook** | YAML file — kya karna hai, kis order me | `ansible/playbooks/*.yml` |
| **Module** | Actual kaam karne wala tool (`apt`, `copy`, `docker_container`) | `ansible.builtin.apt` etc. |
| **Task** | Ek module ka ek call | `- name: Docker install karo` |
| **Handler** | Task jo sirf change hone par chalta hai | `notify: restart prometheus` |
| **Idempotency** | 100 baar chalao, result same — kuch nahi toota | ⭐ Sabse important concept |

> 🎓 **Idempotency — viva ka favourite question!**
> Ansible pehle **check** karta hai ki state already sahi hai ya nahi. Agar Docker installed hai to dobara install nahi karega, output me `ok` (green) dikhega, `changed` (yellow) nahi. Isse playbook ko bar-bar safely chala sakte ho — "script chalane se kuch toot jayega" ka darr nahi.
> Output me: **green = ok** (kuch nahi badla), **yellow = changed** (Ansible ne kuch kiya).

### 9.2 Ansible install karo

```bash
# Laptop pe (Windows wale WSL me)
pip3 install ansible

# Collections install karo (docker aur ufw modules ke liye)
cd studentdesk/ansible
ansible-galaxy collection install -r requirements.yml

# Verify
ansible --version
ansible-galaxy collection list | grep -E "docker|general"
```

### 9.3 Inventory setup karo

`ansible/inventory/hosts.ini` kholo aur **apna VM IP** daalo:

```ini
[webservers]
studentdesk-vm ansible_host=140.245.12.34 ansible_user=ubuntu

[monitoring]
studentdesk-vm

[all:vars]
ansible_ssh_private_key_file=~/.ssh/oracle-studentdesk.pem
ansible_python_interpreter=/usr/bin/python3
```

> 📝 **User naam kya hoga?**
> - Ubuntu image → `ubuntu`
> - Oracle Linux → `opc`
> - AWS Amazon Linux → `ec2-user`
> - Debian → `admin` ya root

### 9.4 Connection test karo (pehla Ansible command!)

```bash
cd studentdesk/ansible

# Sabse simple test — "ping" (SSH ping nahi, Ansible ka module)
ansible all -i inventory/hosts.ini -m ping
```

**Success output:**
```json
studentdesk-vm | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

🎉 `"ping": "pong"` aa gaya to Ansible VM se baat kar sakta hai!

**Agar UNREACHABLE aaye:**
```
studentdesk-vm | UNREACHABLE! => {
    "msg": "Failed to connect to the host via ssh:
            ssh: connect to host 140.245.12.34 port 22: Connection timed out"
}
```
→ IP galat hai, ya SSH key ka path galat, ya firewall port 22 block kar raha hai.

**Aur facts nikalo (system info):**
```bash
ansible all -i inventory/hosts.ini -m setup -a "filter=ansible_distribution*"
ansible all -i inventory/hosts.ini -m shell -a "df -h && free -h"
ansible all -i inventory/hosts.ini -m command -a "docker --version" --become
```

### 9.5 Playbook 1 — Provision (server ready karo)

```bash
ansible-playbook playbooks/provision.yml -i inventory/hosts.ini
```

**Kya-kya hoga:**
1. APT cache update
2. Python, Git, curl install
3. Docker GPG key + repository add
4. Docker Engine + Compose plugin install
5. Docker service enable + start
6. `ubuntu` user ko docker group me add
7. `/opt/studentdesk` folder banao
8. Firewall (UFW) — 22, 5000, 9090, 3000 allow
9. Verification message

**Output kaisa dikhega:**
```
PLAY [Provision StudentDesk server] *********************

TASK [Gathering Facts] **********************************
ok: [studentdesk-vm]

TASK [APT cache update karo] ****************************
changed: [studentdesk-vm]

TASK [Basic packages install karo] **********************
changed: [studentdesk-vm]

TASK [Docker Engine install karo] ***********************
changed: [studentdesk-vm]

TASK [Docker service enable + start] ********************
ok: [studentdesk-vm]

TASK [ubuntu ko docker group me add karo] ***************
changed: [studentdesk-vm]

TASK [Result dikhao] ************************************
ok: [studentdesk-vm] => {
    "msg": "Docker version 27.3.1, build ce12230 — server provision ho gaya ✅"
}

PLAY RECAP **********************************************
studentdesk-vm : ok=14  changed=8  unreachable=0  failed=0  skipped=0
```

> ⚠️ **SSH password maang raha hai?** Add karo: `ansible-playbook playbooks/provision.yml -i inventory/hosts.ini --ask-become-pass` (sudo password)
> Ya better: SSH key setup karo (already inventory me diya hai).

> ⚠️ **`community.general.ufw` module not found?** → `ansible-galaxy collection install community.general` chalao.

**Dobara chalao — idempotency dekho:**
```bash
ansible-playbook playbooks/provision.yml -i inventory/hosts.ini
```
Ab output:
```
TASK [Docker Engine install karo] ***********************
ok: [studentdesk-vm]          ← green, "changed" nahi!

PLAY RECAP
studentdesk-vm : ok=14  changed=0  unreachable=0  failed=0
```
**`changed=0`** ← yahi idempotency hai. Screenshot lo!

### 9.6 Playbook 2 — Deploy

```bash
# Default values ke saath
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini

# Apni repo aur tag ke saath
GIT_REPO=https://github.com/YOUR_USERNAME/studentdesk.git \
IMAGE_TAG=1.0.0 \
APP_SECRET_KEY="$(openssl rand -hex 32)" \
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini

# Sirf deploy task chalao (provision skip)
ansible-playbook site.yml -i inventory/hosts.ini --tags deploy
```

**Output:**
```
TASK [Git se latest code pull karo] *********************
changed: [studentdesk-vm]

TASK [Code change hua ya nahi batayo] *******************
ok: [studentdesk-vm] => { "msg": "Naya commit mila - redeploy hoga" }

TASK [Docker image build karo] **************************
changed: [studentdesk-vm]

TASK [Naya container start karo] ************************
changed: [studentdesk-vm]

TASK [Health check karo] ********************************
ok: [studentdesk-vm]

TASK [Deployment summary] *******************************
ok: [studentdesk-vm] => {
    "msg": [
        "✅ DEPLOYMENT SUCCESSFUL",
        "App URL      : http://140.245.12.34:5000",
        "Health check : ok",
        "Image        : studentdesk:1.0.0"
    ]
}
```

Browser me kholo → **http://VM_IP:5000** ✅

### 9.7 Playbook 3 — Monitoring stack

```bash
ansible-playbook playbooks/monitoring.yml -i inventory/hosts.ini
```

Ye VM pe install karega:
- **Node Exporter** (port 9100) — CPU, RAM, disk, network metrics
- **Prometheus** (port 9090) — metrics collect + store + alert rules
- **Grafana** (port 3000) — dashboards

### 9.8 Ek command me sab — Master playbook

```bash
ansible-playbook site.yml -i inventory/hosts.ini
```

`site.yml` teeno playbooks ko order me chalata hai: **provision → deploy → monitoring**.

**Ye tumhara final demo command hai** — professor ke saamne ye ek command chalao aur poora infrastructure khada ho jayega. 🔥

### 9.9 Dry run aur extra flags (professional touch)

```bash
# Dry run — kya badlega, bina actually kiye
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini --check

# Check + diff (file changes line-by-line dikhayega)
ansible-playbook playbooks/provision.yml -i inventory/hosts.ini --check --diff

# Verbose output (debugging ke liye)
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini -vvv

# Sirf ek task / tag
ansible-playbook site.yml --tags deploy
ansible-playbook site.yml --skip-tags slow

# Ek hi server pe
ansible-playbook playbooks/deploy.yml --limit studentdesk-vm

# Syntax check (chalane se pehle)
ansible-playbook playbooks/deploy.yml --syntax-check

# Playbook ko lint karo
ansible-lint playbooks/
```

### 9.10 Rollback playbook

```bash
# Version 1.0.0 pe wapas jao
ansible-playbook playbooks/rollback.yml -i inventory/hosts.ini -e "rollback_tag=1.0.0"
```

> 🎓 **Viva me bolo:** "Real DevOps me rollback plan hona zaroori hai. Agar naya deploy break ho jaye to hum `rollback.yml` se pichhle stable version pe wapas ja sakte hain — bina manual intervention ke."

### 9.11 Ansible ad-hoc commands (quick one-liners)

```bash
cd studentdesk/ansible

# Sab servers pe disk space dekho
ansible all -i inventory/hosts.ini -m shell -a "df -h /"

# Docker container list
ansible webservers -i inventory/hosts.ini -m shell -a "docker ps" --become

# File copy karo
ansible webservers -i inventory/hosts.ini -m copy -a "src=../README.md dest=/tmp/"

# Service restart
ansible webservers -i inventory/hosts.ini -m systemd -a "name=docker state=restarted" --become

# Sab ko reboot karo (10 minute wait ke saath)
ansible all -i inventory/hosts.ini -m reboot -a "reboot_timeout=600" --become
```

### 9.12 Local pe Ansible practice (VM ke bina)

Agar abhi VM nahi hai to apne laptop pe hi try karo:

```bash
cd studentdesk/ansible
ansible all -i inventory/localhost.ini -m ping
# localhost | SUCCESS => { "ping": "pong" }
```

---

## 10. Monitoring & Log Management

### 10.1 Monitoring kyun zaroori hai

App deploy karne ke baad sawal:
- App chal rahi hai ya crash ho gayi?
- Kitne log use kar rahe hain?
- Server ka CPU/RAM/disk kitna bhara hai?
- Requests slow to nahi ho rahe?
- Koi 500 error to nahi aa raha?

**Ansible/Grafana ke bina** → tumhe SSH karke `docker logs` padhna padega.
**Monitoring ke saath** → ek dashboard pe sab live dikhta hai, alert bhi milta hai.

### 10.2 Architecture

```
                    ┌──────────────────────┐
                    │   StudentDesk App    │  /metrics (Prometheus format)
                    │   :5000              │  /health
                    └──────────┬───────────┘
                               │ scrape har 15 sec
                               ↓
┌──────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│ Node Exporter│───→│      PROMETHEUS      │←───│   Alert Rules   │
│ :9100        │    │        :9090         │    │   (alerts.yml)  │
│ CPU/RAM/Disk │    │  Time-series DB      │    └─────────────────┘
└──────────────┘    └──────────┬───────────┘
                               │ query (PromQL)
                               ↓
                    ┌──────────────────────┐
                    │       GRAFANA        │
                    │        :3000         │  Dashboards + alerts
                    └──────────────────────┘
```

| Tool | Kaam |
|---|---|
| **Prometheus** | Metrics collect karta hai (har 15s), time-series DB me store karta hai, PromQL se query |
| **Node Exporter** | Server ke metrics nikalta hai — CPU, RAM, disk, network |
| **Grafana** | Prometheus ka data beautiful graphs me dikhata hai |
| **Alert Rules** | Condition fail hone par alert (app down, CPU > 85%, disk < 15%) |

### 10.3 App me `/metrics` endpoint

Code me `app/metrics.py` already hai. Kya-kya metrics milte hain:

```bash
curl http://localhost:5000/metrics
```

```
# HELP studentdesk_http_requests_total Total HTTP requests
# TYPE studentdesk_http_requests_total counter
studentdesk_http_requests_total{method="GET",path="/",status="200"} 12.0
studentdesk_http_requests_total{method="GET",path="/students",status="200"} 5.0
studentdesk_http_requests_total{method="POST",path="/students/new",status="302"} 2.0

# HELP studentdesk_http_request_duration_seconds HTTP request latency in seconds
# TYPE studentdesk_http_request_duration_seconds histogram
studentdesk_http_request_duration_seconds_bucket{le="0.005",method="GET",path="/"} 3.0
...
studentdesk_http_request_duration_seconds_sum{method="GET",path="/"} 0.4821
studentdesk_http_request_duration_seconds_count{method="GET",path="/"} 12.0

# HELP studentdesk_students_total Number of students in the database
# TYPE studentdesk_students_total gauge
studentdesk_students_total 8.0

# HELP studentdesk_students_passed_total Number of students who passed
studentdesk_students_passed_total 7.0
```

**3 metric types (viva question):**
- **Counter** — sirf badhta hai (total requests). `rate()` se use karo.
- **Gauge** — up-down dono (current student count, RAM usage).
- **Histogram** — values ko buckets me baant-ta hai (latency distribution) → percentile nikal sakte ho.

### 10.4 Monitoring stack chalao

#### 🟢 Local pe (Docker Compose)
```bash
cd studentdesk
docker compose --profile monitoring up -d
docker compose ps
```

#### 🔵 VM pe (Ansible se)
```bash
cd studentdesk/ansible
ansible-playbook playbooks/monitoring.yml -i inventory/hosts.ini
```

### 10.5 Prometheus use karo

Browser → **http://localhost:9090** (ya `http://VM_IP:9090`)

**Status → Targets** — sab `UP` (green) hone chahiye:

| Endpoint | Job | State |
|---|---|---|
| `http://localhost:9090/metrics` | prometheus | 🟢 UP |
| `http://app:5000/metrics` | studentdesk-app | 🟢 UP |
| `http://node-exporter:9100/metrics` | node | 🟢 UP |

> ⚠️ **Target DOWN dikh raha hai?**
> - Prometheus aur app **same Docker network** pe hone chahiye (compose me hain)
> - `monitoring/prometheus.yml` me target sahi hai? Compose me `app:5000`, VM pe `localhost:5000`
> - VM pe Ansible playbook automatically `app:5000` ko `localhost:5000` me rewrite kar deta hai

**PromQL queries try karo** (upar search box me):

| Query | Kya batata hai |
|---|---|
| `up` | Kaun-kaun se targets alive hain |
| `studentdesk_students_total` | Kitne students DB me |
| `rate(studentdesk_http_requests_total[1m])` | Requests per second |
| `sum by(status) (rate(studentdesk_http_requests_total[5m]))` | Status code wise traffic |
| `histogram_quantile(0.95, rate(studentdesk_http_request_duration_seconds_bucket[5m]))` | 95th percentile latency |
| `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` | CPU usage % |
| `node_memory_MemAvailable_bytes / 1024 / 1024` | Free RAM (MB) |
| `(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100` | Disk free % |
| `rate(node_network_receive_bytes_total[5m])` | Network download speed |

**Status → Rules** me tumhare 6 alert rules dikhenge.

### 10.6 Grafana dashboard

Browser → **http://localhost:3000** (ya `http://VM_IP:3000`)
Login: `admin` / `admin123`

**Datasource check:** Settings (⚙️) → Data sources → **Prometheus** already configured hai (provisioning ki wajah se). URL `http://prometheus:9090`. **Save & Test** → green "Data source is working" ✅

**Dashboard import karo:**
1. Left menu → **Dashboards → New → Import**
2. **Upload JSON file** → `monitoring/grafana/dashboards/studentdesk.json` select karo
3. Data source: Prometheus
4. **Import**

**Ya ready-made community dashboards (bahut sundar):**

| Dashboard ID | Naam | Kaisa hai |
|---|---|---|
| **1860** | Node Exporter Full | Sabse popular, 30+ panels — CPU/RAM/disk/network sab |
| **3662** | Node Exporter Server Metrics | Simple, clean |
| **11074** | Node Exporter for Prometheus 1.x | Detailed |

Import: Dashboards → New → Import → **ID daalo** (jaise `1860`) → Load → Prometheus select → Import.

**Ab load generate karo taaki graphs me kuch dikhe:**
```bash
# Apne laptop se — 100 requests bhejo
for i in $(seq 1 100); do curl -s http://VM_IP:5000/health > /dev/null; done

# Ya continuous load
while true; do curl -s http://VM_IP:5000/api/students > /dev/null; sleep 0.5; done
```

Grafana refresh karo → graphs me movement dikhegi 📈 **Screenshot lo!**

### 10.7 Alerts test karo (demo ke liye zabardast)

```bash
# Container band kar do
docker stop studentdesk

# 1-2 minute wait karo, phir Prometheus me dekho:
# http://localhost:9090/alerts  → AppIsDown  FIRING 🔴
# Grafana → App Status panel → "DOWN" (red)

# Wapas chalao
docker start studentdesk
# 1 minute me alert resolve ho jayega → GREEN
```

**Iska screenshot report me daalo** — alerting working hai prove ho jayega.

**Alertmanager** (email/Slack pe alert bhejne ke liye) — optional:
```yaml
# docker-compose me add karo
  alertmanager:
    image: prom/alertmanager:v0.27.0
    ports: ["9093:9093"]
    volumes:
      - ./monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml
```

### 10.8 Log Management

**Level 1 — Docker logs (simplest):**
```bash
docker logs studentdesk                        # sab logs
docker logs -f studentdesk                     # live tail
docker logs --tail 100 studentdesk             # last 100 lines
docker logs --since 10m studentdesk            # last 10 minutes
docker logs --since 2026-09-19T10:00 studentdesk
docker inspect --format='{{.LogPath}}' studentdesk   # log file ka path
```

Hamari app **structured logs** karti hai (`app/__init__.py` me):
```
2026-09-19 14:32:11,847 | INFO     | app | GET / -> 200
2026-09-19 14:32:15,203 | INFO     | app | POST /login -> 302
2026-09-19 14:32:16,001 | INFO     | app | GET /students -> 200
```

Gunicorn ke access logs bhi:
```
172.18.0.1 - - [19/Sep/2026:14:32:11 +0000] "GET /health HTTP/1.1" 200 68 "-" "curl/8.5.0"
```

**Level 2 — Log rotation (disk bharne se bachao):**
```bash
docker run -d --name studentdesk \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  -p 5000:5000 studentdesk:1.0.0
```
Ansible deploy playbook me ye already configured hai ✅

**Level 3 — Loki + Promtail (proper log aggregation, bonus):**
```yaml
# docker-compose me
  loki:
    image: grafana/loki:3.1.0
    ports: ["3100:3100"]
  promtail:
    image: grafana/promtail:3.1.0
    volumes:
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./monitoring/promtail-config.yml:/etc/promtail/config.yml:ro
```
Phir Grafana me Loki datasource add karke log query karo:
```
{container="studentdesk"} |= "ERROR"
```

**Level 4 — ELK Stack (Elasticsearch + Logstash + Kibana)** — mention karo report me:
> "Bade production setups me ELK ya Loki use hota hai. Hamne resource constraints ki wajah se Docker logs + structured logging + Loki-compatible format use kiya."

### 10.9 Uptime monitoring (free, external)

App internet pe live hai to ye free services use karo — har 5 minute me check karte hain aur down hone par email bhejte hain:

| Service | URL | Free plan |
|---|---|---|
| **UptimeRobot** | https://uptimerobot.com | 50 monitors, 5-min interval |
| **Better Stack** | https://betterstack.com | 10 monitors |
| **Healthchecks.io** | https://healthchecks.io | 20 checks |

Setup: UptimeRobot → Add New Monitor → HTTP(s) → URL `http://VM_IP:5000/health` → Interval 5 min → Create.

**Ab tumhare paas 3 layers hain:** app-level metrics (Prometheus), server-level metrics (Node Exporter), external uptime (UptimeRobot). Report me ye diagram banao 👍

---

## 11. Screenshots & Report

> **Sabse important section!** Professor tumhara code nahi padhenge — **report aur screenshots** dekhenge.
> Achhe screenshots = zyada marks. Ye cheez seriously lo.

### 11.1 Ye screenshots lo (exact order me, checklist)

**A. Application (5)**
- [ ] A1. Login page
- [ ] A2. Dashboard (stats ke saath)
- [ ] A3. Students list (search/filter use karte hue)
- [ ] A4. Add Student form (bhar ke)
- [ ] A5. Validation error (marks = 150 daal ke)

**B. Git & GitHub (4)**
- [ ] B1. `git log --oneline --graph` terminal output
- [ ] B2. GitHub repo ka main page (files ke saath)
- [ ] B3. Commits history page
- [ ] B4. Pull Request page (merged wala)

**C. Tests (3)**
- [ ] C1. `pytest -v` — sab green ✅
- [ ] C2. **Jaan-boojh kar fail kiya hua test** (red ❌) ← *most valuable*
- [ ] C3. Test report `reports/results.xml`

**D. Docker (6)**
- [ ] D1. `docker build` output (stages ke saath)
- [ ] D2. `docker images` — image dikhti hui
- [ ] D3. `docker run` + `docker ps` (status `healthy`)
- [ ] D4. `curl localhost:5000/health` output
- [ ] D5. `docker logs` output
- [ ] D6. **Docker Hub pe tumhari image ka page** 🎓

**E. Jenkins (6)**
- [ ] E1. Jenkins dashboard
- [ ] E2. Pipeline job configuration page (SCM + Jenkinsfile path)
- [ ] E3. **Build SUCCESS — Stage View** (green boxes) 🎓
- [ ] E4. Console Output (stages ke logs)
- [ ] E5. Test Result page (JUnit)
- [ ] E6. **Build FAILURE** (red) ← *most valuable*

**F. GitHub Actions (3)**
- [ ] F1. Actions tab — workflow runs (green ticks)
- [ ] F2. Ek run ke andar jobs expanded
- [ ] F3. Artifacts / logs

**G. Cloud Deployment (4)**
- [ ] G1. Cloud console — VM instance `RUNNING` (IP dikhta hua)
- [ ] G2. SSH connection terminal
- [ ] G3. VM pe `docker ps`
- [ ] G4. **Browser me `http://VM_IP:5000` — LIVE APP** 🎓🎓

**H. Ansible (5)**
- [ ] H1. `ansible all -m ping` → `"ping": "pong"` 🎓
- [ ] H2. `provision.yml` ka PLAY RECAP (`changed=8`)
- [ ] H3. **Dobara chalane par `changed=0`** — idempotency proof 🎓🎓
- [ ] H4. `deploy.yml` ka deployment summary
- [ ] H5. `site.yml` ka full run

**I. Monitoring (6)**
- [ ] I1. `curl /metrics` output
- [ ] I2. **Prometheus → Status → Targets** (sab UP green) 🎓
- [ ] I3. Prometheus graph (koi query chala ke)
- [ ] I4. Prometheus → Status → Rules (alert rules)
- [ ] I5. **Grafana dashboard** (graphs ke saath, load generate karne ke baad) 🎓🎓
- [ ] I6. **Alert FIRING** (app ko stop karke) 🎓

**J. End-to-End Proof (1 — sabse important)**
- [ ] J1. Ek screen pe split: code change → git push → Jenkins build running → app live update

**Total: ~43 screenshots.** Har ek ka naam wahi rakho (`A1-login-page.png`) taaki report me reference karna easy ho.

### 11.2 Screenshots kaise lo

| OS | Shortcut |
|---|---|
| Windows | `Win + Shift + S` (snip) ya `PrtScn` (full) |
| Mac | `Cmd + Shift + 4` (area) ya `Cmd + Shift + 3` (full) |
| Linux | `PrtScn` ya `gnome-screenshot -a` |

> 💡 **Har screenshot me terminal ka prompt dikhna chahiye** (username + path) — isse proof hota hai ki tumne khud kiya hai.
> 💡 Terminal ko **fullscreen** karke screenshot lo — text chhota nahi dikhega.
> 💡 **Dark theme** terminal use karo — print/report me professional lagta hai.

### 11.3 Report ka format

**Cover Page:**
```
        [College Logo]

   TAE-II PROJECT REPORT

   StudentDesk — Student Management System
   with End-to-End DevOps Pipeline

   Subject: ______________
   Class:   ______________
   Roll No: ______________
   Name:    ______________
   Guide:   Prof. ______________

   Submitted: 28 September 2026
```

**Report Structure (15-25 pages):**

| # | Section | Content | Pages |
|---|---|---|---|
| 1 | Abstract | 1 paragraph — kya banaya, kaun-kaun se tools | 1 |
| 2 | Introduction | Problem statement, objective, scope | 1 |
| 3 | System Architecture | Block diagram (niche diya hai) | 1 |
| 4 | Technology Stack | Table — tool + version + kyun choose kiya | 1 |
| 5 | Application Design | Features, ER diagram, screenshots (A1-A5) | 2 |
| 6 | Version Control (Git) | Branch strategy, commit convention, screenshots (B1-B4) | 1 |
| 7 | Testing Strategy | Unit/Integration/API tests, 35 tests, screenshots (C1-C3) | 2 |
| 8 | Containerization (Docker) | Dockerfile explanation, layer caching, compose, screenshots (D1-D6) | 2 |
| 9 | CI/CD — Jenkins | Pipeline stages table, Jenkinsfile, screenshots (E1-E6) | 3 |
| 10 | CI/CD — GitHub Actions | Workflow, comparison with Jenkins, screenshots (F1-F3) | 1 |
| 11 | Deployment | Cloud VM setup, screenshots (G1-G4) | 2 |
| 12 | Configuration Management (Ansible) | Inventory, playbooks, idempotency, screenshots (H1-H5) | 2 |
| 13 | Monitoring & Logging | Prometheus/Grafana architecture, PromQL, alerts, screenshots (I1-I6) | 2 |
| 14 | Results & Observations | Pipeline timing, test coverage, image size | 1 |
| 15 | Challenges & Solutions | 5-6 real problems jo aaye aur kaise solve kiye | 1 |
| 16 | Conclusion & Future Scope | 1 page | 1 |
| 17 | References | Official docs ke links | 1 |

**Architecture Diagram (report me draw karo — draw.io ya hand-drawn scan):**

```
┌──────────────┐     git push      ┌──────────────┐
│  DEVELOPER   │ ────────────────→ │    GITHUB    │
│  (VS Code)   │                   │  Repository  │
└──────────────┘                   └──────┬───────┘
                                          │ webhook
                                          ↓
                                   ┌──────────────┐
                                   │   JENKINS    │
                                   │  (CI/CD)     │
                                   └──────┬───────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              ↓                           ↓                           ↓
      ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
      │ Build        │           │ Test         │           │ Docker Build │
      │ (compileall) │           │ (pytest 35)  │           │ + Smoke Test │
      └──────────────┘           └──────────────┘           └──────┬───────┘
                                                                   ↓
                                                           ┌──────────────┐
                                                           │  Docker Hub  │
                                                           │  / GHCR      │
                                                           └──────┬───────┘
                                                                  ↓
                                                ┌─────────────────────────────┐
                                                │      ANSIBLE (deploy.yml)   │
                                                └─────────────┬───────────────┘
                                                              ↓
                                                ┌─────────────────────────────┐
                                                │        CLOUD VM             │
                                                │  ┌───────────────────────┐  │
                                                │  │  StudentDesk Container│  │
                                                │  │  :5000                │  │
                                                │  └───────────┬───────────┘  │
                                                │              │ /metrics     │
                                                │  ┌───────────↓───────────┐  │
                                                │  │ PROMETHEUS :9090      │  │
                                                │  │ NODE-EXPORTER :9100   │  │
                                                │  │ GRAFANA :3000         │  │
                                                │  └───────────────────────┘  │
                                                └─────────────────────────────┘
                                                              ↓
                                                    📊 Live Dashboard + Alerts
```

**"Challenges & Solutions" section ke liye ready answers (real lagenge):**

| Challenge | Solution |
|---|---|
| Jenkins container se Docker commands nahi chal rahe the | `/var/run/docker.sock` mount kiya aur `docker.io` CLI install kiya Jenkins image me |
| `pytest` me "Duplicated timeseries in CollectorRegistry" error | Prometheus metrics ko function ke andar se hatakar module level pe define kiya (registry process-global hota hai) |
| GitHub webhook `localhost` URL accept nahi kar raha tha | Jenkins ko cloud VM pe shift kiya / ngrok tunnel use kiya |
| Docker image 900MB ki ban rahi thi | `python:3.12-slim` base image + `--no-cache-dir` + `.dockerignore` se 245MB pe laya |
| Cloud VM ka port 5000 bahar se access nahi ho raha tha | Security Group me Ingress Rule add kiya + UFW allow kiya + Oracle ke iptables rules hataye |
| Container restart pe SQLite data chala jata tha | Named Docker volume (`-v studentdesk_data:/app/instance`) mount kiya |
| Build har baar 4 minute le raha tha | `requirements.txt` ko code se pehle COPY kiya → layer caching se 40 second pe aaya |

### 11.4 Submission email ka template

Deadline **28 September 2026** hai. Email aisa likho:

```
Subject: TAE-II Submission — [Roll No] [Name] — StudentDesk DevOps Pipeline

Respected Sir/Ma'am,

Please find below my TAE-II project submission.

📌 PROJECT
   Name        : StudentDesk — Student Management System
   Description : Flask-based web application with a complete end-to-end
                 DevOps pipeline (Git → Jenkins → Docker → Cloud → Ansible → Monitoring)

🔗 LINKS
   GitHub Repo : https://github.com/YOUR_USERNAME/studentdesk
   Live App    : http://VM_IP:5000        (username: admin / password: admin123)
   Docker Hub  : https://hub.docker.com/r/YOUR_USERNAME/studentdesk
   Jenkins     : http://VM_IP:8080        (screenshots attached)

🛠️ TOOLS IMPLEMENTED
   • Git & GitHub        — version control, branching, PR workflow
   • Jenkins             — 9-stage declarative pipeline (build, test, docker, deploy)
   • GitHub Actions      — parallel CI matrix + CodeQL security scan
   • Docker              — containerized app, Docker Compose, multi-service stack
   • Ansible             — 4 playbooks (provision, deploy, monitoring, rollback)
   • Cloud VM            — Ubuntu 24.04 on [Oracle Cloud / AWS EC2]
   • Prometheus + Grafana— metrics, dashboards, 6 alert rules
   • pytest              — 35 automated tests (unit + integration + API)

📊 PIPELINE FLOW
   Developer → Git Repository → Jenkins → Build & Test → Docker Image
             → Deployment → Monitoring

📎 ATTACHED
   1. Project Report (PDF)
   2. Screenshots folder (ZIP)
   3. Demo video link: [Google Drive / YouTube unlisted]

Thank you.

Regards,
[Your Name]
[Roll Number]
[Class / Branch]
[Phone]
```

> 💡 **Demo video bana lo (3-5 min)** — phone se screen record karke:
> 1. App chalao (30 sec)
> 2. Code change karo, git push (30 sec)
> 3. Jenkins build apne aap start hoti dikhao (60 sec)
> 4. Docker image banti dikhao (30 sec)
> 5. Browser me live app refresh (30 sec)
> 6. Grafana dashboard (30 sec)
> Google Drive pe upload karo → "Anyone with the link can view" → link email me daalo.

---

## 12. Viva & Demo Questions

> In sab ke answers yaad kar lo. Ye 90% questions cover kar lenge.

### Git / GitHub
1. **Git aur GitHub me fark?** — Git ek *tool* hai (version control system) jo tumhare laptop pe chalta hai. GitHub ek *service/platform* hai jo Git repos ko internet pe host karta hai, plus collaboration features (PR, Issues, Actions).
2. **`git pull` aur `git fetch` me fark?** — `fetch` sirf remote changes download karta hai (safe). `pull` = `fetch` + `merge` (turant local branch me merge kar deta hai).
3. **`git merge` aur `git rebase`?** — Merge: dono branches ki history combine hoti hai, ek merge commit banta hai (history preserve). Rebase: tumhare commits ko target branch ke top pe "replay" karta hai (linear history, par shared branch pe dangerous).
4. **`.gitignore` kyun?** — Build artifacts, dependencies, secrets, DB files ko repo me jaane se rokta hai. Repo chhoti aur clean rehti hai.
5. **HEAD kya hai?** — Ek pointer jo current checked-out commit ko point karta hai.
6. **Merge conflict kab aata hai aur kaise solve karte ho?** — Jab 2 log same file ki same lines badalte hain. Git `<<<<<<<`, `=======`, `>>>>>>>` markers laga deta hai — manually decide karo kaunsa code rakhna hai, markers hatao, `git add`, `git commit`.

### Jenkins / CI-CD
7. **CI, CD, aur CD (Deployment) me fark?**
   - **Continuous Integration** — code frequently merge hota hai, har merge pe build + test automatically chalta hai
   - **Continuous Delivery** — code hamesha deploy-ready rehta hai, par deploy **manually** trigger hota hai
   - **Continuous Deployment** — tests pass hote hi **automatically** production pe deploy ho jata hai
8. **Jenkinsfile kya hai? Declarative vs Scripted pipeline?**
   - Jenkinsfile = pipeline ka code, repo me stored (Pipeline-as-Code)
   - **Declarative** — structured syntax (`pipeline { stages { stage {} } }`), padhne me easy, validation built-in. Hum yahi use kar rahe hain.
   - **Scripted** — Groovy scripting (`node { }`), zyada flexible par complex
9. **Jenkins me agent/master kya hai?** — Master (controller) scheduling aur UI handle karta hai; agents (build nodes) actual build chalate hain. Isse load distribute hota hai aur master secure rehta hai.
10. **Pipeline fail ho jaye to kya hota hai?** — Us stage pe ruk jati hai, aage ke stages skip ho jate hain, `post { failure }` block chalta hai, build red mark hoti hai, aur (configure kiya ho to) email notification jati hai.
11. **Credentials ko code me kyun nahi likhte?** — Security. Code public repo me chala jata hai, history me hamesha rehta hai. Jenkins credentials encrypted store karta hai aur logs me `***` se mask kar deta hai.
12. **`when { branch 'main' }` kyun lagaya?** — Taaki feature branches pe sirf tests chalein, expensive Docker push aur production deploy sirf `main` pe ho.

### Docker
13. **Container aur Virtual Machine me fark?** 🎓 *Most asked*
    - **VM** — poora guest OS (kernel + OS + app) hypervisor pe chalta hai. Heavy (GBs), slow boot (minutes), resource waste.
    - **Container** — host ka kernel share karta hai, sirf app + libraries pack hoti hain. Light (MBs), boot seconds me, ek machine pe hundreds chal sakte hain.
    - Analogy: VM = poora alag ghar; Container = same building ke alag flats.
14. **Image aur Container?** — Image = read-only template/blueprint (jaise class). Container = image ka running instance (jaise object). Ek image se kai containers ban sakte hain.
15. **Docker layer caching kaise kaam karti hai?** — Har Dockerfile instruction ek layer banata hai. Agar instruction aur uske pehle ki saari layers unchanged hain to Docker cached layer use karta hai. Isliye `requirements.txt` ko code se pehle COPY karte hain — dependencies wala layer cache me rehta hai.
16. **`CMD` aur `ENTRYPOINT`?** — `CMD` default command hai jo `docker run <image> <new-command>` se **override** ho jata hai. `ENTRYPOINT` fixed command hai, `docker run` ke args usme **append** hote hain (override karna mushkil).
17. **`COPY` aur `ADD`?** — `COPY` sirf local files copy karta hai (recommended). `ADD` extra features rakhta hai — URL se download, tar auto-extract. Best practice: `COPY` use karo jab tak `ADD` ki khas feature na chahiye.
18. **`docker stop` aur `docker kill`?** — `stop` = SIGTERM bhejta hai (graceful shutdown, 10s wait) phir SIGKILL. `kill` = directly SIGKILL (force, data loss risk).
19. **Volume kyun chahiye?** — Container ka filesystem ephemeral hai — delete hote hi data gaya. Volume host pe persist hota hai, isliye DB data bachane ke liye.
20. **Image size kam kaise kiya?** — `python:3.12-slim` base, `--no-cache-dir`, `.dockerignore`, non-root user, aur (optionally) multi-stage build. 900MB → 245MB.
21. **Container ko non-root user me kyun chalate hain?** — Security. Agar app compromise ho jaye to attacker ko container ke andar root milega, par host pe nahi — blast radius chhota rehta hai.

### Ansible
22. **Ansible aur Jenkins me fark?** — Jenkins = **CI/CD orchestration** (kab build/test/deploy trigger karna hai). Ansible = **configuration management** (server pe kya install karna hai, kaise configure karna hai). Dono complementary hain — Jenkins Ansible ko call kar sakta hai.
23. **Idempotency kya hai?** 🎓 — Ek operation ko kitni baar bhi chalao, system ki final state same rehti hai aur side-effects repeat nahi hote. Playbook dobara chalane par `changed=0` aata hai agar sab already sahi hai.
24. **Ansible agentless kaise hai?** — Ansible ko target machine pe koi agent install nahi karna padta. Wo **SSH** se connect karta hai, ek chhota Python module push karta hai, execute karta hai, result JSON me laata hai, aur module hata deta hai.
25. **Playbook, Play, Task, Module, Role?**
    - **Module** — atomic unit of work (`apt`, `copy`, `service`)
    - **Task** — ek module ka ek call with parameters
    - **Play** — tasks ka group jo ek host group pe chalta hai
    - **Playbook** — plays ka collection (YAML file)
    - **Role** — reusable, organized playbook structure (tasks/vars/templates/handlers folders)
26. **Handler kab chalta hai?** — Sirf jab koi task `notify:` se use trigger kare **aur** wo task `changed` ho. Example: config file badli → `notify: restart prometheus` → handler service restart karta hai. Config nahi badli to restart nahi hoga.
27. **Inventory kya hai? Static vs Dynamic?** — Static = `hosts.ini` file me manually IPs likhe. Dynamic = cloud API se automatically fetch (AWS EC2 plugin, Oracle plugin) — jab servers auto-scale hote hain tab useful.
28. **`--check` (dry run) kya karta hai?** — Bataata hai ki kya-kya change **hota** agar actually chalate, par kuch change nahi karta. Production pe risky playbook chalane se pehle safe verification.

### Monitoring
29. **Prometheus kaise metrics collect karta hai?** — **Pull model**. Prometheus har `scrape_interval` (15s) pe targets ke `/metrics` endpoint pe HTTP GET karta hai aur response parse karke apne time-series DB me store karta hai. (Pushgateway bhi hota hai short-lived jobs ke liye.)
30. **Counter, Gauge, Histogram me fark?** 🎓
    - **Counter** — monotonically increasing (total requests, total errors). Reset sirf process restart pe. Use `rate()` / `increase()`.
    - **Gauge** — up-down dono (current memory, temperature, active users, student count).
    - **Histogram** — observations ko configurable buckets me count karta hai → percentile/quantile calculate kar sakte ho (p95 latency).
    - **Summary** — Histogram jaisa par quantiles client-side calculate karta hai (aggregate nahi kar sakte across instances).
31. **PromQL kya hai?** — Prometheus Query Language. Example: `rate(studentdesk_http_requests_total[5m])` = last 5 minute ki average per-second request rate.
32. **Grafana aur Prometheus ka relation?** — Prometheus = data store + query engine. Grafana = visualization layer. Grafana Prometheus ko datasource ki tarah query karta hai aur dashboards banata hai. Grafana khud data store nahi karta.
33. **Push vs Pull monitoring?** — Pull (Prometheus): server targets se khud data kheenchta hai — simple, target down hone ka pata chal jata hai (`up == 0`). Push (StatsD, CloudWatch): app khud data bhejti hai — firewalls/NAT ke peeche ke targets ke liye better.
34. **Logs aur Metrics me fark?** — Metrics = **aggregate numbers over time** (kitne requests/sec, CPU %). Cheap to store, fast to query, alerting ke liye best. Logs = **individual events with detail** (kaunsi request me kya error aaya). Debugging ke liye best, storage expensive. Dono complementary hain.
35. **Agar app down ho jaye to alert kaise milega?** — Prometheus ka `up{job="studentdesk-app"} == 0` rule 1 minute tak true rehne par `AppIsDown` alert FIRE karta hai → Alertmanager → email/Slack. External UptimeRobot bhi independently `/health` check karta hai.

### General DevOps
36. **DevOps kya hai?** — Ek culture/practice jisme Development aur Operations teams collaborate karti hain, automation pe focus ke saath, taaki software **jaldi, reliably aur frequently** deliver ho sake. Tool nahi, mindset hai — tools (Git, Jenkins, Docker, Ansible) usko implement karte hain.
37. **DevOps lifecycle ke stages?** — Plan → Code → Build → Test → Release → Deploy → Operate → Monitor → (feedback loop wapas Plan pe)
38. **Shift-left testing kya hai?** — Testing ko development cycle me **jaldi** lana (unit tests developer ke laptop pe hi, PR pe CI), bajaye end me QA team pe chhodne ke. Bugs saste me pakde jate hain.
39. **12-Factor App kya hai?** — Cloud-native apps banane ke 12 principles. Humne 3 follow kiye: (III) Config environment me, (XI) Logs ko event streams ki tarah treat karo (stdout), (VI) Processes stateless rakho.
40. **Infrastructure as Code (IaC)?** — Infrastructure (servers, networks, config) ko machine-readable files me define karna — Ansible playbooks, Terraform. Fayde: version control, repeatability, review, disaster recovery.
41. **Blue-Green / Canary deployment?** — Blue-Green: 2 identical environments, traffic ek jhatke me switch. Canary: naya version chhote % traffic pe release karo, metrics dekho, theek ho to badhao.
42. **Is pipeline me rollback kaise karoge?** — `ansible/playbooks/rollback.yml` se previous image tag pe wapas ja sakte hain. Docker Hub pe har build ka unique tag (`BUILD_NUMBER-GIT_SHA`) stored hai, isliye koi bhi purana version pull karke chala sakte ho.
43. **Production me kya improve karoge? (Future scope)** 🎓
    - SQLite → **PostgreSQL/MySQL** (concurrency ke liye)
    - **Terraform** se infrastructure provisioning
    - **Kubernetes** pe orchestration (auto-scaling, self-healing)
    - **Trivy/Snyk** se container image vulnerability scanning
    - **SonarQube** se code quality analysis
    - **ELK / Loki** se centralized log aggregation
    - **JWT-based authentication** + RBAC
    - **Load balancer** + multiple replicas
    - **ArgoCD** se GitOps deployment
    - **Rate limiting** aur **CSRF protection**

---

## 13. Troubleshooting

> **Rule #1: Error message PADHO.** 90% baar answer usi me likha hota hai. Upar se neeche padho, sabse pehla error root cause hota hai (baaki uske cascade hote hain).

### Python / App

| Error | Reason | Fix |
|---|---|---|
| `python: command not found` | PATH me nahi | `python3` use karo, ya Windows pe Python reinstall karke "Add to PATH" tick karo |
| `ModuleNotFoundError: No module named 'flask'` | Venv activate nahi hai | `source venv/bin/activate` (ya `venv\Scripts\activate`) phir `pip install -r requirements.txt` |
| `pip: command not found` | pip install nahi | `python3 -m pip install ...` ya `sudo apt install python3-pip` |
| `externally-managed-environment` | System Python protect hai | Venv use karo (yahi karna chahiye), ya `pip install --break-system-packages` (not recommended) |
| `Port 5000 is already in use` | Kuch aur chal raha hai | `lsof -i :5000` (Mac/Linux) ya `netstat -ano \| findstr :5000` (Windows) → PID kill karo. Ya `PORT=5001 python run.py` |
| `Permission denied` | File permissions | `chmod +x script.sh` ya `sudo` |
| Browser me `Connection refused` | App chali hi nahi | Terminal me error dekho; `curl localhost:5000/health` |

### Git / GitHub

| Error | Reason | Fix |
|---|---|---|
| `fatal: not a git repository` | `git init` nahi kiya | `git init` chalao |
| `error: failed to push some refs` | Remote pe commits hain jo local pe nahi | `git pull origin main --rebase` phir `git push` |
| `fatal: remote origin already exists` | Remote dobara add kar rahe ho | `git remote set-url origin <NEW_URL>` |
| `Authentication failed` / `403` | Credentials expire | GitHub → Settings → Developer settings → Personal Access Token → naya banao → Credential Manager (Windows) me purana hatao |
| `Permission denied (publickey)` | SSH key setup nahi | HTTPS URL use karo ya `ssh-keygen` + GitHub pe public key add karo |
| `Updates were rejected because the remote contains work` | GitHub pe README banaya tha | `git pull origin main --allow-unrelated-histories` phir push |
| Accidentally committed `venv/` | .gitignore baad me add kiya | `git rm -r --cached venv` → commit → push |

### Docker

| Error | Reason | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop nahi chal raha | Docker Desktop kholo, engine start hone do. Linux: `sudo systemctl start docker` |
| `permission denied ... docker.sock` | User docker group me nahi | `sudo usermod -aG docker $USER` → **logout/login** (ya `newgrp docker`) |
| `port is already allocated` | Port conflict | `docker ps` dekho, purana container `docker rm -f <name>`, ya alag port `-p 5001:5000` |
| `no matching manifest for linux/arm64` | Mac M1/M2 pe x86 image | `docker run --platform linux/amd64 ...` ya ARM-native image use karo |
| Build bahut slow hai | Cache miss | `.dockerignore` check karo (`.git`, `venv` exclude hain?), `requirements.txt` code se pehle COPY ho raha hai? |
| Container start hote hi exit ho jata hai | App crash | `docker logs <container>` dekho. Common: wrong `CMD`, missing env var |
| `docker compose` command not found | Purana Docker | `docker-compose` (hyphen) try karo, ya Docker Desktop update karo |
| Image bahut badi hai (1GB+) | Full base image | `python:3.12-slim` use karo, `.dockerignore` add karo, multi-stage build |

### Jenkins

| Error | Reason | Fix |
|---|---|---|
| `localhost:8080` nahi khul raha | Jenkins start nahi hua | `docker ps` / `docker logs jenkins`. Direct install: `sudo systemctl status jenkins` |
| `docker: command not found` in pipeline | Jenkins container me Docker CLI nahi | `docker exec -u root jenkins bash -c "apt update && apt install -y docker.io"` → `docker restart jenkins` |
| `permission denied` on docker.sock | Socket permissions | compose me `user: root` set karo, ya `chmod 666 /var/run/docker.sock` (dev only) |
| `python3: not found` in Jenkins | Python install nahi | Jenkins Docker image me: `docker exec -u root jenkins apt install -y python3 python3-venv python3-pip` |
| `curl: not found` in Jenkins | curl missing | `docker exec -u root jenkins apt install -y curl` |
| Pipeline me `credentials('dockerhub-creds')` fail | Credential ID galat | Manage Jenkins → Credentials → ID **exactly** `dockerhub-creds` hona chahiye |
| Build stuck / never finishes | Agent offline | Manage Jenkins → Nodes → built-in node `Online` hona chahiye |
| `junit` step se error | JUnit plugin nahi | Manage Jenkins → Plugins → **JUnit** install karo |
| `cleanWs` se error | Workspace Cleanup plugin nahi | Install karo, ya Jenkinsfile se `cleanWs()` line hata do |
| Webhook trigger nahi ho raha | `localhost` URL / plugin missing | Public IP ya ngrok use karo; **GitHub Integration** plugin install karo; fallback `Poll SCM H/2 * * * *` |
| Jenkins bahut slow hai | RAM kam | `JAVA_OPTS=-Xmx2048m` set karo, ya VM ka RAM badhao |

### Ansible

| Error | Reason | Fix |
|---|---|---|
| `UNREACHABLE! ... Connection timed out` | IP galat / firewall / VM band | IP check, security group me port 22, VM running hai? |
| `Permission denied (publickey)` | Key path galat | `ansible_ssh_private_key_file` sahi path? `chmod 600 key.pem`? |
| `sudo: a password is required` | become password chahiye | `--ask-become-pass` flag add karo, ya passwordless sudo setup |
| `No module named 'ansible'` | Install nahi / venv issue | `pip3 install ansible`, phir `ansible --version` |
| `couldn't resolve module/action: community.docker.docker_container` | Collection missing | `ansible-galaxy collection install community.docker community.general` |
| `yaml.scanner.ScannerError` | YAML syntax galat | Indentation **spaces** se karo (TAB nahi!), colons ke baad space, `ansible-lint` chalao |
| Playbook `changed` har baar dikha raha hai | Non-idempotent task | `command`/`shell` ki jagah proper module use karo (`apt`, `copy`, `file`), ya `creates:`/`changed_when:` add karo |
| Windows pe `ansible` nahi chal raha | Ansible Windows support nahi karta | WSL2 install karo, ya VM ke andar se chalao |

### Cloud / Network

| Problem | Fix |
|---|---|
| `http://VM_IP:5000` bahar se nahi khul raha | 1) Cloud **Security Group / Ingress Rule** me TCP 5000 allow (source `0.0.0.0/0`) 2) VM me `sudo ufw allow 5000/tcp` 3) Oracle: `sudo iptables -I INPUT 6 -p tcp --dport 5000 -j ACCEPT && sudo netfilter-persistent save` 4) `docker run -p 5000:5000` (0.0.0.0 bind, 127.0.0.1 nahi) |
| SSH disconnect ho jata hai | `~/.ssh/config` me `ServerAliveInterval 60` add karo |
| VM ka IP change ho gaya | Static/public IP reserve karo, ya har baar inventory update karo |
| Free tier me instance band ho gaya | Oracle: idle instances reclaim hoti hain — "Always Free" shape use karo aur instance ko `Running` rakho |
| DNS/domain chahiye HTTPS ke liye | **DuckDNS** (free subdomain) ya **Freenom**; phir Let's Encrypt certbot |

### Debugging ka systematic tarika (ye approach viva me batao)

```
1. Error message POORA padho (sirf last line nahi)
2. Layer identify karo: App? Docker? Network? Jenkins? Ansible?
3. Isolate karo — sabse chhota test case:
   - App chalti hai?          → python run.py, curl /health
   - Container chalta hai?    → docker run --rm -p 5000:5000 image, docker logs
   - VM se access?            → ssh ke andar curl localhost:5000
   - Bahar se access?         → laptop se curl VM_IP:5000
   - Jenkins?                 → Console Output step-by-step
4. Logs dekho: docker logs, journalctl -u jenkins, /var/log/, Grafana
5. Ek cheez badlo, test karo (multiple changes ek saath mat karo)
6. Solution mil jaye to note kar lo — report ke "Challenges" section me jayega
```

**Handy debug commands:**
```bash
# Network
curl -v http://localhost:5000/health
nc -zv VM_IP 5000                    # port open hai?
sudo ss -tulpn | grep 5000           # kaun sun raha hai?
traceroute VM_IP

# Docker
docker logs --tail 100 <container>
docker exec -it <container> sh
docker inspect <container> | grep -A5 NetworkSettings
docker network inspect studentdesk_studentdesk-net

# Linux
sudo systemctl status docker jenkins
sudo journalctl -u jenkins -f
free -h && df -h && top

# Python
python -c "from app import create_app; print(create_app())"
pip list | grep -i flask
```

---

## 14. Day-wise Plan (aaj se 28 September tak)

> Aaj **19 September 2026** hai. Deadline **28 September 2026**. = **9 din bache hain.**
> Roz **2-3 ghante** do. Ye plan follow karo:

| Din | Date | Kya karna hai | Guide section | Deliverable |
|---|---|---|---|---|
| **Day 1** | 19 Sep (Fri) | Saare accounts banao (GitHub, Docker Hub, Oracle/AWS). Git, Python, Docker, VS Code install karo. Sab verify karo. | §0, §1 | ✅ Toolchain ready |
| **Day 2** | 20 Sep (Sat) | Project folder lo, venv banao, dependencies install, app chalao, saare features click karke dekho, tests chalao | §2, §3 | ✅ App + 35 tests running |
| **Day 3** | 21 Sep (Sun) | GitHub repo banao, push karo, ek feature branch + PR banao. Screenshots A1-A5, B1-B4, C1-C3 lo. | §4 | ✅ Repo public, screenshots |
| **Day 4** | 22 Sep (Mon) | Docker: image build, container run, health check, volume, compose. Docker Hub pe push karo. Screenshots D1-D6. | §5 | ✅ Live image on Docker Hub |
| **Day 5** | 23 Sep (Tue) | Jenkins Docker me install karo, plugins, credentials, pipeline job banao, pehla build chalao. Screenshots E1-E5. | §6 | ✅ Green pipeline build |
| **Day 6** | 24 Sep (Wed) | GitHub Actions verify karo + branch protection. Jaan-boojh kar build FAIL karo (Jenkins + Actions dono) aur screenshots lo. Webhook setup karo. | §6.11, §6.12, §7 | ✅ Failure + auto-trigger proof |
| **Day 7** | 25 Sep (Thu) | Cloud VM banao, SSH karo, manually deploy karo, browser me live URL kholo. Screenshots G1-G4. | §8 | ✅ App LIVE on internet |
| **Day 8** | 26 Sep (Fri) | Ansible: install, inventory, ping test, provision → deploy → monitoring playbooks. Idempotency demo. Screenshots H1-H5. | §9 | ✅ Ansible automated deploy |
| **Day 9** | 27 Sep (Sat) | Prometheus targets verify, Grafana dashboard, load generate karo, alert test karo (container stop). Screenshots I1-I6. **Report likhna shuru karo.** | §10, §11 | ✅ Monitoring live + report draft |
| **Day 10** | 28 Sep (Sun) | Report complete karo, screenshots organize karo, 3-min demo video banao, **email bhejo** (subah bhejo, raat ka wait mat karo!) | §11.3, §11.4 | 🎓 **SUBMITTED** |

### ⚠️ Buffer aur risk management

- **Har din ke end me 30 min buffer rakho** — cheezein hamesha sochi se zyada time leti hain.
- **Sabse risky step:** Cloud VM (credit card, region availability, security groups). **Isko Day 7 tak mat taal do** — agar Day 1 pe hi account bana lo to approval me time mil jayega.
- **Plan B ready rakho:** Agar VM na mile to **Render.com** (§8.6) ya **VirtualBox** (§8.4). Pipeline same rahega, sirf "deployment target" section change hoga.
- **Roz ka kaam commit karo** — `git push` karte raho. Laptop crash ho gaya to GitHub pe sab safe hai.
- **Screenshots roz lo** — end me yaad nahi rahega kya kahan tha. Ek folder banao `TAE-II-screenshots/` aur naam `A1-login.png` format me rakho.
- **Report ka skeleton Day 3 se bana lo** (headings + placeholders), content end me bharo. Last din report likhna panic deta hai.

### 🎯 Minimum Viable Submission (agar time kam pad jaye)

Priority order me — upar wale zaroor karo:

| Priority | Item | Time |
|---|---|---|
| 🔴 **MUST** | Working app + tests (already done ✅) | — |
| 🔴 **MUST** | GitHub repo with code | 30 min |
| 🔴 **MUST** | Dockerfile + image build/run proof | 45 min |
| 🔴 **MUST** | Jenkins pipeline green build screenshot | 90 min |
| 🟠 **HIGH** | Deployment (Render.com sabse fast — 15 min) | 15-60 min |
| 🟡 **MEDIUM** | GitHub Actions green runs | 10 min (automatic) |
| 🟡 **MEDIUM** | Ansible playbook run | 60 min |
| 🟢 **BONUS** | Prometheus + Grafana dashboards | 45 min |
| 🟢 **BONUS** | Demo video | 30 min |

**MUST + HIGH = passing submission.** Baaki = extra marks.

---

## ✅ Final Submission Checklist

Email bhejne se pehle ye sab tick karo:

**Code & Repo**
- [ ] GitHub repo **public** hai aur link kaam kar raha hai
- [ ] README.md complete hai (features, setup, architecture)
- [ ] `venv/`, `.env`, `*.db` commit **nahi** hue
- [ ] Kam se kam 10 meaningful commits hain (ek hi "initial commit" nahi)
- [ ] Kam se kam 1 Pull Request merge hua hai

**App**
- [ ] Local pe `python run.py` se chal rahi hai
- [ ] `pytest -v` → 35 passed
- [ ] Live URL browser me khul raha hai
- [ ] Login ho raha hai, CRUD kaam kar raha hai

**Docker**
- [ ] `docker build` successful
- [ ] `docker run` → `/health` returns 200
- [ ] Image Docker Hub pe public hai

**Jenkins**
- [ ] Pipeline job bana hua hai
- [ ] Kam se kam 1 SUCCESS build
- [ ] Kam se kam 1 FAILURE build (intentional — proof of testing)
- [ ] Test results visible in Jenkins UI

**Ansible**
- [ ] `ansible all -m ping` → pong
- [ ] `provision.yml` successful
- [ ] `deploy.yml` successful
- [ ] Idempotency demonstrated (`changed=0` on rerun)

**Monitoring**
- [ ] Prometheus targets sab UP
- [ ] Grafana dashboard me graphs dikh rahe hain
- [ ] Ek alert test kiya (FIRING → RESOLVED)

**Report**
- [ ] Cover page with name, roll no, class
- [ ] Architecture diagram
- [ ] Sab tools ke sections with screenshots
- [ ] Challenges & Solutions section
- [ ] Future scope
- [ ] References
- [ ] PDF format me (Word nahi)
- [ ] Filename: `TAE-II_[RollNo]_[Name]_StudentDesk.pdf`

**Email**
- [ ] Subject line clear: `TAE-II Submission — [Roll No] [Name]`
- [ ] Report PDF attached
- [ ] Screenshots ZIP attached
- [ ] GitHub / Live / Docker Hub links working
- [ ] Demo video link (Drive permission = "anyone with link")
- [ ] **28 September 2026 se PEHLE bheja** — aakhri din ka wait mat karo!

---

## 📚 References (report me ye daalo)

| Resource | URL |
|---|---|
| Git official docs | https://git-scm.com/doc |
| GitHub Actions docs | https://docs.github.com/en/actions |
| Jenkins User Handbook | https://www.jenkins.io/doc/book/ |
| Jenkins Pipeline Syntax | https://www.jenkins.io/doc/book/pipeline/syntax/ |
| Docker Docs | https://docs.docker.com/ |
| Dockerfile Best Practices | https://docs.docker.com/build/building/best-practices/ |
| Docker Compose Spec | https://docs.docker.com/compose/compose-file/ |
| Ansible Documentation | https://docs.ansible.com/ansible/latest/ |
| Flask Documentation | https://flask.palletsprojects.com/ |
| pytest Documentation | https://docs.pytest.org/ |
| Prometheus Docs | https://prometheus.io/docs/introduction/overview/ |
| PromQL Basics | https://prometheus.io/docs/prometheus/latest/querying/basics/ |
| Grafana Docs | https://grafana.com/docs/grafana/latest/ |
| 12-Factor App | https://12factor.net/ |
| Gunicorn Docs | https://docs.gunicorn.org/ |
| Oracle Cloud Free Tier | https://www.oracle.com/cloud/free/ |
| AWS Free Tier | https://aws.amazon.com/free/ |

---

## 🎬 Ab kya karo?

1. **Aaj hi** GitHub aur Docker Hub account bana lo (10 minute)
2. **Aaj hi** Git, Python, Docker install kar lo (§1)
3. **Kal** app local pe chalao (§2, §3)
4. Baaki plan §14 ke table se follow karo

**Yaad rakho:**
> Perfect project se zyada **complete + documented + demonstrable** project marks dilata hai.
> Chhoti app + poori pipeline > badi app + adhuri pipeline.
>
> Aur haan — **har step ka screenshot lete jao**. Baad me wapas karna painful hai.

**All the best! 🚀**

---

*Guide version 1.0 — StudentDesk DevOps Project | Last updated: 19 September 2026*
