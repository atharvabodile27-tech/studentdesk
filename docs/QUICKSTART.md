# 🚀 QUICKSTART — 15 minute me project chalu karo

> Poori detail ke liye → [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) (2900 lines, step-by-step Hinglish)
> Report banane ke liye → [`REPORT_TEMPLATE.md`](REPORT_TEMPLATE.md)

---

## ⏱️ Level 0 — App local pe chalao (5 minute)

```bash
cd studentdesk
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
python run.py
```

👉 **http://localhost:5000** — login `admin` / `admin123`

**Tests:**
```bash
pytest -v          # 35 passed ✅
```

---

## 🐳 Level 1 — Docker (5 minute)

```bash
docker build -t studentdesk:1.0.0 .
docker run -d --name studentdesk -p 5000:5000 studentdesk:1.0.0
curl http://localhost:5000/health
docker ps                  # STATUS: Up (healthy)
docker logs -f studentdesk
```

**Pura stack (app + monitoring):**
```bash
docker compose --profile monitoring up -d
```

| URL | Kya |
|---|---|
| http://localhost:5000 | App |
| http://localhost:9090 | Prometheus |
| http://localhost:3000 | Grafana (admin/admin123) |

---

## 🔁 Level 2 — Git + GitHub (10 minute)

```bash
git init && git branch -M main
git add . && git commit -m "feat: initial StudentDesk app with DevOps pipeline"
git remote add origin https://github.com/YOUR_USERNAME/studentdesk.git
git push -u origin main
```

Repo pehle https://github.com/new se banao — **Public**, aur README/.gitignore tick **mat** karo.

---

## 🏗️ Level 3 — Jenkins (30 minute)

```bash
cd jenkins
docker compose up -d
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

👉 **http://localhost:8080** → password paste → Install suggested plugins → Admin user banao

**Plugins:** Docker, Docker Pipeline, JUnit, Credentials Binding, Workspace Cleanup, Timestamper, SSH Agent, GitHub Integration

**Credentials:** Manage Jenkins → Credentials → Add → Username with password → ID = `dockerhub-creds` ⚠️

**Job:** New Item → `studentdesk-pipeline` → Pipeline → Definition = **Pipeline script from SCM** → Git → repo URL → Branch `*/main` → Script Path `Jenkinsfile` → Save → **Build Now**

Full details → [`JENKINS_SETUP.md`](JENKINS_SETUP.md)

---

## ⚡ Level 3b — GitHub Actions (0 minute — automatic!)

Push karte hi `.github/workflows/ci-cd.yml` chal jayega.
Repo → **Actions** tab → green ticks dekho.

---

## ☁️ Level 4 — Cloud VM + Deploy (45 minute)

**VM lo:** Oracle Cloud Free Tier / AWS EC2 t2.micro / VirtualBox
**Image:** Ubuntu 24.04 LTS · **Ports open:** 22, 5000, 8080, 9090, 3000

```bash
ssh -i your-key.pem ubuntu@VM_IP

# VM pe
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER && newgrp docker
git clone https://github.com/YOUR_USERNAME/studentdesk.git && cd studentdesk
docker build -t studentdesk:1.0.0 .
docker run -d --name studentdesk --restart unless-stopped -p 5000:5000 \
  -v studentdesk_data:/app/instance studentdesk:1.0.0
curl http://localhost:5000/health
```

👉 **http://VM_IP:5000** — LIVE! 🎉

Full details → main guide §8

---

## 🤖 Level 5 — Ansible (45 minute)

```bash
pip3 install ansible
cd studentdesk/ansible
ansible-galaxy collection install -r requirements.yml

# inventory/hosts.ini me apna VM IP daalo, phir:
ansible all -i inventory/hosts.ini -m ping                      # → pong ✅
ansible-playbook playbooks/provision.yml -i inventory/hosts.ini # server ready
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini    # app deploy
ansible-playbook playbooks/monitoring.yml -i inventory/hosts.ini # Prometheus+Grafana

# Ya ek command me sab:
ansible-playbook site.yml -i inventory/hosts.ini
```

Full details → [`ANSIBLE_SETUP.md`](ANSIBLE_SETUP.md)

---

## 📊 Level 6 — Monitoring (30 minute)

1. **Prometheus** → http://VM_IP:9090 → Status → Targets → sab **UP**
2. **Grafana** → http://VM_IP:3000 (admin/admin123)
   → Dashboards → New → Import → `monitoring/grafana/dashboards/studentdesk.json`
   → Ya Dashboard ID **1860** (Node Exporter Full)
3. **Load generate karo:** `for i in $(seq 1 100); do curl -s http://VM_IP:5000/health >/dev/null; done`
4. **Alert test:** `docker stop studentdesk` → Prometheus `/alerts` → **AppIsDown FIRING** 🔴

Full details → [`MONITORING.md`](MONITORING.md)

---

## 📸 Level 7 — Report

43 screenshots ki checklist + report format → [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) §11
Ready-to-fill report → [`REPORT_TEMPLATE.md`](REPORT_TEMPLATE.md)

---

## 🗺️ Documentation Index

| File | Kab padho |
|---|---|
| **[GUIDE_HINGLISH.md](GUIDE_HINGLISH.md)** | ⭐ **MAIN GUIDE** — sab kuch, step by step, Hinglish |
| [QUICKSTART.md](QUICKSTART.md) | Ye file — fast reference |
| [JENKINS_SETUP.md](JENKINS_SETUP.md) | Jenkins install + pipeline detail |
| [ANSIBLE_SETUP.md](ANSIBLE_SETUP.md) | Ansible playbooks detail |
| [MONITORING.md](MONITORING.md) | Prometheus + Grafana detail |
| [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) | College report likhne ke liye |
| [SCREENSHOT_CHECKLIST.md](SCREENSHOT_CHECKLIST.md) | Kaun-kaun se screenshots lene hain |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Errors aa jayein to |
| [VIVA_QUESTIONS.md](VIVA_QUESTIONS.md) | Viva/demo ki taiyaari |

---

## 📅 Deadline: 28 September 2026

9 din bache hain (aaj 19 Sep). Din-wise plan → [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) §14

**Aaj hi karo:** GitHub + Docker Hub account banao, Git/Python/Docker install karo.
