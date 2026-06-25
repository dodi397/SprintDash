from flask import Blueprint, jsonify
from ..services.history_service import history_service

bp = Blueprint("history", __name__)

@bp.get("/")
def list_history():
    return jsonify({"ok": True, "items": history_service.list_history()})

@bp.post("/clear")
def clear():
    history_service.clear()
    return jsonify({"ok": True})
