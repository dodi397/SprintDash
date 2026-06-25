from app.services.distance_service import haversine_meters

def test_haversine_zero():
    assert haversine_meters(-6.2, 106.8, -6.2, 106.8) == 0

def test_haversine_positive():
    d = haversine_meters(-6.2, 106.8, -6.201, 106.801)
    assert d > 0
