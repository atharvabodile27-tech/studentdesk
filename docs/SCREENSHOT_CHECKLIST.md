# 📸 SCREENSHOT CHECKLIST — Print karo aur tick karte jao

> **43 screenshots.** Har ek ka naam isi format me rakho → `A1-login-page.png`
> Report me figure numbering isi order me hogi.

**Tips:**
- Terminal **fullscreen** karo, text chhota na lage
- Prompt (`user@host:path$`) dikhe — proof ki tumne khud kiya
- Browser me URL bar dikhe
- Dark theme = professional look
- Shortcut: Windows `Win+Shift+S` · Mac `Cmd+Shift+4` · Linux `PrtScn`

---

## A. Application (5)

- [ ] **A1** `A1-login-page.png` — Login page
- [ ] **A2** `A2-dashboard.png` — Dashboard with all 4 stat cards
- [ ] **A3** `A3-students-search.png` — Students list, search box me "Aarav" type karke
- [ ] **A4** `A4-add-student-form.png` — Add Student form bhara hua
- [ ] **A5** `A5-validation-error.png` — Marks = 150 daal ke error flash

## B. Git & GitHub (4)

- [ ] **B1** `B1-git-log.png` — `git log --oneline --graph --all`
- [ ] **B2** `B2-github-repo.png` — GitHub repo main page (files dikhte hue)
- [ ] **B3** `B3-commit-history.png` — Commits page
- [ ] **B4** `B4-pull-request.png` — Merged PR with green checks

## C. Tests (3)

- [ ] **C1** `C1-pytest-pass.png` — `pytest -v` → **35 passed**
- [ ] **C2** `C2-pytest-fail.png` — ❌ **intentionally failed test** (red output)
- [ ] **C3** `C3-junit-report.png` — `reports/results.xml` content

## D. Docker (6)

- [ ] **D1** `D1-docker-build.png` — `docker build` with all stages
- [ ] **D2** `D2-docker-images.png` — `docker images` output
- [ ] **D3** `D3-docker-ps.png` — `docker ps` → STATUS `Up (healthy)`
- [ ] **D4** `D4-health-check.png` — `curl localhost:5000/health` JSON response
- [ ] **D5** `D5-docker-logs.png` — `docker logs studentdesk` (gunicorn logs)
- [ ] **D6** `D6-docker-hub.png` — 🎓 Docker Hub repository page with tags

## E. Jenkins (6)

- [ ] **E1** `E1-jenkins-dashboard.png` — Jenkins home
- [ ] **E2** `E2-job-config.png` — Pipeline config page (SCM = Git, Script Path = Jenkinsfile)
- [ ] **E3** `E3-stage-view-success.png` — 🎓 **All 9 stages GREEN**
- [ ] **E4** `E4-console-output.png` — Console Output (test stage visible)
- [ ] **E5** `E5-test-results.png` — JUnit Test Result page
- [ ] **E6** `E6-build-failure.png` — 🎓 **RED build** (test fail → deploy skipped)

## F. GitHub Actions (3)

- [ ] **F1** `F1-actions-runs.png` — Actions tab, list of green runs
- [ ] **F2** `F2-actions-jobs.png` — Ek run expanded (matrix jobs + docker job)
- [ ] **F3** `F3-actions-logs.png` — Step logs inside a job

## G. Cloud Deployment (4)

- [ ] **G1** `G1-cloud-console.png` — VM instance RUNNING with public IP visible
- [ ] **G2** `G2-ssh-session.png` — SSH connected terminal
- [ ] **G3** `G3-vm-docker-ps.png` — `docker ps` on the VM
- [ ] **G4** `G4-live-app.png` — 🎓🎓 **Browser: `http://VM_IP:5000` — LIVE APP**

## H. Ansible (5)

- [ ] **H1** `H1-ansible-ping.png` — 🎓 `"ping": "pong"`
- [ ] **H2** `H2-provision-changed8.png` — PLAY RECAP `changed=8`
- [ ] **H3** `H3-idempotency-changed0.png` — 🎓🎓 **Rerun → `changed=0`**
- [ ] **H4** `H4-deploy-summary.png` — "✅ DEPLOYMENT SUCCESSFUL" debug output
- [ ] **H5** `H5-site-playbook.png` — `site.yml` full run recap

## I. Monitoring (6)

- [ ] **I1** `I1-app-metrics.png` — `curl /metrics` output
- [ ] **I2** `I2-prometheus-targets.png` — 🎓 Status → Targets, sab **UP** green
- [ ] **I3** `I3-prometheus-graph.png` — Koi PromQL query ka graph
- [ ] **I4** `I4-prometheus-rules.png` — Status → Rules (6 alerts)
- [ ] **I5** `I5-grafana-dashboard.png` — 🎓🎓 Grafana dashboard with live graphs
- [ ] **I6** `I6-alert-firing.png` — 🎓 AppIsDown **FIRING** (container stop karke)

## J. End-to-End (1)

- [ ] **J1** `J1-end-to-end.png` — 🎓🎓🎓 Split screen: code change → git push → Jenkins running → live app

---

**Total: 43**

🎓 = report me sabse zyada impact wale (ye 12 miss mat karna)

---

## Organization

```
TAE-II-submission/
├── TAE-II_RollNo_Name_StudentDesk.pdf      ← report
├── screenshots/
│   ├── A1-login-page.png
│   ├── ...
│   └── J1-end-to-end.png
├── screenshots.zip                          ← email attachment
└── demo-video-link.txt
```

## Auto-screenshot script (terminal captures)

```bash
#!/bin/bash
# save as capture.sh, run: bash capture.sh
mkdir -p shots && cd shots

ts() { echo -e "\n\$ $*\n"; }

{ ts "git log";      git log --oneline --graph --all -15; } > B1-git-log.txt
{ ts "pytest";       cd .. && pytest -v; }                  > C1-pytest-pass.txt
{ ts "docker images";docker images; }                       > D2-docker-images.txt
{ ts "docker ps";    docker ps -a; }                        > D3-docker-ps.txt
{ ts "health";       curl -s localhost:5000/health; }       > D4-health-check.txt
{ ts "logs";         docker logs --tail 30 studentdesk; }   > D5-docker-logs.txt
{ ts "metrics";      curl -s localhost:5000/metrics; }      > I1-app-metrics.txt
```

> Terminal text captures se kaam chal sakta hai, par **actual screenshots zyada marks dilate hain** — professor dekhna chahte hain ki tools ka UI use kiya hai.
