# ===================================================================
# Makefile — ek word me bade commands
#   make setup / make run / make test / make docker / make up ...
# ===================================================================
.PHONY: help setup run test test-v report clean docker docker-run docker-stop \
        compose-up compose-down compose-monitoring push lint

APP_NAME    ?= studentdesk
IMAGE_TAG   ?= 1.0.0
PORT        ?= 5000
DOCKER_USER ?= yourusername

help: ## Ye help dikhao
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------- Local development ----------------
setup: ## Venv + dependencies + tests (first time)
	bash setup.sh

run: ## App chalao (dev server)
	@source venv/bin/activate && python run.py

test: ## Saare tests chalao
	@source venv/bin/activate && pytest -v

test-v: ## Sirf unit tests
	@source venv/bin/activate && pytest tests/test_unit.py -v

report: ## JUnit XML test report banao
	@source venv/bin/activate && mkdir -p reports && pytest -v --junitxml=reports/results.xml
	@echo "✅ Report: reports/results.xml"

lint: ## Code style check
	@source venv/bin/activate && python -m compileall -q app run.py && echo "✅ Syntax OK"

clean: ## Cache aur temp files hatao
	rm -rf .pytest_cache venv instance *.db reports htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean"

# ---------------- Docker ----------------
docker: ## Image build karo
	docker build -t $(APP_NAME):$(IMAGE_TAG) .

docker-run: ## Container chalao
	docker run -d --name $(APP_NAME) -p $(PORT):5000 \
	  -v $(APP_NAME)_data:/app/instance $(APP_NAME):$(IMAGE_TAG)
	@sleep 3 && curl -s http://localhost:$(PORT)/health && echo " ✅"

docker-stop: ## Container band karo + hatao
	docker rm -f $(APP_NAME) 2>/dev/null || true

docker-logs: ## Live logs
	docker logs -f $(APP_NAME)

compose-up: ## Sirf app (compose)
	docker compose up -d app

compose-monitoring: ## App + Prometheus + Grafana + Node Exporter
	docker compose --profile monitoring up -d

compose-down: ## Sab band karo
	docker compose down

push: ## Docker Hub pe push (DOCKER_USER set karo)
	docker tag $(APP_NAME):$(IMAGE_TAG) $(DOCKER_USER)/$(APP_NAME):$(IMAGE_TAG)
	docker push $(DOCKER_USER)/$(APP_NAME):$(IMAGE_TAG)

# ---------------- Ansible ----------------
ansible-ping: ## Connection test
	cd ansible && ansible all -i inventory/hosts.ini -m ping

ansible-provision: ## VM provision
	cd ansible && ansible-playbook playbooks/provision.yml -i inventory/hosts.ini

ansible-deploy: ## App deploy
	cd ansible && ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini

ansible-all: ## Pura setup (provision + deploy + monitoring)
	cd ansible && ansible-playbook site.yml -i inventory/hosts.ini

# ---------------- Jenkins ----------------
jenkins-up: ## Jenkins ko Docker me chalao
	cd jenkins && docker compose up -d
	@echo "🔑 Initial password:"
	@sleep 8 && docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || \
	  echo "  (thoda wait karo, phir: docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword)"
	@echo "👉 http://localhost:8080"

jenkins-down: ## Jenkins band karo
	cd jenkins && docker compose down
