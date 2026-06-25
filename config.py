from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

def _default_db_uri():
    # Kalau di Vercel, simpan sqlite ke /tmp
    if os.getenv("VERCEL") == "1":
        return "sqlite:////tmp/sprintdash.sqlite3"

    # Lokal / server biasa
    return f"sqlite:///{BASE_DIR / 'instance' / 'sprintdash.sqlite3'}"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _default_db_uri())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    JSON_SORT_KEYS = False