# 🤖 ANSIBLE SETUP — Complete Guide

> Beginner detail: [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) §9

---

## 1. Install

```bash
pip3 install ansible                       # ya: sudo apt install ansible
ansible --version

cd studentdesk/ansible
ansible-galaxy collection install -r requirements.yml
# installs: community.docker, community.general, ansible.posix
```

> ⚠️ **Windows:** Ansible natively nahi chalta. **WSL2** install karo (`wsl --install -d Ubuntu`), ya VM ke andar se chalao.

---

## 2. Inventory

`ansible/inventory/hosts.ini`:
```ini
[webservers]
studentdesk-vm ansible_host=140.245.12.34 ansible_user=ubuntu

[monitoring]
studentdesk-vm

[all:vars]
ansible_ssh_private_key_file=~/.ssh/oracle-studentdesk.pem
ansible_python_interpreter=/usr/bin/python3
```

**Default user by image:** Ubuntu → `ubuntu` · Oracle Linux → `opc` · Amazon Linux → `ec2-user` · Debian → `admin`

**Local practice (VM ke bina):** `ansible/inventory/localhost.ini`

---

## 3. Connection Test

```bash
cd studentdesk/ansible
ansible all -i inventory/hosts.ini -m ping
```

Success:
```json
studentdesk-vm | SUCCESS => { "changed": false, "ping": "pong" }
```

Failure:
```
studentdesk-vm | UNREACHABLE! => { "msg": "... Connection timed out" }
```
→ IP check · key path check · `chmod 600 key.pem` · security group port 22

**Aur ad-hoc commands:**
```bash
ansible all -i inventory/hosts.ini -m setup -a "filter=ansible_distribution*"
ansible all -i inventory/hosts.ini -m shell -a "df -h && free -h"
ansible webservers -i inventory/hosts.ini -m command -a "docker --version" --become
ansible all -i inventory/hosts.ini -m reboot --become
```

---

## 4. Playbooks

| File | Kaam | Run |
|---|---|---|
| `playbooks/provision.yml` | Docker, Python, firewall, folders | `ansible-playbook playbooks/provision.yml -i inventory/hosts.ini` |
| `playbooks/deploy.yml` | Git pull → image build → container run → health check | `ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini` |
| `playbooks/monitoring.yml` | Prometheus + Grafana + Node Exporter | `ansible-playbook playbooks/monitoring.yml -i inventory/hosts.ini` |
| `playbooks/rollback.yml` | Purane version pe wapas | `ansible-playbook playbooks/rollback.yml -e "rollback_tag=1.0.0"` |
| `site.yml` | Sab kuch order me | `ansible-playbook site.yml -i inventory/hosts.ini` |

**Env vars se override:**
```bash
GIT_REPO=https://github.com/YOUR_USERNAME/studentdesk.git \
IMAGE_TAG=1.0.0 \
APP_SECRET_KEY="$(openssl rand -hex 32)" \
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini
```

**Tags:**
```bash
ansible-playbook site.yml --tags deploy
ansible-playbook site.yml --skip-tags slow
ansible-playbook site.yml --list-tags
```

---

## 5. Idempotency Proof (report ke liye zaroori)

```bash
# Pehli baar
ansible-playbook playbooks/provision.yml -i inventory/hosts.ini
# PLAY RECAP: ok=14  changed=8  unreachable=0  failed=0

# Bilkul wahi dobara
ansible-playbook playbooks/provision.yml -i inventory/hosts.ini
# PLAY RECAP: ok=14  changed=0  unreachable=0  failed=0   ← ⭐
```

**`changed=0` = idempotent.** Screenshot lo!

**PLAY RECAP colors:** 🟢 green `ok` = already sahi tha · 🟡 yellow `changed` = Ansible ne kuch kiya · 🔴 `failed` = error · ⚫ `unreachable` = SSH fail

---

## 6. Safety Flags

```bash
--check            # dry run — kya badlega, actually nahi karega
--diff             # file changes line-by-line
--syntax-check     # YAML validate
-v / -vv / -vvv    # verbosity
--limit <host>     # sirf ek host
--start-at-task "Task name"   # beech se resume
--step             # har task pe confirm maangega
```

```bash
ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini --check --diff
ansible-lint playbooks/
```

---

## 7. Jinja2 Variables & Conditionals (playbook me)

```yaml
- name: Environment ke hisaab se port set karo
  ansible.builtin.debug:
    msg: "{{ 'Production port 443' if env == 'prod' else 'Dev port 5000' }}"

- name: Sirf Ubuntu pe chale
  ansible.builtin.apt:
    name: nginx
  when: ansible_distribution == "Ubuntu"

- name: Har course pe loop
  ansible.builtin.debug:
    msg: "Course: {{ item }}"
  loop: ["B.Tech CSE", "MCA", "MBA"]

- name: File se variable padho
  ansible.builtin.include_vars: secrets.yml
```

---

## 8. Vault — Secrets encrypt karna (bonus)

```bash
# Naya secret file banao
ansible-vault create secrets.yml
# password set karo, editor khulega:
#   app_secret_key: "mysupersecret"
#   grafana_password: "grafana123"

# Dekhna
ansible-vault view secrets.yml

# Edit
ansible-vault edit secrets.yml

# Encrypt existing file
ansible-vault encrypt myfile.yml

# Playbook me use
ansible-playbook deploy.yml --ask-vault-pass
# ya: --vault-password-file ~/.vault_pass
```

`secrets.yml` `.gitignore` me hai → commit nahi hoga ✅

---

## 9. Roles — Reusable Structure (bonus)

Bade projects me playbooks ko **roles** me todo:

```bash
cd studentdesk/ansible
ansible-galaxy init roles/docker
```

```
roles/docker/
├── tasks/main.yml        # kya karna hai
├── handlers/main.yml     # restart triggers
├── templates/            # Jinja2 config files
├── files/                # static files
├── vars/main.yml         # variables
├── defaults/main.yml     # default (override ho sakte hain)
└── meta/main.yml         # dependencies
```

Playbook me:
```yaml
- hosts: webservers
  become: true
  roles:
    - docker
    - studentdesk-app
    - monitoring
```

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `UNREACHABLE! Connection timed out` | IP galat / VM band / security group me port 22 block |
| `Permission denied (publickey)` | `ansible_ssh_private_key_file` path sahi? `chmod 600`? username sahi? |
| `sudo: a password is required` | `--ask-become-pass` add karo |
| `No module named 'ansible'` | `pip3 install ansible`; venv activate hai? |
| `couldn't resolve module/action: community.docker.*` | `ansible-galaxy collection install community.docker` |
| `community.general.ufw` fail | `ansible-galaxy collection install community.general` |
| YAML `ScannerError` | **TAB nahi, spaces!** Colon ke baad space. `ansible-lint` chalao |
| `found a tab character` | Indentation spaces se karo |
| Har baar `changed` aata hai | `command`/`shell` ki jagah proper module; ya `creates:`, `changed_when: false` add karo |
| `ansible_python_interpreter` error | Inventory me `/usr/bin/python3` set karo |
| Playbook slow hai | `ansible.cfg` me `forks = 10`; `pipelining = True`; `gather_facts: false` jahan zaroorat na ho |
| Target pe Python nahi | `ansible <host> -m raw -a "apt install -y python3"` |

**Debugging:**
```bash
ansible-playbook playbooks/deploy.yml -vvvv 2>&1 | tee ansible-debug.log
ansible all -i inventory/hosts.ini -m debug -a "msg={{ ansible_facts }}"
```
