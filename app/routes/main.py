from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    race_state = {
        "target_m": 201,
        "distance_m": 0,
        "distance_ft": 0,
        "time_seconds": 0,
        "current_speed": 0,
        "top_speed": 0,
        "status": "Ready",
        "gps_accuracy": "-",
        "lat": "-",
        "lon": "-"
    }

    return render_template(
        "index.html",
        page_title="SprintDash",
        race_state=race_state
    )