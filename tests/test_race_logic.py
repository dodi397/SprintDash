from app.services.race_service import race_service

def test_target_update():
    state = race_service.set_target(150)
    assert state["target_m"] == 150.0
