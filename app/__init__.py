"""
StudentDesk - Factory function.
Yahan Flask app create hota hai, DB init hota hai aur blueprints register hote hain.
"""
import logging
import os

from flask import Flask, request

from .config import BASE_DIR, Config
from .models import db


def _init_database(app):
    """Tables + seed data — multi-worker safe.

    gunicorn ke 2+ workers ek saath create_app() chalate hain. SQLite pe
    simultaneous CREATE TABLE / INSERT race condition karta hai
    ("table already exists" / "UNIQUE constraint failed").
    File lock (fcntl.flock) se ek waqt me sirf ek worker init karta hai,
    baaki workers line me wait karte hain.
    Windows pe fcntl nahi hota — wahan dev server/tests single-process
    hote hain, isliye bina lock ke seedha init kar dete hain.
    """

    def _do_init():
        db.create_all()
        from .seed import seed_if_empty
        seed_if_empty()

    lock_dir = os.path.join(BASE_DIR, "instance")
    os.makedirs(lock_dir, exist_ok=True)
    lock_path = os.path.join(lock_dir, ".init.lock")

    try:
        import fcntl
    except ImportError:
        _do_init()
        return

    with open(lock_path, "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            _do_init()
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ---- Database init ----
    db.init_app(app)

    # ---- Blueprints (routes) register ----
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # ---- DB tables + sample data (race-safe) ----
    with app.app_context():
        _init_database(app)

    # ---- Health check (Docker / Monitoring ke liye zaroori) ----
    @app.route("/health")
    def health():
        return {"status": "ok", "app": "StudentDesk", "version": app.config.get("VERSION", "1.0.0")}, 200

    # ---- Prometheus metrics (/metrics) - optional dependency ----
    from .metrics import init_metrics
    init_metrics(app)

    # ---- Simple request logging (log management demo) ----
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

    @app.after_request
    def log_request(response):
        app.logger.info(
            "%s %s -> %s", request.method, request.path, response.status_code
        )
        return response

    return app