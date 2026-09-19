# TAE-II Project Report — TEMPLATE

> Isko copy karke apne details bharo. `[BRACKETS]` wali cheezein replace karni hain.
> Final output **PDF** me convert karo (Word/Google Docs/LaTeX — jo comfortable ho).

---

## 📄 COVER PAGE

```
                    [COLLEGE LOGO]

        [COLLEGE NAME], [CITY]
        Department of [Computer Engineering / IT]


                    TAE-II
            PROJECT REPORT  (2025–26)


   ┌─────────────────────────────────────────────┐
   │                                             │
   │              StudentDesk                    │
   │     Student Management System with an       │
   │       End-to-End DevOps Pipeline            │
   │                                             │
   │   Git → Jenkins → Docker → Cloud → Ansible  │
   │            → Prometheus/Grafana             │
   │                                             │
   └─────────────────────────────────────────────┘


   Submitted by  :  [YOUR FULL NAME]
   Roll Number   :  [ROLL NO]
   Class / Branch:  [T.E. / B.E. — Computer]
   Batch         :  [BATCH]

   Under the guidance of
   Prof. [GUIDE NAME]


   Date of Submission : 28 September 2026
```

---

## 📄 CERTIFICATE

```
CERTIFICATE

This is to certify that the project entitled "StudentDesk — Student Management
System with an End-to-End DevOps Pipeline" is a bona fide record of the work
carried out by [YOUR NAME], Roll No [ROLL NO], of class [CLASS], in partial
fulfilment of the requirement for the award of the TAE-II course during the
academic year 2025–26, under my guidance and supervision.

The work embodied in this report is original and has not been submitted
elsewhere for the award of any other degree or diploma.


Place: [CITY]                                   ______________________
Date:  28 September 2026                        Prof. [GUIDE NAME]
                                                (Project Guide)


                                                ______________________
                                                [HOD NAME]
                                                (Head of Department)
```

---

## 📄 ACKNOWLEDGEMENT

```
I would like to express my sincere gratitude to my project guide
Prof. [GUIDE NAME] for the constant guidance, valuable suggestions and
encouragement throughout the development of this project.

I am also thankful to [HOD NAME], Head of the Department of [DEPT], and to
all the faculty members and staff for providing the necessary infrastructure
and support.

Finally, I thank my family and friends for their patience and motivation
during the course of this work.

                                                        [YOUR NAME]
                                                        [ROLL NO]
```

---

## 📄 ABSTRACT

```
Modern software delivery demands speed, reliability and repeatability — goals
that manual build and deployment processes cannot meet. This project implements
a complete end-to-end DevOps pipeline around "StudentDesk", a web-based Student
Management System developed in Python using the Flask framework with an
SQLAlchemy-backed SQLite database.

Source code is versioned using Git and hosted on GitHub, where branching and
pull-request workflows enforce code review. Continuous Integration and
Continuous Deployment are automated through Jenkins using a declarative
nine-stage Jenkinsfile (Checkout → Environment Setup → Build → Unit Tests →
Application & API Tests → Docker Build → Container Smoke Test → Registry Push →
Deployment). An equivalent GitHub Actions workflow was also configured for
comparison, including a parallel Python-version test matrix and a CodeQL
security scan.

The application is containerized using Docker with a slim base image, layered
caching for fast rebuilds, a non-root runtime user and a built-in health check.
Docker Compose orchestrates a multi-service stack comprising the application,
Prometheus, Grafana and Node Exporter. Configuration management and automated
deployment to an Ubuntu cloud virtual machine are handled by Ansible through
four idempotent playbooks (provision, deploy, monitoring, rollback).

Monitoring is achieved with Prometheus scraping application-level metrics
(request counters, latency histograms and business gauges) exposed at a
/metrics endpoint, together with host-level metrics from Node Exporter; Grafana
visualises the data and six alert rules detect application downtime, high
latency, error spikes and host resource exhaustion. Logs follow the
twelve-factor principle of writing to standard output, with rotation configured
at the container runtime.

The project successfully demonstrates the complete DevOps flow
Developer → Git Repository → Jenkins → Build & Test → Docker Image →
Deployment → Monitoring, and validates that a broken commit is automatically
blocked from reaching production.

Keywords: DevOps, CI/CD, Jenkins, Docker, Ansible, Prometheus, Grafana, Flask,
GitHub Actions, Containerization, Infrastructure as Code, Monitoring.
```

---

## 📑 TABLE OF CONTENTS

```
1.  Introduction .................................................. 1
    1.1 Problem Statement
    1.2 Objectives
    1.3 Scope of the Project
2.  System Architecture ........................................... 3
    2.1 DevOps Pipeline Flow
    2.2 Component Diagram
3.  Technology Stack .............................................. 5
4.  Application Design & Implementation ........................... 7
    4.1 Features
    4.2 Data Model (ER Diagram)
    4.3 Design Patterns Used
    4.4 Screenshots
5.  Version Control with Git & GitHub ............................. 12
    5.1 Repository Structure
    5.2 Branching Strategy
    5.3 Commit Conventions
6.  Automated Testing ............................................. 15
    6.1 Test Pyramid
    6.2 Unit / Integration / API Tests
    6.3 Test Reports
7.  Containerization with Docker .................................. 18
    7.1 Dockerfile Design & Layer Caching
    7.2 Docker Compose Multi-Service Stack
    7.3 Image Registry (Docker Hub)
    7.4 Security Considerations
8.  Continuous Integration & Deployment — Jenkins ................. 22
    8.1 Jenkins Installation & Plugins
    8.2 Credentials Management
    8.3 Pipeline Stages Explained
    8.4 Successful and Failed Builds
    8.5 Webhook-based Automatic Triggering
9.  GitHub Actions — Alternative CI/CD ............................ 28
    9.1 Workflow Design
    9.2 Jenkins vs GitHub Actions Comparison
10. Cloud Deployment .............................................. 31
    10.1 Virtual Machine Provisioning
    10.2 Manual Deployment
    10.3 Firewall and Networking
11. Configuration Management with Ansible ......................... 34
    11.1 Inventory and Playbook Structure
    11.2 Provisioning, Deployment, Monitoring and Rollback
    11.3 Idempotency Demonstration
12. Monitoring and Log Management ................................. 39
    12.1 Prometheus Metrics and PromQL
    12.2 Grafana Dashboards
    12.3 Alerting
    12.4 Logging Strategy
13. Results and Observations ...................................... 45
14. Challenges Faced and Solutions ................................ 47
15. Conclusion and Future Scope ................................... 49
16. References .................................................... 51
```

---

## 1. INTRODUCTION

### 1.1 Problem Statement

```
Traditional software delivery involves manual steps for building, testing and
deploying an application. Each manual step introduces delay, human error and
inconsistency between developer machines and production servers. There is no
single place that answers the questions: "Is the application healthy?",
"Did the latest change break anything?" and "Can we roll back quickly?"

This project addresses these problems by building a small but complete web
application and wrapping it in a fully automated DevOps pipeline, so that every
code change is automatically built, tested, containerized, deployed and
monitored without human intervention.
```

### 1.2 Objectives

```
1.  To develop a functional web-based Student Management System with
    authentication, CRUD operations, search, validation and a REST API.
2.  To maintain the source code under Git version control with a proper
    branching strategy and pull-request based review workflow.
3.  To automate build and testing using Jenkins with a declarative pipeline
    stored as code (Jenkinsfile) in the repository.
4.  To write a comprehensive automated test suite (unit, integration and API)
    using pytest and publish machine-readable JUnit reports.
5.  To containerize the application with Docker using best practices —
    slim base image, layer caching, non-root user, health checks and volumes.
6.  To publish container images to a registry (Docker Hub / GHCR) with
    immutable, traceable tags.
7.  To deploy the application on a cloud virtual machine.
8.  To automate server configuration and deployment using Ansible playbooks
    and demonstrate idempotency and rollback capability.
9.  To implement monitoring using Prometheus and Grafana with application
    metrics, host metrics, dashboards and alerting rules.
10. To implement log management using structured application logs written to
    standard output, with container-level log rotation.
11. To validate that the pipeline blocks faulty code from reaching production.
```

### 1.3 Scope

```
The scope covers a single-node deployment of a monolithic Flask application
with a local embedded database, intended to demonstrate DevOps practices
end-to-end. Horizontal scaling, Kubernetes orchestration, centralized log
aggregation and blue-green deployment are considered outside the current scope
and are listed under Future Scope (Section 15).
```

---

## 2. SYSTEM ARCHITECTURE

### 2.1 DevOps Pipeline Flow

```
[Paste the ASCII architecture diagram from docs/GUIDE_HINGLISH.md §11.3 here,
 or recreate it in draw.io and insert as an image — image looks much better]
```

### 2.2 Component Description

| Component | Technology | Responsibility |
|---|---|---|
| Source Control | Git + GitHub | Version history, branching, pull requests, webhooks |
| CI/CD Server | Jenkins 2.x LTS | Pipeline orchestration, build, test, image build, deploy trigger |
| Secondary CI/CD | GitHub Actions | Parallel test matrix, CodeQL security scan, GHCR push |
| Application | Python 3.12 + Flask 3.1 | Web UI and REST API |
| Persistence | SQLite + SQLAlchemy 2.0 | Student and user data |
| Testing | pytest | 35 automated tests across 3 layers |
| Containerization | Docker 27.x | Image build and runtime isolation |
| Orchestration | Docker Compose v2 | Multi-container stack (app + monitoring) |
| Registry | Docker Hub / GHCR | Image distribution |
| Web Server | Gunicorn 23 | Production WSGI server |
| Config Management | Ansible 2.1x | Provisioning, deployment, monitoring setup, rollback |
| Metrics Collection | Prometheus 2.54 | Scrape, store and query time-series metrics |
| Host Metrics | Node Exporter 1.8 | CPU, memory, disk, network |
| Visualization | Grafana 11.2 | Dashboards and alert visualization |
| Compute | Ubuntu 24.04 LTS VM | Deployment target (Oracle Cloud / AWS EC2) |

---

## 3. TECHNOLOGY STACK — Justification

| Tool | Version | Why it was chosen |
|---|---|---|
| Python | 3.12 | Simple syntax, huge ecosystem, easy for beginners, well supported in CI images |
| Flask | 3.1.3 | Lightweight micro-framework; enough for a CRUD app without the overhead of Django |
| SQLAlchemy | 2.0.44 | ORM removes raw SQL, makes the data layer testable and database-portable |
| SQLite | built-in | Zero-configuration embedded database; ideal for demo, swappable via `DATABASE_URL` env var |
| Gunicorn | 23.0.0 | Production-grade WSGI server with multiple workers; Flask's dev server is single-threaded and not for production |
| pytest | 8.4.2 | Simple syntax, powerful fixtures, native JUnit XML output for Jenkins |
| Docker | 27.x | Industry-standard containerization; "build once, run anywhere" |
| Jenkins | 2.x LTS | Required by the syllabus; most widely deployed open-source CI server with 1800+ plugins |
| GitHub Actions | — | Zero-infrastructure CI, useful for comparison and as a free fallback |
| Ansible | 2.1x | Agentless configuration management using simple YAML; idempotent by design |
| Prometheus | 2.54 | Pull-based monitoring, powerful PromQL, native cloud-native ecosystem support |
| Grafana | 11.2 | Best-in-class dashboards, supports Prometheus out of the box |
| Ubuntu | 24.04 LTS | Most common server distribution, excellent documentation, free-tier availability |

---

## 4. APPLICATION DESIGN

### 4.1 Features

| # | Feature | Description |
|---|---|---|
| F1 | Authentication | Session-based admin login with hashed passwords (Werkzeug) |
| F2 | Dashboard | Total students, active count, pass rate, average marks, course-wise distribution, recent additions |
| F3 | Student listing | Paginated table of all students with grade and result |
| F4 | Search | Real-time filter by name, roll number or email |
| F5 | Course filter | Dropdown to filter students by course |
| F6 | Add student | Form with server-side validation and duplicate detection |
| F7 | Edit student | Update any field except roll number (immutable primary business key) |
| F8 | Delete student | Confirmation prompt before deletion |
| F9 | Automatic grading | Marks → grade (A+ … F) and PASS/FAIL computed by the model layer |
| F10 | REST API | `/api/students` (GET, POST), `/api/students/<id>` (GET, DELETE), `/api/stats` |
| F11 | Health endpoint | `/health` returns JSON status — used by Docker healthcheck, Jenkins smoke test and Prometheus |
| F12 | Metrics endpoint | `/metrics` exposes Prometheus counters, histograms and gauges |
| F13 | Validation | Marks range 0–100, numeric year, unique roll number and email |
| F14 | Seed data | 6 sample students and one admin user created on first run |

### 4.2 Data Model

```
┌──────────────────────────────────┐        ┌────────────────────────┐
│           STUDENT                │        │          USER          │
├──────────────────────────────────┤        ├────────────────────────┤
│ id          INTEGER  PK          │        │ id            INT  PK  │
│ roll_no     VARCHAR(20)  UNIQUE  │        │ username      UNIQUE   │
│ name        VARCHAR(100) NOT NULL│        │ password_hash VARCHAR  │
│ email       VARCHAR(120) UNIQUE  │        └────────────────────────┘
│ course      VARCHAR(50)          │
│ year        INTEGER              │
│ marks       FLOAT                │
│ status      VARCHAR(20)          │
│ created_at  DATETIME             │
└──────────────────────────────────┘

Derived (not stored, computed in model layer):
  grade  = f(marks)  →  A+ / A / B / C / D / E / F
  result = PASS if marks >= 40 else FAIL
```

**Grading scale:**

| Marks | Grade | Result |
|---|---|---|
| 90 – 100 | A+ | PASS |
| 80 – 89.99 | A | PASS |
| 70 – 79.99 | B | PASS |
| 60 – 69.99 | C | PASS |
| 50 – 59.99 | D | PASS |
| 40 – 49.99 | E | PASS |
| 0 – 39.99 | F | FAIL |

### 4.3 Design Patterns

| Pattern | Where | Benefit |
|---|---|---|
| **Application Factory** | `app/__init__.py` → `create_app()` | Allows creating separate app instances for testing with a different config; avoids global state |
| **Blueprints** | `routes/main.py`, `routes/auth.py`, `routes/api.py` | Separation of concerns; each module owns its routes |
| **Repository/ORM** | `models.py` with SQLAlchemy | Data access is abstracted; database can be swapped by changing `DATABASE_URL` |
| **Configuration Object** | `config.py` → `Config`, `TestConfig` | Environment-driven configuration (12-Factor Factor III) |
| **Decorator** | `login_required` | Cross-cutting authentication concern applied declaratively |
| **Fixtures** | `tests/conftest.py` | Reusable, isolated test setup with automatic teardown |

### 4.4 Screenshots

```
[Insert Screenshot A1 — Login page]
Figure 4.1: Login page with demo credentials

[Insert Screenshot A2 — Dashboard]
Figure 4.2: Dashboard showing aggregate statistics

[Insert Screenshot A3 — Student list with search]
Figure 4.3: Student listing with search and course filter

[Insert Screenshot A4 — Add student form]
Figure 4.4: Add-student form

[Insert Screenshot A5 — Validation error]
Figure 4.5: Server-side validation rejecting marks = 150

[Insert Screenshot — API response]
Figure 4.6: JSON response from /api/students
```

---

## 5. VERSION CONTROL

### 5.1 Repository Structure

```
[Paste the folder tree from README.md §Project Structure]
```

### 5.2 Branching Strategy

```
main                     — always deployable; protected branch
  └── feature/<name>     — new functionality, merged via Pull Request
  └── fix/<name>         — bug fixes, merged via Pull Request

Pull requests require the CI status checks "Build & Test (3.11)" and
"Build & Test (3.12)" to pass before merging (GitHub branch protection rule).
Direct pushes to main are blocked once protection is enabled.
```

### 5.3 Commit Convention

```
Conventional Commits format is followed:  <type>: <subject>

feat:     a new feature
fix:      a bug fix
docs:     documentation only
test:     adding or correcting tests
chore:    build process, dependencies, tooling
ci:       CI/CD configuration changes

Example history:
  a1b2c3d ci: add CodeQL security scan workflow
  e4f5g6h docs: add Ansible setup guide
  i7j8k9l test: add API error-case coverage (400/404/409)
  m0n1o2p feat: add course filter to student list
  q3r4s5t fix: reject marks outside 0-100 range
```

```
[Insert Screenshot B2 — GitHub repository main page]
Figure 5.1: Project repository on GitHub

[Insert Screenshot B3 — Commit history]
Figure 5.2: Commit history showing conventional commit messages

[Insert Screenshot B4 — Merged pull request]
Figure 5.3: Pull request with passing CI checks, merged into main
```

---

## 6. AUTOMATED TESTING

### 6.1 Test Pyramid

```
              ▲
             / \        E2E / Smoke (1)     — container /health after deploy
            /   \
           /─────\      Integration / API (22) — Flask routes + REST endpoints
          /       \
         /─────────\    Unit (12)             — grade() and result() logic
        /___________\

Total: 35 automated tests, executed in ~4 seconds
```

### 6.2 Test Distribution

| File | Layer | Tests | What is verified |
|---|---|---|---|
| `tests/test_unit.py` | Unit | 12 | Grade boundaries (90→A+, 40→E), result threshold (39.9→FAIL) |
| `tests/test_app.py` | Integration | 13 | Login/logout, access control redirect, dashboard render, form add/edit/delete, duplicate roll number rejection, marks range rejection, search filtering |
| `tests/test_api.py` | API | 9 | HTTP 200/201/400/404/409 status codes, JSON payload correctness, missing-field and invalid-input handling |
| `tests/test_metrics.py` | Feature | 2 | `/metrics` responds correctly whether or not `prometheus_client` is installed (graceful degradation) |

### 6.3 Test Isolation

```
Every test receives a fresh in-memory SQLite database (sqlite:///:memory:)
through a function-scoped pytest fixture in tests/conftest.py. The database is
created before the test and dropped afterwards, so:

  • tests never pollute the development database,
  • tests can run in any order,
  • tests can run in parallel,
  • a failing test cannot cause another test to fail.
```

### 6.4 Machine-Readable Reports

```
pytest -v --junitxml=reports/results.xml

produces a JUnit-format XML report that Jenkins (via the junit step) and
GitHub Actions (via upload-artifact) both consume. The Jenkins UI therefore
shows test counts, durations and full stack traces for failures without
reading console logs.
```

```
[Insert Screenshot C1 — pytest all green]
Figure 6.1: All 35 tests passing locally

[Insert Screenshot C2 — intentionally failing test]
Figure 6.2: Deliberately introduced defect detected by the test suite

[Insert Screenshot E6 — Jenkins build FAILURE]
Figure 6.3: Pipeline aborted at the test stage, preventing deployment
```

---

## 7. CONTAINERIZATION WITH DOCKER

### 7.1 Dockerfile Design

```
[Paste the Dockerfile here in a code block]
```

**Design decisions:**

| Decision | Rationale |
|---|---|
| `python:3.12-slim` base | ~130 MB instead of ~900 MB for the full image; smaller attack surface and faster pulls |
| `COPY requirements.txt` before `COPY .` | Layer caching — dependency layer is reused unless requirements change, cutting rebuild time from ~3 min to ~15 s |
| `pip install --no-cache-dir` | Prevents pip's download cache from bloating the image |
| `useradd` + `USER appuser` | Runs as non-root; limits blast radius if the container is compromised |
| `HEALTHCHECK` on `/health` | Docker marks the container `unhealthy` automatically, enabling orchestrators and operators to react |
| `PYTHONUNBUFFERED=1` | Logs are flushed immediately to stdout instead of being buffered |
| `EXPOSE 5000` | Documentation of the listening port |
| `CMD ["gunicorn", ...]` | Exec-form CMD (no shell wrapper) so signals reach Gunicorn correctly for graceful shutdown |
| `.dockerignore` | Excludes `.git`, `venv`, `instance`, tests and docs from the build context |

### 7.2 Image Statistics

```
[Fill in after building]

Base image           : python:3.12-slim
Final image size     : ______ MB
Build time (cold)    : ______ s
Build time (cached)  : ______ s
Number of layers     : ______
Runtime user         : appuser (UID ______)
```

### 7.3 Docker Compose Multi-Service Stack

```
[Paste docker-compose.yml here]

Services:
  app            — StudentDesk, port 5000, named volume for the database
  prometheus     — port 9090, mounts monitoring/prometheus.yml
  grafana        — port 3000, persistent volume for dashboards
  node-exporter  — port 9100, host metrics

The monitoring services are behind a Compose profile so that
`docker compose up -d app` starts only the application, while
`docker compose --profile monitoring up -d` starts the full stack.
All services share the user-defined bridge network `studentdesk-net`,
which provides DNS-based service discovery (Prometheus reaches the app as `app:5000`).
```

### 7.4 Registry Publishing

```
docker tag studentdesk:1.0.0 <dockerhub-user>/studentdesk:1.0.0
docker push <dockerhub-user>/studentdesk:1.0.0

Jenkins additionally tags every build with an immutable identifier:
    <build-number>-<git-short-sha>      e.g. 12-a1b2c3d

This makes every deployed artifact traceable back to the exact commit that
produced it, and allows instant rollback to any previous version.
```

```
[Insert Screenshot D1 — docker build output]
Figure 7.1: Multi-step Docker image build

[Insert Screenshot D3 — docker ps showing healthy]
Figure 7.2: Running container reporting a healthy status

[Insert Screenshot D6 — Docker Hub repository page]
Figure 7.3: Published image on Docker Hub
```

---

## 8. CONTINUOUS INTEGRATION & DEPLOYMENT — JENKINS

### 8.1 Installation

```
Environment  : Jenkins LTS (JDK 17) running inside a Docker container
Access       : http://localhost:8080
Data volume  : jenkins_home (persistent)
Docker access: /var/run/docker.sock bind-mounted so the pipeline can build
               and run images on the host engine
```

### 8.2 Plugins Installed

| Plugin | Purpose |
|---|---|
| Pipeline | Declarative Jenkinsfile support |
| Git | Source checkout |
| Docker / Docker Pipeline | Image build and container operations |
| JUnit | Test result parsing and visualization |
| Credentials Binding | Secure secret injection |
| Workspace Cleanup | Post-build workspace hygiene |
| Timestamper | Timestamped console output |
| SSH Agent | Remote deployment over SSH |
| GitHub Integration | Webhook-based triggering |
| Blue Ocean | Modern pipeline visualization |

### 8.3 Pipeline Stages

| # | Stage | Command / Action | Blocks deployment on failure |
|---|---|---|---|
| 1 | Checkout | `checkout scm`, print commit info | ✔ |
| 2 | Setup Python Env | `python3 -m venv`, `pip install -r requirements*.txt` | ✔ |
| 3 | Build | `python -m compileall -q app run.py` (syntax verification) | ✔ |
| 4 | Unit Tests | `pytest tests/test_unit.py --junitxml=reports/unit-results.xml` | ✔ |
| 5 | App & API Tests | `pytest tests/test_app.py tests/test_api.py --junitxml=reports/app-results.xml` | ✔ |
| 6 | Docker Build | `docker build -t studentdesk:${IMAGE_TAG} .` | ✔ |
| 7 | Smoke Test | Run the image, poll `/health` up to 10 times, print logs and fail if unhealthy | ✔ |
| 8 | Docker Push | Login with stored credentials, tag, push (`when { branch 'main' }`) | ✔ |
| 9 | Deploy | Remove old container, run new image, verify `/health` (`when { branch 'main' }`) | — |
| post | Always | Archive `reports/*.xml`, clean workspace, echo status | — |

```
[Insert the Jenkinsfile here as a code block]
```

### 8.4 Credentials Management

```
No secret appears anywhere in the repository or the pipeline script.

ID                  Kind                            Used by
dockerhub-creds     Username with password          Docker Push stage
vm-ssh-key          SSH Username with private key   Remote deployment (optional)

Jenkins encrypts these at rest and masks their values in console output.
```

### 8.5 Build Results

```
[Fill in from your Jenkins dashboard]

Total builds executed   : ______
Successful builds       : ______
Failed builds           : ______
Average pipeline time   : ______ minutes
Longest stage           : ______ (______ s)
```

```
[Insert Screenshot E3 — Stage View all green]
Figure 8.1: Successful pipeline run — all nine stages green

[Insert Screenshot E4 — Console output]
Figure 8.2: Console output of the test stage

[Insert Screenshot E5 — JUnit test results]
Figure 8.3: Test result report inside Jenkins

[Insert Screenshot E6 — Failed build]
Figure 8.4: Pipeline failure at the Unit Tests stage — Docker and deploy
             stages were skipped, proving the quality gate works
```

### 8.6 Automatic Triggering

```
A GitHub webhook (push event) posts to
    http://<JENKINS_HOST>:8080/github-webhook/
which triggers the pipeline within seconds of `git push`, with no manual
intervention. As a fallback, SCM polling (H/2 * * * *) checks the repository
every two minutes.
```

---

## 9. GITHUB ACTIONS

### 9.1 Workflow Design

```
[Paste .github/workflows/ci-cd.yml here]

Jobs:
  test    — matrix of Python 3.11 and 3.12; installs dependencies, runs a
            compile check, executes the full pytest suite, uploads the JUnit
            report as an artifact. Runs on pushes AND pull requests.
  docker  — depends on `test`; builds the image with Buildx, uses the GitHub
            Actions cache (type=gha) and pushes to GHCR with `latest` and
            commit-SHA tags. Runs only on pushes to main.
  deploy  — depends on `docker`; connects over SSH using repository secrets
            and restarts the container on the VM. Runs only on pushes to main.

Additional workflow: codeql.yml performs static security analysis on every
push, pull request and weekly on a schedule.
Dependabot opens automated pull requests for outdated pip, Docker and Actions
dependencies.
```

### 9.2 Jenkins vs GitHub Actions

| Criterion | Jenkins | GitHub Actions |
|---|---|---|
| Hosting model | Self-hosted (you own the server) | Managed by GitHub (also supports self-hosted runners) |
| Infrastructure cost | Server + maintenance | Free for public repositories; 2000 min/month for private |
| Setup effort | High — Java, plugins, credentials, Docker access | Near zero — commit a YAML file |
| Configuration language | Groovy (Jenkinsfile) | YAML |
| Extensibility | 1800+ plugins, unlimited customization | Marketplace of ~20,000 reusable actions |
| On-premise / air-gapped use | Excellent | Requires self-hosted runners |
| Native integration with the repository | Via plugins and webhooks | Built-in |
| Secret masking | Credentials plugin | Built-in, automatic |
| Best suited for | Regulated / on-premise / highly customized pipelines | Cloud-native and open-source projects |

```
Conclusion: Jenkins was chosen as the primary CI server because the syllabus
requires it and because self-hosting demonstrates deeper understanding of CI
infrastructure. GitHub Actions was configured as well to compare developer
experience and to provide a zero-cost pipeline that runs even when the Jenkins
server is unavailable.
```

```
[Insert Screenshot F1 — Actions tab]
Figure 9.1: GitHub Actions workflow runs
```

---

## 10. CLOUD DEPLOYMENT

### 10.1 Virtual Machine

```
Provider          : [Oracle Cloud Free Tier / AWS EC2 / VirtualBox]
Region            : [India West (Mumbai) / ap-south-1]
Instance shape    : [VM.Standard.E2.1.Micro / t2.micro]
Operating system  : Ubuntu Server 24.04 LTS
Public IP         : [xxx.xxx.xxx.xxx]
Access            : SSH with an RSA key pair (password authentication disabled)
```

### 10.2 Network and Firewall Configuration

| Layer | Rule | Purpose |
|---|---|---|
| Cloud Security List / Security Group | TCP 22 from admin IP | SSH administration |
| Cloud Security List / Security Group | TCP 5000 from 0.0.0.0/0 | Application access |
| Cloud Security List / Security Group | TCP 9090, 3000 | Prometheus and Grafana |
| Host firewall (UFW) | allow OpenSSH, 5000, 9090, 3000; default deny | Defence in depth |
| Container | `-p 5000:5000` bound to 0.0.0.0 | Reachable from outside the host |

### 10.3 Deployment Procedure

```
1.  SSH into the virtual machine
2.  Install Docker Engine and the Compose plugin
3.  Add the deployment user to the docker group
4.  Clone the repository
5.  Build the image:      docker build -t studentdesk:1.0.0 .
6.  Run the container with a named volume and a generated secret key:
      docker run -d --name studentdesk --restart unless-stopped \
        -p 5000:5000 -v studentdesk_data:/app/instance \
        -e SECRET_KEY="$(openssl rand -hex 32)" studentdesk:1.0.0
7.  Verify:               curl http://localhost:5000/health
8.  Open the firewall and access http://<PUBLIC_IP>:5000 from a browser
```

```
[Insert Screenshot G1 — Cloud console instance RUNNING]
Figure 10.1: Virtual machine running in the cloud console

[Insert Screenshot G2 — SSH session]
Figure 10.2: SSH session on the virtual machine

[Insert Screenshot G4 — Live URL in browser]
Figure 10.3: Application accessible over the public internet
```

---

## 11. CONFIGURATION MANAGEMENT WITH ANSIBLE

### 11.1 Inventory

```
[Paste ansible/inventory/hosts.ini here]
```

### 11.2 Playbooks

| Playbook | Purpose | Key modules used |
|---|---|---|
| `provision.yml` | Prepare a bare Ubuntu VM: package updates, Python, Git, Docker Engine, Compose plugin, docker group membership, application directories, UFW firewall rules | `apt`, `apt_repository`, `get_url`, `systemd`, `user`, `file`, `ufw`, `command` |
| `deploy.yml` | Pull code from Git, build the image, replace the running container, wait for the port, verify `/health`, print a deployment summary | `git`, `docker_image`, `docker_container`, `wait_for`, `uri`, `debug` |
| `monitoring.yml` | Install Node Exporter, Prometheus and Grafana as containers, copy configuration files, rewrite scrape targets for the VM network | `copy`, `replace`, `docker_container`, `debug`, handlers |
| `rollback.yml` | Revert to a previous image tag with health verification | `docker_image_info`, `docker_container`, `uri`, `fail` |
| `site.yml` | Master playbook importing the three above in order, taggable per stage | `import_playbook` |

### 11.3 Idempotency Demonstration

```
First execution:
    PLAY RECAP
    studentdesk-vm : ok=14  changed=8  unreachable=0  failed=0

Second execution (no changes made in between):
    PLAY RECAP
    studentdesk-vm : ok=14  changed=0  unreachable=0  failed=0

Ansible inspects the current state before acting. Packages that are already
installed, services already running and directories already present are
reported as "ok" rather than "changed". The playbook can therefore be re-run
at any time — after a partial failure, after a reboot, or as a drift-correction
mechanism — without breaking the server.
```

### 11.4 Safety Features

```
--check (dry run)          Predicts changes without applying them
--diff                     Shows line-level file differences
--syntax-check             Validates YAML before execution
ansible-lint               Enforces best practices
Handlers                   Restart services only when configuration changed
Serial ordering            SSH firewall rule is applied before UFW is enabled,
                           preventing administrator lockout
```

```
[Insert Screenshot H1 — ansible ping pong]
Figure 11.1: Connectivity test returning "pong"

[Insert Screenshot H2 — provision recap changed=8]
Figure 11.2: First provisioning run

[Insert Screenshot H3 — rerun changed=0]
Figure 11.3: Idempotency — re-running produces zero changes

[Insert Screenshot H4 — deploy summary]
Figure 11.4: Automated deployment summary
```

---

## 12. MONITORING AND LOG MANAGEMENT

### 12.1 Metrics Exposed by the Application

| Metric | Type | Labels | Meaning |
|---|---|---|---|
| `studentdesk_http_requests_total` | Counter | method, path, status | Total HTTP requests served |
| `studentdesk_http_request_duration_seconds` | Histogram | method, path | Request latency distribution |
| `studentdesk_students_total` | Gauge | — | Number of student records |
| `studentdesk_students_passed_total` | Gauge | — | Number of students with a passing grade |

Host metrics come from Node Exporter (CPU, memory, disk, filesystem, network).

### 12.2 Prometheus Configuration

```
[Paste monitoring/prometheus.yml here]

Scrape interval: 15 seconds
Targets: prometheus (self), studentdesk-app (/metrics), node-exporter
```

### 12.3 Example PromQL Queries

| Query | Interpretation |
|---|---|
| `up` | 1 = target reachable, 0 = target down |
| `rate(studentdesk_http_requests_total[1m])` | Requests per second over the last minute |
| `sum by (status) (rate(studentdesk_http_requests_total[5m]))` | Traffic split by HTTP status class |
| `histogram_quantile(0.95, rate(studentdesk_http_request_duration_seconds_bucket[5m]))` | 95th-percentile latency |
| `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` | CPU utilization percentage |
| `node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100` | Free memory percentage |

### 12.4 Alert Rules

| Alert | Condition | Severity |
|---|---|---|
| AppIsDown | `up{job="studentdesk-app"} == 0` for 1 min | critical |
| HighRequestLatency | p95 latency > 1 s for 2 min | warning |
| HighErrorRate | 5xx rate > 0.1 req/s for 2 min | critical |
| HostHighCPU | CPU > 85 % for 5 min | warning |
| HostOutOfMemory | Available memory < 15 % for 5 min | warning |
| HostDiskSpaceLow | Free disk < 15 % for 5 min | warning |

### 12.5 Logging Strategy

```
Following the twelve-factor methodology (Factor XI — Logs), the application
writes structured, timestamped records to standard output rather than to files:

    2026-09-19 14:32:11 | INFO  | app | GET /health -> 200
    2026-09-19 14:32:15 | INFO  | app | POST /login -> 302

Gunicorn access and error logs are likewise directed to stdout/stderr
(--access-logfile -  --error-logfile -). The container runtime captures these
streams, which means:

  • `docker logs -f studentdesk` gives a live tail
  • logs survive container restarts but not container removal unless the log
    driver writes them out
  • log rotation is configured at runtime (max-size 10m, max-file 3) so disk
    space is bounded
  • the same stream can be shipped to Loki, Fluentd or the ELK stack without
    changing application code
```

```
[Insert Screenshot I1 — /metrics output]
Figure 12.1: Prometheus metrics exposed by the application

[Insert Screenshot I2 — Prometheus targets]
Figure 12.2: All scrape targets reporting UP

[Insert Screenshot I5 — Grafana dashboard]
Figure 12.3: Grafana dashboard with live application and host metrics

[Insert Screenshot I6 — Alert firing]
Figure 12.4: AppIsDown alert firing after stopping the container
```

---

## 13. RESULTS AND OBSERVATIONS

```
[Fill in with your actual numbers]

Metric                                        Value
------------------------------------------------------------------
Lines of application code (Python)            ______
Number of automated tests                     35
Test execution time                           ______ s
Test pass rate                                100 %
Docker image size                             ______ MB
Cold Docker build time                        ______ s
Warm (cached) Docker build time               ______ s
Jenkins pipeline duration (full)              ______ min
Jenkins pipeline duration (tests only)        ______ s
Manual deployment time (before Ansible)       ______ min
Automated deployment time (with Ansible)      ______ min
Time to provision a fresh server (Ansible)    ______ min
Ansible re-run changes (idempotency)          0
Application availability during the demo      ______ %
Average request latency (p95)                 ______ ms
Alert detection time (app down → alert)       ______ s
```

**Key observations:**

```
1.  The complete feedback loop — from `git push` to a verified live deployment
    — takes approximately ____ minutes with zero manual steps.
2.  A deliberately introduced defect was detected at the unit-test stage in
    ____ seconds and prevented the faulty build from being containerized or
    deployed, validating the quality gate.
3.  Docker layer caching reduced repeat build time by approximately ____ %.
4.  Ansible reduced server preparation from a ____-minute manual procedure to
    a single reproducible command, and re-running it produced no changes.
5.  Prometheus detected a simulated outage and raised an alert within ____
    seconds, confirming that monitoring provides real operational value.
```

---

## 14. CHALLENGES FACED AND SOLUTIONS

```
[Use the table from docs/GUIDE_HINGLISH.md §11.3, and add 2-3 of your OWN
 real problems — the ones you actually hit. Authentic challenges impress
 examiners far more than textbook ones.]

1.  Challenge: ______________________________________________
    Root cause: _____________________________________________
    Solution: _______________________________________________
    Learning: _______________________________________________

2.  Challenge: Jenkins could not execute Docker commands from inside its own
    container.
    Root cause: The Jenkins container had no Docker CLI and no access to the
    host engine.
    Solution: Bind-mounted /var/run/docker.sock into the container and
    installed the docker.io package inside the Jenkins image.
    Learning: Container-to-Docker access must be granted explicitly; this
    pattern (socket mounting) is convenient but carries security implications
    that must be understood.

3.  Challenge: pytest crashed with "Duplicated timeseries in CollectorRegistry".
    Root cause: Prometheus metric objects were being created inside the
    application factory, so every test that built a new app tried to register
    the same metric names in the process-global registry.
    Solution: Moved metric definitions to module level so they are registered
    exactly once per process.
    Learning: Some libraries hold process-global state; test isolation at the
    database level is not enough if other globals exist.

4.  Challenge: ______________________________________________
...
```

---

## 15. CONCLUSION AND FUTURE SCOPE

### 15.1 Conclusion

```
This project successfully designed, implemented and demonstrated a complete
end-to-end DevOps pipeline around a functional web application. Every stage of
the flow — Developer → Git Repository → Jenkins → Build & Test → Docker Image →
Deployment → Monitoring — was realized with real, working tooling rather than
simulation.

The objectives set out in Section 1.2 were met:
  • A working Student Management System with validation, search, a REST API
    and 35 automated tests.
  • Source control with branching, pull requests and branch protection.
  • A nine-stage declarative Jenkins pipeline that fails safe.
  • A containerized, registry-published, health-checked application image.
  • Deployment to a cloud virtual machine.
  • Idempotent configuration management and deployment with Ansible, including
    a rollback playbook.
  • Live monitoring with Prometheus and Grafana plus six alert rules.

The most significant outcome is cultural as much as technical: the pipeline
proves that quality can be enforced automatically. A broken commit never
reaches production, a good commit reaches users within minutes, and the state
of the system is visible at all times on a dashboard.
```

### 15.2 Future Scope

```
Short term
  • Replace SQLite with PostgreSQL for concurrent write support
  • Add container image vulnerability scanning (Trivy / Snyk) to the pipeline
  • Add code quality analysis with SonarQube
  • Implement JWT authentication with role-based access control
  • Add CSRF protection and rate limiting

Medium term
  • Provision the infrastructure itself with Terraform (Infrastructure as Code
    for the cloud layer, complementing Ansible for the OS layer)
  • Centralize logs with Loki + Promtail or the ELK stack
  • Configure Alertmanager to deliver alerts to e-mail and Slack
  • Add end-to-end browser tests with Selenium or Playwright

Long term
  • Migrate from a single VM to Kubernetes for self-healing, horizontal
    autoscaling and rolling updates
  • Implement blue-green or canary deployment strategies
  • Adopt GitOps with ArgoCD so that the cluster state is reconciled from Git
  • Introduce distributed tracing with OpenTelemetry and Jaeger
```

---

## 16. REFERENCES

```
[1]  Git Documentation, https://git-scm.com/doc
[2]  GitHub Actions Documentation, https://docs.github.com/en/actions
[3]  Jenkins User Handbook, https://www.jenkins.io/doc/book/
[4]  Jenkins Pipeline Syntax, https://www.jenkins.io/doc/book/pipeline/syntax/
[5]  Docker Documentation, https://docs.docker.com/
[6]  Dockerfile Best Practices, https://docs.docker.com/build/building/best-practices/
[7]  Docker Compose Specification, https://docs.docker.com/compose/compose-file/
[8]  Ansible Documentation, https://docs.ansible.com/ansible/latest/
[9]  Flask Documentation, https://flask.palletsprojects.com/
[10] pytest Documentation, https://docs.pytest.org/
[11] Prometheus Documentation, https://prometheus.io/docs/introduction/overview/
[12] PromQL Querying Basics, https://prometheus.io/docs/prometheus/latest/querying/basics/
[13] Grafana Documentation, https://grafana.com/docs/grafana/latest/
[14] The Twelve-Factor App, https://12factor.net/
[15] Gunicorn Documentation, https://docs.gunicorn.org/
[16] Oracle Cloud Free Tier, https://www.oracle.com/cloud/free/
[17] AWS Free Tier, https://aws.amazon.com/free/
[18] Kim, G., Humble, J., Debois, P., Willis, J., "The DevOps Handbook",
     IT Revolution Press, 2016.
[19] Forsgren, N., Humble, J., Kim, G., "Accelerate: The Science of Lean
     Software and DevOps", IT Revolution Press, 2018.
```

---

## 📎 APPENDIX A — Complete File Listing

```
[Run this on your project and paste the output]

find . -type f -not -path './venv/*' -not -path './.git/*' \
       -not -path './instance/*' -not -name '*.pyc' | sort
```

## 📎 APPENDIX B — Command Cheat Sheet Used

```
[Run this and paste]

history | grep -E "git|docker|ansible|pytest|curl" | sort -u
```

## 📎 APPENDIX C — GitHub Repository Link

```
https://github.com/[YOUR_USERNAME]/studentdesk
```

---

### ✍️ Report writing tips

- **Length:** 20-25 pages is ideal. Kam nahi, bahut zyada bhi nahi.
- **Font:** Times New Roman 12pt (body), 1.5 line spacing, 1" margins
- **Code blocks:** Courier New / Consolas 9-10pt, light grey background
- **Figures:** har screenshot ke neeche "Figure X.Y: description" likho
- **Tables:** har table ke upar "Table X.Y: description"
- **Page numbers:** bottom center
- **Plagiarism:** AI se likhwa ke directly mat daalo — apne words me paraphrase karo. Professor pakad lete hain.
- **Proofread:** Grammarly free version se ek baar check kar lo.
- **PDF:** hamesha PDF submit karo, Word file nahi (formatting shift ho jati hai)
- **File name:** `TAE-II_RollNo_Name_StudentDesk.pdf`
