from dataclasses import dataclass
from ..utils.helpers import distance2d

@dataclass
class GPSFix:
    lat: float | None = None
    lon: float | None = None
    accuracy: float | None = None
    ready: bool = False

class GPSService:
    @staticmethod
    def normalize(lat, lon, accuracy=None):
        try:
            lat = float(lat)
            lon = float(lon)
            accuracy = None if accuracy is None else float(accuracy)
        except (TypeError, ValueError):
            return GPSFix()
        return GPSFix(lat=lat, lon=lon, accuracy=accuracy, ready=True)

    @staticmethod
    def moved_enough(prev_lat, prev_lon, lat, lon, threshold_m):
        if prev_lat is None or prev_lon is None:
            return False
        return distance2d(prev_lat, prev_lon, lat, lon) >= threshold_m

gps_service = GPSService()
