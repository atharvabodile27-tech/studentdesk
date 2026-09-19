"""
Configuration - sab kuch environment variable se aayega (12-factor app style).
Local pe default values chalengi, Docker/Cloud pe env vars set karenge.
"""
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "instance", "studentdesk.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VERSION = os.environ.get("APP_VERSION", "1.0.0")


class TestConfig(Config):
    """Tests ke liye - in-memory SQLite DB use hoti hai, real DB gandi nahi hoti."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
