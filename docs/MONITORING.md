# 📊 MONITORING & LOGS — Complete Guide

> Beginner detail: [`GUIDE_HINGLISH.md`](GUIDE_HINGLISH.md) §10

---

## 1. Architecture

```
   StudentDesk App (:5000)  ──/metrics──┐
                                        ↓
   Node Exporter (:9100) ──────→  PROMETHEUS (:9090)  ←── alerts.yml
                                        ↓ PromQL
                                   GRAFANA (:3000)
```

| Tool | Kaam | Port |
|---|---|---|
| Prometheus | Metrics scrape (pull, 15s), store, query, alert rules | 9090 |
| Node Exporter | Host CPU / RAM / disk / network | 9100 |
| Grafana | Dashboards, visualization | 3000 |
| App `/metrics` | Application + business metrics | 5000 |

---

## 2. Chalao

**Local (Docker Compose):**
```bash
cd studentdesk
docker compose --profile monitoring up -d
docker compose ps
docker compose logs -f prometheus
```

**VM pe (Ansible):**
```bash
cd studentdesk/ansible
ansible-playbook playbooks/monitoring.yml -i inventory/hosts.ini
```

> 💡 Ansible playbook automatically `app:5000` ko `localhost:5000` me rewrite kar deta hai,
> kyunki VM pe app container network ke bahar host pe chalti hai.

---

## 3. App Metrics

```bash
curl http://localhost:5000/metrics
```

| Metric | Type | Labels |
|---|---|---|
| `studentdesk_http_requests_total` | Counter | method, path, status |
| `studentdesk_http_request_duration_seconds` | Histogram | method, path |
| `studentdesk_students_total` | Gauge | — |
| `studentdesk_students_passed_total` | Gauge | — |

Plus standard: `python_gc_*`, `python_info`, `process_*`, `flask_*`

**Metric types (viva):**
- **Counter** — sirf badhta hai. `rate()` / `increase()` se use karo.
- **Gauge** — up/down dono. Direct value.
- **Histogram** — buckets → percentile. `histogram_quantile()`.
- **Summary** — client-side quantiles (aggregate nahi ho sakta).


---

## 4. Prometheus

👉 http://localhost:9090

**Status → Targets** — sab `UP` chahiye.

**Useful PromQL:**

| Query | Matlab |
|---|---|
| `up` | Kaun alive hai |
| `studentdesk_students_total` | DB me students |
| `rate(studentdesk_http_requests_total[1m])` | req/sec |
| `sum by (status) (rate(studentdesk_http_requests_total[5m]))` | Status-wise traffic |
| `histogram_quantile(0.95, rate(studentdesk_http_request_duration_seconds_bucket[5m]))` | p95 latency |
| `100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` | CPU % |
| `node_memory_MemAvailable_bytes / 1024 / 1024` | Free RAM (MB) |
| `(node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100` | Disk free % |
| `rate(node_network_receive_bytes_total[5m])` | Network RX |
| `count(container_last_seen)` | Kitne containers |

**Status → Rules** = 6 alert rules. **Status → Configuration** = loaded config.

---

## 5. Alert Rules (`monitoring/alerts.yml`)

| Alert | Condition | For | Severity |
|---|---|---|---|
| AppIsDown | `up{job="studentdesk-app"} == 0` | 1m | critical |
| HighRequestLatency | p95 > 1s | 2m | warning |
| HighErrorRate | 5xx rate > 0.1/s | 2m | critical |
| HostHighCPU | CPU > 85% | 5m | warning |
| HostOutOfMemory | Free RAM < 15% | 5m | warning |
| HostDiskSpaceLow | Free disk < 15% | 5m | warning |

**Alert test (demo ke liye):**
```bash
docker stop studentdesk
# wait 1-2 min → http://localhost:9090/alerts → AppIsDown FIRING 🔴
docker start studentdesk
# 1 min me RESOLVED 🟢
```

---

## 6. Grafana

👉 http://localhost:3000 · login `admin` / `admin123`

**Datasource** already provisioned hai (`monitoring/grafana/provisioning/datasources/prometheus.yml`) → `http://prometheus:9090`. Save & Test → green ✅

**Dashboard import:**
- Apna: Dashboards → New → Import → upload `monitoring/grafana/dashboards/studentdesk.json`
- Community: Import → ID **1860** (Node Exporter Full) → Load → Prometheus → Import

**Load generate karo (graphs me kuch dikhega tabhi):**
```bash
for i in $(seq 1 200); do curl -s http://localhost:5000/health > /dev/null; done

# continuous:
while true; do curl -s http://localhost:5000/api/students > /dev/null; sleep 0.3; done
```

**Alert notifications (Grafana side):**
Alerting → Notification channels → Add email / Slack → phir dashboard panel pe alert rule lagao.

---

## 7. Alertmanager (email/Slack alerts)

`monitoring/alertmanager.yml`:
```yaml
route:
  receiver: 'email-alerts'
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

receivers:
  - name: 'email-alerts'
    email_configs:
      - to: 'tumhari-email@example.com'
        from: 'alerts@example.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'tumhari-email@example.com'
        auth_password: 'GMAIL_APP_PASSWORD'
        require_tls: true
```

`docker-compose.yml` me add karo + `prometheus.yml` me `alerting:` block uncomment karo.

---

## 8. Logs

### Docker logs
```bash
docker logs studentdesk
docker logs -f studentdesk                    # live tail
docker logs --tail 100 studentdesk
docker logs --since 10m studentdesk
docker logs --since 2026-09-19T10:00:00 studentdesk
docker inspect --format='{{.LogPath}}' studentdesk
```

### App log format (structured)
```
2026-09-19 14:32:11,847 | INFO     | app | GET / -> 200
2026-09-19 14:32:15,203 | INFO     | app | POST /login -> 302
```

### Gunicorn access log
```
172.18.0.1 - - [19/Sep/2026:14:32:11 +0000] "GET /health HTTP/1.1" 200 68 "-" "curl/8.5.0"
```

### Log rotation
```bash
docker run -d --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 \
  --name studentdesk -p 5000:5000 studentdesk:1.0.0
```
Ansible `deploy.yml` me already configured ✅

Daemon-wide: `/etc/docker/daemon.json`
```json
{ "log-driver": "json-file", "log-opts": { "max-size": "10m", "max-file": "3" } }
```
`sudo systemctl restart docker`

---

## 9. Loki (centralized log aggregation — bonus)

`docker-compose.yml` me:
```yaml
  loki:
    image: grafana/loki:3.1.0
    ports: ["3100:3100"]
    profiles: ["monitoring"]

  promtail:
    image: grafana/promtail:3.1.0
    profiles: ["monitoring"]
    volumes:
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock
      - ./monitoring/promtail-config.yml:/etc/promtail/config.yml:ro
```

`monitoring/promtail-config.yml`:
```yaml
server:
  http_listen_port: 9080
positions:
  filename: /tmp/positions.yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
```

Grafana → Data sources → **Loki** → `http://loki:3100` → Explore me query:
```
{container="studentdesk-app"}
{container="studentdesk-app"} |= "ERROR"
{container="studentdesk-app"} | json | status="500"
```

---

## 10. Uptime Monitoring (external, free)

| Service | Free plan |
|---|---|
| UptimeRobot | 50 monitors, 5-min |
| Better Stack | 10 monitors |
| Healthchecks.io | 20 checks |

Setup: Add Monitor → HTTP(s) → `http://VM_IP:5000/health` → 5 min → Create.

---

## 11. Troubleshooting

| Problem | Fix |
|---|---|
| Prometheus target **DOWN** | Same Docker network? Target hostname sahi (`app:5000` compose me, `localhost:5000` VM pe)? App `/metrics` de rahi hai? |
| Grafana "Data source not working" | URL `http://prometheus:9090` (compose) ya `http://localhost:9090` (VM pe alag install) |
| Graphs khali hain | Load generate karo! Prometheus me 15-30s data chahiye. Time range badhao (last 1 hour) |
| Node exporter metrics nahi | Container chal raha hai? `curl localhost:9100/metrics` |
| Alert fire nahi ho raha | `for:` duration wait karo (1-5 min). Prometheus → Status → Rules → state dekho |
| Prometheus disk bhar raha | `--storage.tsdb.retention.time=7d` command me add karo |
| Port 9090/3000 conflict | compose me port badlo (`9091:9090`) |
| Multiple gunicorn workers se metrics inconsistent | `PROMETHEUS_MULTIPROC_DIR` set karo, ya `--workers 1` (demo ke liye theek) |

**Debug:**
```bash
docker compose ps
docker compose logs prometheus | tail -50
curl http://localhost:9090/-/healthy
curl http://localhost:9090/api/v1/targets | python3 -m json.tool | head -40
promtool check config monitoring/prometheus.yml
```
