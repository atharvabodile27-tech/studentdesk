"""
StudentDesk - Factory function.
Yahan Flask app create hota hai, DB init hota hai aur blueprints register hote hain.
"""
import os
from flask import Flask

from .config import Config
from .models import db


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

    # ---- DB tables + sample data ----
    with app.app_context():
        db.create_all()
        from .seed import seed_if_empty
        seed_if_empty()

    # ---- Health check (Docker / Monitoring ke liye zaroori) ----
    @app.route("/health")
    def health():
        return {"status": "ok", "app": "StudentDesk", "version": app.config.get("VERSION", "1.0.0")}, 200

    # ---- Prometheus metrics (/metrics) - optional dependency ----
    from .metrics import init_metrics
    init_metrics(app)

    # ---- Simple request logging (log management demo) ----
    import logging
    from flask import request as _req
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

    @app.after_request
    def log_request(response):
        app.logger.info(
            "%s %s -> %s", _req.method, _req.path, response.status_code
        )
        return response

    return app
