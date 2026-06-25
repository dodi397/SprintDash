from flask import Blueprint, jsonify, request
from ..services.race_service import race_service
from ..utils.validators import validate_target_meter, validate_lat_lon

bp = Blueprint("race", __name__)

@bp.post("/start")
def start():
    return jsonify({"ok": True, "state": race_service.start()})

@bp.post("/stop")
def stop():
    return jsonify({"ok": True, "state": race_service.stop()})

@bp.post("/reset")
def reset():
    return jsonify({"ok": True, "state": race_service.reset()})

@bp.post("/target")
def target():
    data = request.get_json(silent=True) or request.form
    ok, result = validate_target_meter(data.get("target_m"))
    if not ok:
        return jsonify({"ok": False, "message": result}), 400
    return jsonify({"ok": True, "state": race_service.set_target(result)})

@bp.post("/location")
def location():
    data = request.get_json(silent=True) or request.form
    ok, result = validate_lat_lon(data.get("lat"), data.get("lon"))
    if not ok:
        return jsonify({"ok": False, "message": result}), 400
    lat, lon = result
    accuracy = data.get("accuracy")
    return jsonify({"ok": True, "state": race_service.set_location(lat, lon, accuracy)})

@bp.post("/update")
def update():
    data = request.get_json(silent=True) or request.form
    ok, result = validate_lat_lon(data.get("lat"), data.get("lon"))
    if not ok:
        return jsonify({"ok": False, "message": result}), 400
    lat, lon = result
    accuracy = data.get("accuracy")
    state = race_service.update_position(lat, lon, accuracy)
    return jsonify({"ok": True, "state": state})
