# 🛠️ TROUBLESHOOTING — Errors aur Fixes

> Sabse pehle: **error message poora padho.** Pehla error = root cause, baaki cascade hote hain.

---

## 🔍 Debugging ka systematic tarika

```
1. Error poora padho (last line nahi, pehla error)
2. Layer identify karo: App? Docker? Network? Jenkins? Ansible? Cloud?
3. Isolate karo — sabse chhote test se shuru:
     App chalti hai?        → python run.py ; curl localhost:5000/health
     Container chalta hai?  → docker run --rm -p 5000:5000 img ; docker logs
     VM ke andar?           → ssh ; curl localhost:5000/health
     Bahar se?              → curl VM_IP:5000/health
4. Logs dekho: docker logs, journalctl -u jenkins, Prometheus targets
5. EK cheez badlo, test karo
6. Solution note karo → report ke "Challenges" section me jayega
```

---

## 🐍 Python / App

| Error | Reason | Fix |
|---|---|---|
| `python: command not found` | PATH | `python3` use karo; Windows pe Python reinstall + "Add to PATH" |
| `ModuleNotFoundError: No module named 'flask'` | Venv activate nahi | `source venv/bin/activate` → `pip install -r requirements.txt` |
| `pip: command not found` | pip missing | `python3 -m pip install ...` / `sudo apt install python3-pip` |
| `error: externally-managed-environment` | System Python protected | **Venv use karo** (yahi sahi hai) |
| `Address already in use` / Port 5000 busy | Pehle se kuch chal raha | `lsof -i :5000` (Mac/Linux) · `netstat -ano \| findstr :5000` (Win) → kill PID. Ya `PORT=5001 python run.py` |
| `sqlalchemy.exc.OperationalError` | DB locked/corrupt | `rm instance/studentdesk.db` → app restart (fresh seed) |
| `TemplateNotFound: dashboard.html` | Galat folder se chala rahe ho | `cd studentdesk` karke `python run.py` |
| `jinja2.exceptions.UndefinedError` | Template me variable nahi bheja | `render_template(..., var=value)` check karo |
| App chalu hai par browser blank | Cache / galat port | Hard refresh `Ctrl+Shift+R`; URL me port confirm |
| Static CSS load nahi ho raha | `url_for` path galat | `{{ url_for('static', filename='css/style.css') }}` |

---

## 🔧 Git / GitHub

| Error | Reason | Fix |
|---|---|---|
| `fatal: not a git repository` | init nahi kiya | `git init` |
| `error: failed to push some refs` | Remote ahead | `git pull origin main --rebase` → `git push` |
| `Updates were rejected ... remote contains work` | GitHub pe README bana tha | `git pull origin main --allow-unrelated-histories` → resolve → push |
| `fatal: remote origin already exists` | Remote set hai | `git remote set-url origin <URL>` |
| `Authentication failed` / `403` | Token expire | Naya PAT banao; Windows Credential Manager se purana hatao |
| `Permission denied (publickey)` | SSH key nahi | HTTPS URL use karo, ya `ssh-keygen -t ed25519` + GitHub pe public key add |
| `Your branch is ahead of 'origin/main' by N commits` | Push nahi kiya | `git push` |
| `merge conflict` | Same lines changed | File kholo → `<<<<<<<` / `=======` / `>>>>>>>` markers → manually fix → `git add` → `git commit` |
| `detached HEAD` | Commit pe directly checkout | `git checkout main` (ya `git switch -c new-branch`) |
| `venv/` commit ho gaya | .gitignore baad me | `git rm -r --cached venv` → commit → push |
| Galat commit message | — | `git commit --amend -m "new message"` (push ke baad `--force-with-lease`) |
| Galat commit undo | — | `git reset --soft HEAD~1` (changes rakhe) / `git revert HEAD` (safe, naya commit) |

---

## 🐳 Docker

| Error | Reason | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker nahi chal raha | Docker Desktop kholo; Linux: `sudo systemctl start docker` |
| `permission denied ... /var/run/docker.sock` | User docker group me nahi | `sudo usermod -aG docker $USER` → **logout/login** (ya `newgrp docker`) |
| `port is already allocated` | Port conflict | `docker ps -a` → `docker rm -f <name>` · ya `-p 5001:5000` |
| `no matching manifest for linux/arm64` | Mac M-chip vs x86 image | `--platform linux/amd64` |
| `exec format error` | Architecture mismatch | Same `--platform` use karo build aur run me |
| Build bahut slow | Cache miss | `.dockerignore` check; `requirements.txt` pehle COPY |
| Container turant exit ho jata hai | App crash | `docker logs <c>` · `docker run --rm -it <img> sh` andar jhanko |
| `docker compose: command not found` | Purana Docker | `docker-compose` (hyphen) ya Docker Desktop update |
| `unable to prepare context: ... Dockerfile not found` | Galat directory | `cd studentdesk` (jahan Dockerfile hai) |
| Image 1GB+ | Full base image | `python:3.12-slim` + `.dockerignore` + multi-stage |
| `/health` unreachable from host | Port map nahi | `-p 5000:5000` confirm; `docker port <c>` |
| `unhealthy` status | Healthcheck fail | `docker inspect <c> \| grep -A10 Health` → log dekho |
| Disk full (`no space left on device`) | Purane images/containers | `docker system prune -af --volumes` ⚠️ volumes bhi delete honge |
| Data restart pe chala gaya | Volume nahi | `-v studentdesk_data:/app/instance` |

**Handy:**
```bash
docker system df                    # kitni disk use ho rahi
docker system prune -af             # unused images/containers hatao
docker stats                        # live CPU/RAM
docker inspect <c> | less           # full details
docker exec -it <c> sh              # andar shell
docker network ls && docker network inspect <net>
docker volume ls && docker volume inspect <vol>
```

---

## 🏗️ Jenkins

| Error | Reason | Fix |
|---|---|---|
| `localhost:8080` nahi khul raha | Jenkins start nahi | `docker ps` · `docker logs jenkins` · `sudo systemctl status jenkins` |
| `docker: command not found` in build | CLI missing | `docker exec -u root jenkins bash -c "apt update && apt install -y docker.io"` → `docker restart jenkins` |
| `python3: not found` | Python missing | `docker exec -u root jenkins apt install -y python3 python3-venv python3-pip` |
| `curl: not found` | curl missing | `docker exec -u root jenkins apt install -y curl` |
| Permission denied on docker.sock | Socket perms | compose me `user: root` |
| `credentials('dockerhub-creds')` fail | ID mismatch | Credential ID **exactly** `dockerhub-creds` |
| Build stuck "Waiting for next available executor" | Agent offline | Manage Jenkins → Nodes → built-in node Online |
| `junit` / `cleanWs` undefined | Plugin missing | JUnit / Workspace Cleanup install |
| `WorkflowScript: 7: invalid stage name` | Groovy syntax | Quotes/braces check; Jenkins Replay feature use karo |
| Webhook trigger nahi chalta | localhost URL | Public IP / ngrok / fallback `Poll SCM H/2 * * * *` |
| Webhook 404 | Plugin missing | **GitHub Integration** plugin install |
| Bahut slow | RAM kam | `JAVA_OPTS=-Xmx2048m`; purane builds delete; `docker system prune` |
| Disk full | Workspace accumulate | `cleanWs()` in post; Manage Jenkins → Disk Usage |

**Debug:**
```bash
docker exec -it -u root jenkins bash
ls /var/jenkins_home/workspace/
cat /var/jenkins_home/jobs/<job>/config.xml
sudo journalctl -u jenkins -f            # direct install
# Job page → "Replay" → Jenkinsfile edit karke turant retry (bina push kiye)
```

---

## 🤖 Ansible

| Error | Reason | Fix |
|---|---|---|
| `UNREACHABLE! Connection timed out` | IP/firewall/VM down | IP verify; security group port 22; VM running |
| `Permission denied (publickey)` | Key path/perms | `ansible_ssh_private_key_file` sahi; `chmod 600 key.pem`; username sahi |
| `sudo: a password is required` | become pass | `--ask-become-pass` |
| `No module named 'ansible'` | Install/venv | `pip3 install ansible` |
| `couldn't resolve module/action: community.docker.*` | Collection missing | `ansible-galaxy collection install community.docker community.general` |
| `yaml.scanner.ScannerError` | YAML syntax | **Spaces, TAB nahi**; colon ke baad space; `ansible-lint` |
| `found a tab character` | TAB indent | Editor me "Spaces: 2" set karo |
| `The field 'hosts' has an invalid value` | Inventory group name | Group brackets `[webservers]` check |
| Har baar `changed` | Non-idempotent task | Proper module use karo; `creates:` / `changed_when: false` |
| `ansible_python_interpreter` error | Python path | Inventory me `/usr/bin/python3` |
| Slow | Serial execution | `ansible.cfg` me `forks=10`, `pipelining=True` |
| Target pe Python nahi | Bare OS | `ansible <h> -m raw -a "apt install -y python3"` |
| Windows pe Ansible nahi chalta | Unsupported | **WSL2** use karo |

**Debug:**
```bash
ansible-playbook pb.yml -vvvv 2>&1 | tee debug.log
ansible-playbook pb.yml --check --diff
ansible-playbook pb.yml --syntax-check
ansible-playbook pb.yml --start-at-task "Task Name"
ansible-playbook pb.yml --step            # har task pe confirm
ansible all -i inv.ini -m setup -a "filter=ansible_*" | less
ansible-lint playbooks/
```

---

## ☁️ Cloud / Network

| Problem | Fix |
|---|---|
| `http://VM_IP:5000` bahar se nahi khulta | **Sabse common galti.** 4 layers check karo: (1) Cloud **Security Group / Ingress Rule** TCP 5000 from `0.0.0.0/0` (2) VM me `sudo ufw allow 5000/tcp` (3) **Oracle extra:** `sudo iptables -I INPUT 6 -p tcp --dport 5000 -j ACCEPT && sudo netfilter-persistent save` (4) `docker run -p 5000:5000` (0.0.0.0, 127.0.0.1 nahi) |
| SSH timeout | Security group port 22; IP sahi; VM running; `ssh -vvv` se debug |
| SSH disconnect baar-baar | `~/.ssh/config` me `ServerAliveInterval 60` |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED` | Purana host key | `ssh-keygen -R VM_IP` |
| VM ka IP change ho gaya | Static/public IP reserve karo |
| Oracle ne instance reclaim kar li | "Always Free" shape (E2.1.Micro / A1) use karo; instance ko Running rakho |
| HTTPS chahiye | DuckDNS free domain + `sudo certbot --nginx -d yourdomain.duckdns.org` |
| Render app sleep ho jati hai | Free tier behavior — pehli request pe 30-50s cold start. Normal hai. |

**Network debug:**
```bash
curl -v http://VM_IP:5000/health
nc -zv VM_IP 5000
sudo ss -tulpn | grep 5000
sudo iptables -L INPUT -n --line-numbers
sudo ufw status verbose
ping VM_IP
traceroute VM_IP
dig yourdomain.com
```

---

## 📊 Monitoring

| Problem | Fix |
|---|---|
| Prometheus target **DOWN** | Same network? Hostname sahi? App `/metrics` de rahi hai (`curl` karke dekho)? |
| Grafana "Data source not working" | URL: `http://prometheus:9090` (compose) / `http://localhost:9090` (VM) |
| Graphs khali | **Load generate karo!** Aur time range badhao (last 1h) |
| Node exporter data nahi | Container up? `curl localhost:9100/metrics` |
| Alert fire nahi ho raha | `for:` duration wait (1-5 min); Rules page pe state dekho |
| Prometheus disk full | `--storage.tsdb.retention.time=7d` |
| Metrics inconsistent (gunicorn multi-worker) | `PROMETHEUS_MULTIPROC_DIR` set karo, ya `--workers 1` |
| Port 9090/3000 busy | compose me remap: `"9091:9090"` |

```bash
promtool check config monitoring/prometheus.yml
curl -s localhost:9090/api/v1/targets | python3 -m json.tool | head -50
curl -s 'localhost:9090/api/v1/query?query=up' | python3 -m json.tool
docker compose logs prometheus | tail -50
```

---

## 🆘 Aakhri rasta — fresh start

```bash
# Sab containers/images hatao
docker compose down -v
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -q)
docker system prune -af --volumes

# Python fresh
rm -rf venv instance *.db
python3 -m venv venv && source venv/bin/activate

# Jenkins fresh
cd jenkins && docker compose down -v && docker compose up -d

# Git fresh (⚠️ local changes jayenge)
git fetch origin && git reset --hard origin/main && git clean -fd
```

---

## 📞 Help kahan se mile

| Resource | Link |
|---|---|
| Stack Overflow | https://stackoverflow.com |
| Jenkins community | https://community.jenkins.io |
| Docker community | https://forums.docker.com |
| Ansible forum | https://forum.ansible.com |
| r/devops | https://reddit.com/r/devops |
| Error message ko Google pe **exact quotes me** search karo | `"Duplicated timeseries in CollectorRegistry"` |

> 💡 **Pro tip:** Error ka **pehla unique line** copy karke quotes me Google karo. 95% baar kisi ne same problem face ki hai.
