# 🎤 VIVA QUESTIONS — Revision Sheet

> Full answers: [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) §12
> Ye file = exam se 1 ghante pehle revise karne ke liye

---

## 🔥 TOP 10 (ye zaroor aayenge)

**1. Container aur VM me kya fark hai?**
VM me poora guest OS (kernel + OS + app) hypervisor pe chalta hai — GBs me size, minute me boot. Container host ka **kernel share** karta hai, sirf app + libs pack hoti hain — MBs me size, second me boot, ek machine pe hundreds chal sakte hain.
*Analogy:* VM = alag ghar; Container = same building ke alag flats.

**2. CI, CD (Delivery), CD (Deployment) — teeno ka fark?**
- **Continuous Integration** — code frequently merge, har merge pe auto build + test
- **Continuous Delivery** — hamesha deploy-ready, par deploy **manual** trigger
- **Continuous Deployment** — tests pass hote hi **automatically** production

**3. DevOps kya hai?**
Ek **culture/practice**, tool nahi — Dev aur Ops teams collaborate karti hain, automation ke saath, taaki software **jaldi, reliably, frequently** deliver ho. Tools (Git, Jenkins, Docker, Ansible) ise implement karte hain.

**4. Idempotency kya hai?**
Operation kitni baar bhi chalao, final state same, side-effects repeat nahi. Playbook dobara chalane par `changed=0`. Isse safely re-run kar sakte ho — drift correction ke liye bhi.

**5. Docker layer caching kaise kaam karti hai?**
Har instruction ek layer. Instruction + uske pehle ki saari layers unchanged → cached layer reuse. Isliye `COPY requirements.txt` **pehle**, `COPY .` baad me — dependency layer cache me rehta hai. Build 3 min → 15 sec.

**6. Jenkins aur Ansible ka fark?**
Jenkins = **CI/CD orchestration** (kab build/test/deploy trigger karna hai). Ansible = **configuration management** (server pe kya install/configure karna hai). Complementary — Jenkins Ansible ko call kar sakta hai.

**7. Counter, Gauge, Histogram?**
- **Counter** — sirf badhta hai (total requests). `rate()` se use.
- **Gauge** — up/down dono (student count, RAM).
- **Histogram** — buckets me count → percentile (p95 latency).

**8. Prometheus pull karta hai ya push?**
**Pull.** Har `scrape_interval` (15s) pe target ke `/metrics` pe HTTP GET. Fayda: target down hone ka turant pata (`up == 0`). Short-lived jobs ke liye Pushgateway bhi hai.

**9. Logs aur Metrics me fark?**
Metrics = **aggregate numbers over time** (req/sec, CPU%) — cheap, fast, alerting ke liye. Logs = **individual detailed events** — debugging ke liye, storage expensive. Dono complementary.

**10. Agar pipeline fail ho jaye to kya hota hai?**
Us stage pe ruk jati hai, aage ke stages **skip**, `post { failure }` chalta hai, build red mark hoti hai, email alert (configured ho to). **Deploy nahi hota** — yahi quality gate hai.

---

## 🔀 Git

- **Git vs GitHub?** Git = tool (laptop pe). GitHub = hosting service (internet pe) + collaboration (PR, Issues, Actions).
- **`pull` vs `fetch`?** fetch = sirf download (safe). pull = fetch + merge.
- **`merge` vs `rebase`?** merge = history combine, merge commit banta hai. rebase = commits replay, linear history (shared branch pe dangerous).
- **`.gitignore` kyun?** Build artifacts, deps, secrets, DB ko repo me jaane se rokta hai.
- **HEAD?** Current checked-out commit ka pointer.
- **Merge conflict?** 2 log same lines badlein → `<<<<<<<` / `=======` / `>>>>>>>` markers → manually resolve → add → commit.
- **Commit convention?** `feat:` `fix:` `docs:` `test:` `chore:` `ci:` (Conventional Commits)

---

## 🏗️ Jenkins

- **Jenkinsfile?** Pipeline-as-Code — repo me stored, version controlled.
- **Declarative vs Scripted?** Declarative = structured (`pipeline { stages { stage {} } }`), easy, validated. Scripted = Groovy (`node {}`), flexible par complex. Hum Declarative use karte hain.
- **Master/Agent?** Master scheduling + UI; agents actual build. Load distribution + security.
- **Credentials code me kyun nahi?** Security — public repo/history me leak ho jate. Jenkins encrypt karta hai aur logs me `***` mask.
- **`when { branch 'main' }` kyun?** Feature branches pe sirf tests; expensive push/deploy sirf main pe.
- **"Pipeline script from SCM" kyun?** Pipeline bhi version control me — code aur pipeline ek saath change hote hain.

---

## 🐳 Docker

- **Image vs Container?** Image = read-only blueprint (class). Container = running instance (object). Ek image → kai containers.
- **`CMD` vs `ENTRYPOINT`?** CMD = default, `docker run <img> <cmd>` se override. ENTRYPOINT = fixed, args append.
- **`COPY` vs `ADD`?** COPY = local files only (recommended). ADD = extra (URL download, tar extract).
- **`stop` vs `kill`?** stop = SIGTERM (graceful, 10s) phir SIGKILL. kill = direct SIGKILL (data loss risk).
- **Volume kyun?** Container FS ephemeral — delete = data gaya. Volume host pe persist.
- **Non-root user kyun?** Security — container compromise hone pe host pe root nahi milega, blast radius chhota.
- **Image size kaise kam kiya?** `python:3.12-slim` + `--no-cache-dir` + `.dockerignore` + non-root + multi-stage. ~900MB → 245MB.
- **`EXPOSE` kya karta hai?** Sirf documentation — actual mapping `docker run -p` se.
- **`PYTHONUNBUFFERED=1` kyun?** Logs turant flush ho, buffer me na rukein.

---

## 🤖 Ansible

- **Agentless kaise?** SSH se connect → chhota Python module push → execute → JSON result → module hata do. Target pe kuch install nahi.
- **Playbook / Play / Task / Module / Role?** Module = atomic work (`apt`). Task = module ka call. Play = tasks ka group for a host group. Playbook = plays (YAML). Role = reusable organized structure.
- **Handler kab chalta hai?** Jab task `notify:` kare **aur** `changed` ho. Config nahi badli → service restart nahi.
- **Inventory static vs dynamic?** Static = manual `hosts.ini`. Dynamic = cloud API se auto-fetch (auto-scaling ke liye).
- **`--check`?** Dry run — kya change hota batata hai, actually nahi karta.
- **Ansible kyun, shell script kyun nahi?** Idempotency built-in, parallel execution, error handling, modules tested, readable YAML, inventory management, dry-run, roles se reusability.

---

## 📊 Monitoring

- **PromQL?** Prometheus Query Language. `rate(studentdesk_http_requests_total[5m])` = 5-min average per-sec rate.
- **Grafana aur Prometheus relation?** Prometheus = store + query engine. Grafana = visualization. Grafana khud data store nahi karta.
- **Push vs Pull?** Pull (Prometheus) = simple, down detection built-in. Push (StatsD/CloudWatch) = firewall/NAT ke peeche ke targets ke liye better.
- **Alert kaise milega app down hone par?** `up{job="studentdesk-app"} == 0` for 1m → AppIsDown FIRE → Alertmanager → email/Slack. Plus external UptimeRobot independently `/health` check karta hai.
- **`for: 1m` ka matlab?** Condition 1 minute tak continuously true rehni chahiye — flapping se false alerts nahi honge.

---

## 🎯 General DevOps

- **DevOps lifecycle?** Plan → Code → Build → Test → Release → Deploy → Operate → Monitor → (feedback wapas Plan)
- **Shift-left testing?** Testing ko cycle me jaldi lana (dev laptop, PR pe CI) — bugs saste me pakde jate hain.
- **12-Factor App?** Cloud-native principles. Humne follow kiye: (III) Config in env, (XI) Logs as streams (stdout), (VI) Stateless processes.
- **IaC (Infrastructure as Code)?** Infra ko machine-readable files me define (Ansible/Terraform) — version control, repeatability, review, DR.
- **Blue-Green / Canary?** Blue-Green = 2 identical envs, traffic ek jhatke me switch. Canary = chhote % traffic pe naya version, metrics dekho, phir badhao.
- **Rollback kaise?** `rollback.yml` se previous tag pe. Docker Hub pe har build ka unique tag (`BUILD_NUMBER-GIT_SHA`) → koi bhi version pull karke chala sakte ho.
- **Security pipeline me kahan?** CodeQL static analysis, Dependabot dependency updates, non-root container, secrets masking, branch protection, firewall rules, hashed passwords.

---

## 🚀 Future Scope (ye zaroor poochenge)

**Short term:**
- SQLite → **PostgreSQL** (concurrency)
- **Trivy / Snyk** — container vulnerability scanning
- **SonarQube** — code quality
- **JWT + RBAC** authentication
- CSRF protection + rate limiting

**Medium term:**
- **Terraform** — infrastructure provisioning
- **Loki / ELK** — centralized logs
- **Alertmanager** → email/Slack
- **Selenium / Playwright** — E2E browser tests

**Long term:**
- **Kubernetes** — auto-scaling, self-healing, rolling updates
- **Blue-green / canary** deployments
- **ArgoCD** — GitOps
- **OpenTelemetry + Jaeger** — distributed tracing

---

## 💬 Answer karne ka tarika

1. **Direct answer pehle** — ghumaao mat. ("Container VM se halka hota hai kyunki...")
2. **Apne project ka example do** — "Hamare project me humne `python:3.12-slim` use kiya, image 900MB se 245MB pe aa gayi"
3. **Fayda batao** — sirf definition nahi, "isliye humne ye kiya kyunki..."
4. **Nahi aata to jhooth mat bolo** — "Ye maine explore nahi kiya, par mera samajhna ye hai ki..." — honest answer galat answer se better hai
5. **Confident raho** — tumne khud kiya hai, tumhe pata hai

**Agar professor kuch aisa pooche jo tumne nahi kiya:**
> "Sir, wo maine implement nahi kiya kyunki [resource/time/scope constraint]. Par mujhe concept pata hai — [1-2 line explain]. Future scope me maine use include kiya hai."

---

## 📋 Demo ke din ka flow (10 min)

1. **App dikhao** (1 min) — login, dashboard, add/edit/delete, search
2. **Code change karo** (1 min) — VS Code me ek line badlo, `git commit && git push`
3. **Jenkins build apne aap start** (2 min) — dashboard pe live dekho, Console Output kholo
4. **Tests pass hote dikhao** (1 min) — Test Result page
5. **Docker image banti dikhao** (1 min) — Stage View me Docker Build green
6. **Deploy + live URL** (1 min) — browser me refresh
7. **Grafana dashboard** (1 min) — live metrics
8. **Alert demo** (1 min) — `docker stop studentdesk` → Prometheus FIRING
9. **Rollback dikhao** (1 min) — `ansible-playbook rollback.yml -e rollback_tag=1.0.0`

**Backup plan:** Internet slow ho ya VM down ho → **screenshots se dikhao**. Isliye pehle se sab screenshots ready rakho aur laptop pe ek local copy chalao.
