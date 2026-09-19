"""
Prometheus metrics - /metrics endpoint.

Ye OPTIONAL hai. Agar `prometheus_client` install nahi hai to app
bilkul normal chalegi (graceful fallback). Monitoring ke liye:

    pip install -r requirements-monitoring.txt

Metrics jo expose hote hain:
  - studentdesk_http_requests_total{method,path,status}
  - studentdesk_http_request_duration_seconds (histogram)
  - studentdesk_students_total
  - studentdesk_students_passed_total

NOTE: Metrics MODULE LEVEL pe define kiye gaye hain, kyunki Prometheus ka
      CollectorRegistry process-wide hota hai. Function ke andar banate to
      dusri baar app create karne par "Duplicated timeseries" error aata.
"""
import time

from flask import request, g

try:
    from prometheus_client import (
        Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST,
    )
    PROMETHEUS_AVAILABLE = True

    REQUEST_COUNT = Counter(
        "studentdesk_http_requests_total",
        "Total HTTP requests",
        ["method", "path", "status"],
    )
    REQUEST_LATENCY = Histogram(
        "studentdesk_http_request_duration_seconds",
        "HTTP request latency in seconds",
        ["method", "path"],
    )
    STUDENTS_TOTAL = Gauge(
        "studentdesk_students_total",
        "Number of students in the database",
    )
    STUDENTS_PASSED = Gauge(
        "studentdesk_students_passed_total",
        "Number of students who passed",
    )
except ImportError:
    PROMETHEUS_AVAILABLE = False


def init_metrics(app):
    """Flask app factory se call hota hai."""

    if not PROMETHEUS_AVAILABLE:
        app.logger.info("prometheus_client install nahi hai - /metrics fallback mode me hai.")

        @app.route("/metrics", endpoint="metrics_disabled")
        def metrics_disabled():
            return (
                "# prometheus_client install nahi hai.\n"
                "# Install karo:  pip install -r requirements-monitoring.txt\n"
                "# Phir app restart karo.\n"
            ), 501, {"Content-Type": "text/plain"}

        return app

    @app.before_request
    def start_timer():
        g.request_started_at = time.perf_counter()

    @app.after_request
    def record_metrics(response):
        path = request.path
        if path != "/metrics" and not path.startswith("/static"):
            REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
            if hasattr(g, "request_started_at"):
                REQUEST_LATENCY.labels(request.method, path).observe(
                    time.perf_counter() - g.request_started_at
                )
        return response

    @app.route("/metrics", endpoint="metrics_enabled")
    def metrics():
        # Live DB counts ko gauges me daalo
        try:
            from .models import Student
            students = Student.query.all()
            STUDENTS_TOTAL.set(len(students))
            STUDENTS_PASSED.set(sum(1 for s in students if s.result() == "PASS"))
        except Exception as exc:
            app.logger.warning("metrics gauge update failed: %s", exc)

        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    return app
