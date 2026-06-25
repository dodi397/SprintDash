from app.services.speed_service import speed_service

def test_calculate_speed():
    assert speed_service.calculate_speed(100, 10) == 10
