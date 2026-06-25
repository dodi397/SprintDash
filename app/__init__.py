from pathlib import Path
from flask import Flask
from config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # pastikan folder instance ada
    instance_dir = Path(app.root_path).parent / "instance"
    instance_dir.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    from .routes.main import bp as main_bp
    from .routes.race import bp as race_bp
    from .routes.api import bp as api_bp
    from .routes.history import bp as history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(race_bp, url_prefix="/race")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/history")

    with app.app_context():
        from .models.history import HistoryEntry
        db.create_all()

    return app