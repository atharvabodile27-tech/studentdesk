# ===================================================================
# StudentDesk Dockerfile  (multi-stage nahi, simple rakha hai beginner ke liye)
# Build:  docker build -t studentdesk:1.0.0 .
# Run:    docker run -p 5000:5000 studentdesk:1.0.0
# ===================================================================

# Python ka official slim image (chhota size = fast build & pull)
FROM python:3.12-slim

# Metadata labels - image ke baare me info (Jenkins/registry me dikhta hai)
LABEL maintainer="student@example.com"
LABEL app="studentdesk"
LABEL version="1.0.0"

# Container ke andar working directory
WORKDIR /app

# Pehle sirf requirements copy karo -> Docker layer caching ka fayda.
# Code change karne par dependencies dobara install nahi honge.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ab baaki source code copy karo
COPY . .

# DB file ke liye folder (volume mount point)
RUN mkdir -p /app/instance && chmod -R 777 /app/instance

# Non-root user banana = security best practice
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Container ke andar app kis port pe chalega
EXPOSE 5000

# Docker healthcheck - container really alive hai ya nahi
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=4).status==200 else 1)"

# Environment defaults (docker run -e se override kar sakte ho)
ENV FLASK_APP=run.py \
    PORT=5000 \
    PYTHONUNBUFFERED=1

# Production me gunicorn use karo (Flask dev server nahi)
# 2 workers, 5000 port pe bind
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
