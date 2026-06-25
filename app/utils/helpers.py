from datetime import datetime
from math import hypot

def format_number(value, digits=1):
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "-"

def format_time(seconds):
    try:
        seconds = max(0.0, float(seconds))
    except (TypeError, ValueError):
        return "00:00.00"

    mins = int(seconds // 60)
    secs = seconds % 60
    if mins:
        return f"{mins:02d}:{secs:05.2f}"
    return f"00:{secs:05.2f}"

def format_datetime(dt):
    return dt.strftime("%d %b %Y %H:%M") if dt else "-"

def meters_to_feet(meters):
    try:
        return float(meters) * 3.28084
    except (TypeError, ValueError):
        return 0.0

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def distance2d(lat1, lon1, lat2, lon2):
    # lightweight for threshold checks only
    return hypot((lat2 - lat1) * 111_000, (lon2 - lon1) * 111_000)
