from .constants import MIN_TARGET, MAX_TARGET

def validate_target_meter(value):
    try:
        target = float(value)
    except (TypeError, ValueError):
        return False, "Target harus berupa angka."

    if target < MIN_TARGET:
        return False, f"Target minimal {MIN_TARGET} m."
    if target > MAX_TARGET:
        return False, f"Target maksimal {MAX_TARGET:,.0f} m."
    return True, target

def validate_lat_lon(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return False, "Koordinat tidak valid."

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return False, "Latitude/longitude di luar range."
    return True, (lat, lon)
