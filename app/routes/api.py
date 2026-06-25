from flask import Blueprint, jsonify
from ..services.race_service import race_service
from ..services.history_service import history_service

bp = Blueprint("api", __name__)

@bp.get("/state")
def state():
    return jsonify({"ok": True, "state": race_service.get_state()})

@bp.get("/history")
def history():
    return jsonify({"ok": True, "items": history_service.list_history()})

@bp.post("/history/clear")
def clear_history():
    history_service.clear()
    return jsonify({"ok": True, "items": []})
