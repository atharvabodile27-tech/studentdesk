# 🏗️ JENKINS SETUP — Complete Guide

> Beginner-level detail: [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) §6
> Ye file = quick reference + advanced troubleshooting

---

## 1. Install

### Option A — Docker (recommended, 5 min)

```bash
cd studentdesk/jenkins
docker compose up -d
docker logs -f jenkins            # wait for "Jenkins is fully up and running"
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

👉 http://localhost:8080

`jenkins/docker-compose.yml` me ye important lines hain:
```yaml
user: root                                              # docker.sock access ke liye
volumes:
  - jenkins_home:/var/jenkins_home                      # data persist
  - /var/run/docker.sock:/var/run/docker.sock           # host Docker engine
  - /usr/bin/docker:/usr/bin/docker                     # docker CLI
```

### Option B — Ubuntu VM pe direct

```bash
sudo apt update && sudo apt install -y openjdk-17-jdk curl
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
  sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update && sudo apt install -y jenkins
sudo systemctl enable --now jenkins
sudo ufw allow 8080/tcp && sudo ufw allow OpenSSH
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

👉 http://VM_IP:8080

---

## 2. Setup Wizard

1. Initial admin password paste → Continue
2. **Install suggested plugins** (3-5 min wait)
3. Admin user banao (username, strong password, naam, email)
4. Instance URL confirm → Save and Finish
5. **Start using Jenkins**

---

## 3. Plugins

**Manage Jenkins → Plugins → Available plugins:**

| Plugin | Zaroori? | Kaam |
|---|---|---|
| Pipeline | ✅ (suggested me aata hai) | Jenkinsfile |
| Git | ✅ (suggested) | Code checkout |
| **Docker** | ✅ | Docker commands |
| **Docker Pipeline** | ✅ | `docker.build()` etc. |
| **JUnit** | ✅ | Test reports |
| **Credentials Binding** | ✅ | Secrets |
| **Workspace Cleanup** | ✅ | `cleanWs()` |
| **Timestamper** | ✅ | Console me time |
| **SSH Agent** | ✅ (remote deploy ke liye) | SSH key injection |
| **GitHub Integration** | ✅ | Webhook trigger |
| Blue Ocean | ⚪ optional | Pretty UI |
| Email Extension | ⚪ optional | Failure emails |
| Build Timeout | ⚪ optional | Stuck builds |

Install → ✅ **Restart Jenkins when installation is complete**

---

## 4. Global Tools

**Manage Jenkins → Tools:**
- **Git:** auto-detect (path `/usr/bin/git`)
- **JDK:** Name `jdk17`, auto-detect
- **Docker:** path `/usr/bin/docker`
- Save

**Docker access verify:**
```bash
docker exec jenkins docker --version
# agar "not found":
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y docker.io curl python3 python3-venv python3-pip"
docker restart jenkins
```

> ⚠️ Jenkins ke official image me Python/curl nahi hota — pipeline me `python3` chahiye to upar wala command chalao.

---

## 5. Credentials

**Manage Jenkins → Credentials → System → Global credentials → Add Credentials**

### Docker Hub
| Field | Value |
|---|---|
| Kind | Username with password |
| Username | Docker Hub username |
| Password | Docker Hub password **ya Access Token** |
| **ID** | `dockerhub-creds` ← exact! |

### VM SSH (remote deploy)
| Field | Value |
|---|---|
| Kind | SSH Username with private key |
| Username | `ubuntu` |
| Private Key | Enter directly → `.pem` content paste |
| **ID** | `vm-ssh-key` |

### GitHub (private repo)
| Field | Value |
|---|---|
| Kind | Username with password |
| Username | GitHub username |
| Password | Personal Access Token (`repo` scope) |
| **ID** | `github-token` |

---

## 6. Pipeline Job

**New Item →** name `studentdesk-pipeline` → **Pipeline** → OK

| Setting | Value |
|---|---|
| Description | StudentDesk CI/CD |
| GitHub project | `https://github.com/YOUR_USERNAME/studentdesk/` |
| **Definition** | **Pipeline script from SCM** |
| SCM | Git |
| Repository URL | `https://github.com/YOUR_USERNAME/studentdesk.git` |
| Credentials | none (public) / github-token (private) |
| Branch Specifier | `*/main` |
| **Script Path** | `Jenkinsfile` |
| Lightweight checkout | ✅ tick |
| **Build Triggers** | ✅ GitHub hook trigger for GITScm polling |

Save → **Build Now**

---

## 7. Pipeline Stages (hamara Jenkinsfile)

```
1. Checkout           git clone + commit info print
2. Setup Python Env   venv + pip install
3. Build              python -m compileall (syntax check)
4. Unit Tests         pytest test_unit.py → JUnit XML
5. App & API Tests    pytest test_app.py test_api.py → JUnit XML
6. Docker Build       docker build -t studentdesk:${BUILD_NUMBER}-${GIT_SHA}
7. Smoke Test         container run + poll /health 10x
8. Docker Push        when { branch 'main' } → Docker Hub
9. Deploy             when { branch 'main' } → docker run + health verify

post:
  success → echo ✅
  failure → echo ❌
  always  → archiveArtifacts reports/*.xml + cleanWs()
```

**Environment block:**
```groovy
DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
APP_NAME              = 'studentdesk'
IMAGE_TAG             = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(7)}"
```

---

## 8. Webhook (auto-trigger)

**GitHub repo → Settings → Webhooks → Add webhook**

| Field | Value |
|---|---|
| Payload URL | `http://<JENKINS_PUBLIC_URL>/github-webhook/` |
| Content type | `application/json` |
| Secret | (khali) |
| Events | ✅ Just the push event |
| Active | ✅ |

⚠️ **`localhost` chalega nahi!** GitHub ka server tumhare laptop tak nahi pahunch sakta.

**Solutions:**
1. Jenkins ko **VM pe** install karo (public IP) ← best
2. **ngrok:** `ngrok http 8080` → `https://xxxx.ngrok-free.app/github-webhook/`
3. **Poll SCM:** `H/2 * * * *` (har 2 min check)

**Verify:** Webhooks list → Recent Deliveries → **200 OK** green

---

## 9. Results dekhna

| Kahan | Kya |
|---|---|
| Job page → **Stage View** | Green/red boxes with timing |
| Job page → **Pipeline Steps** | Step-by-step tree |
| Build → **Console Output** | Raw logs |
| Job page → **Test Result** | JUnit summary + failures |
| Job page → **Build History** | Sab builds, trend graph |
| **Blue Ocean** (`/blue`) | Modern visual pipeline |

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `docker: command not found` | `docker exec -u root jenkins apt install -y docker.io` → restart |
| `python3: not found` | `docker exec -u root jenkins apt install -y python3 python3-venv python3-pip` → restart |
| `curl: not found` | `docker exec -u root jenkins apt install -y curl` → restart |
| Permission denied on docker.sock | compose me `user: root`, ya `chmod 666 /var/run/docker.sock` |
| `credentials('dockerhub-creds')` not found | Credential ID **exactly** wahi hona chahiye |
| Build stuck at "Waiting for next available executor" | Manage Jenkins → Nodes → built-in node **Online** karo |
| `junit` / `cleanWs` undefined | JUnit / Workspace Cleanup plugin install karo |
| Webhook 404 | GitHub Integration plugin install karo; URL me trailing `/github-webhook/` zaroori |
| Jenkins bahut slow | `JAVA_OPTS=-Xmx2048m`; VM RAM badhao; purane builds delete karo |
| Disk full | Manage Jenkins → System → workspace cleanup; `docker system prune -af` |
| Port 8080 conflict | compose me `"8081:8080"` karo |

**Jenkins ke andar shell access (debugging ke liye):**
```bash
docker exec -it -u root jenkins bash
whoami; java -version; docker --version; python3 --version
ls /var/jenkins_home/workspace/
```

**Reset (sab kuch fresh):**
```bash
docker compose down -v       # volume bhi delete
docker compose up -d
```

---

## 11. Advanced (bonus marks)

### Parallel stages
```groovy
stage('Quality Checks') {
    parallel {
        stage('Unit Tests')  { steps { sh 'pytest tests/test_unit.py' } }
        stage('Lint')        { steps { sh 'flake8 app/' } }
        stage('Security')    { steps { sh 'bandit -r app/' } }
    }
}
```

### Input approval (manual gate before production)
```groovy
stage('Approve Production Deploy') {
    steps {
        timeout(time: 30, unit: 'MINUTES') {
            input message: 'Production pe deploy karein?', ok: 'Haan, deploy karo'
        }
    }
}
```

### Parameterized build
```groovy
pipeline {
    agent any
    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'production'], description: 'Deploy target')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
        booleanParam(name: 'SKIP_TESTS', defaultValue: false)
    }
    stages {
        stage('Test') { when { expression { !params.SKIP_TESTS } } steps { sh 'pytest' } }
    }
}
```

### Ansible ko Jenkins se call karna
```groovy
stage('Deploy with Ansible') {
    steps {
        sh '''
          . venv/bin/activate
          pip install ansible
          cd ansible
          ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini
        '''
    }
}
```

### Docker agent (har build fresh container me)
```groovy
pipeline {
    agent {
        docker {
            image 'python:3.12-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages { ... }
}
```
