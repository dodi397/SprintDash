from datetime import datetime, timezone
from uuid import uuid4

from ..models.race_model import RaceModel
from ..utils.helpers import meters_to_feet, format_time
from ..utils.constants import (
    STATUS_IDLE, STATUS_READY, STATUS_ARMED, STATUS_RUNNING,
    STATUS_FINISHED, STATUS_NEED_LOCATION,
    MOVEMENT_THRESHOLD_M, MIN_ACCURACY_M
)
from .speed_service import speed_service
from .history_service import history_service
from .distance_service import haversine_meters

class RaceService:
    def __init__(self):
        self.state = RaceModel()
        self._started_clock = None
        self._armed_at = None
        self._last_point = None
        self._last_timestamp = None
        self._last_distance = 0.0

    def get_state(self):
        return self.state.to_dict()

    def set_target(self, target_m):
        self.state.target_m = float(target_m)
        if self.state.status == STATUS_IDLE:
            self.state.status = STATUS_READY
        return self.get_state()

    def set_location(self, lat, lon, accuracy=None):
        self.state.lat = float(lat)
        self.state.lon = float(lon)
        self.state.gps_accuracy = None if accuracy is None else float(accuracy)
        self.state.gps_ready = True
        if self.state.status == STATUS_IDLE:
            self.state.status = STATUS_READY
        return self.get_state()

    def start(self):
        if not self.state.gps_ready:
            self.state.status = STATUS_NEED_LOCATION
            return self.get_state()

        self.state.status = STATUS_ARMED
        self.state.timer_started = False
        self._armed_at = datetime.now(timezone.utc)
        self.state.armed_at_lat = self.state.lat
        self.state.armed_at_lon = self.state.lon
        self._last_point = (self.state.lat, self.state.lon)
        self._last_timestamp = self._armed_at
        self.state.elapsed_time = 0.0
        self.state.distance_m = 0.0
        self.state.distance_ft = 0.0
        self.state.current_speed = 0.0
        self.state.top_speed = 0.0
        self.state.path = []
        self.state.run_id = str(uuid4())[:8]
        self.state.started_at = None
        self.state.finished_at = None
        return self.get_state()

    def _start_timer_if_needed(self, lat, lon, accuracy):
        if self.state.status != STATUS_ARMED:
            return False

        if accuracy is not None and float(accuracy) > MIN_ACCURACY_M:
            return False

        if self.state.armed_at_lat is None or self.state.armed_at_lon is None:
            return False

        moved = haversine_meters(self.state.armed_at_lat, self.state.armed_at_lon, lat, lon)
        if moved < MOVEMENT_THRESHOLD_M:
            return False

        self.state.status = STATUS_RUNNING
        self.state.timer_started = True
        self._started_clock = datetime.now(timezone.utc)
        self.state.started_at = self._started_clock.isoformat()
        self._last_timestamp = self._started_clock
        self._last_point = (lat, lon)
        return True

    def update_position(self, lat, lon, accuracy=None):
        lat = float(lat)
        lon = float(lon)

        self.state.lat = lat
        self.state.lon = lon
        self.state.gps_ready = True
        if accuracy is not None:
            self.state.gps_accuracy = float(accuracy)

        if self.state.status == STATUS_ARMED:
            self._start_timer_if_needed(lat, lon, accuracy)

        if self.state.status != STATUS_RUNNING:
            return self.get_state()

        now = datetime.now(timezone.utc)
        elapsed = (now - self._started_clock).total_seconds() if self._started_clock else 0.0
        self.state.elapsed_time = elapsed

        if self._last_point is None:
            self._last_point = (lat, lon)

        segment_distance = haversine_meters(self._last_point[0], self._last_point[1], lat, lon)
        segment_seconds = (now - self._last_timestamp).total_seconds() if self._last_timestamp else 0.001
        self._last_point = (lat, lon)
        self._last_timestamp = now

        self.state.distance_m = max(self.state.distance_m, self._last_distance + segment_distance)
        self._last_distance = self.state.distance_m
        self.state.distance_ft = meters_to_feet(self.state.distance_m)

        current_speed = speed_service.calculate_segment_speed(segment_distance, segment_seconds)
        self.state.current_speed = current_speed
        self.state.top_speed = max(self.state.top_speed, current_speed)
        self.state.path.append({"lat": lat, "lon": lon, "t": elapsed})

        if self.state.distance_m >= self.state.target_m > 0:
            self.finish(auto=True)

        return self.get_state()

    def stop(self):
        if self.state.status in (STATUS_RUNNING, STATUS_ARMED):
            self.state.status = STATUS_FINISHED if self.state.distance_m >= self.state.target_m else "STOPPED"
        return self.get_state()

    def reset(self):
        target = self.state.target_m
        self.state = RaceModel(target_m=target)
        self._started_clock = None
        self._armed_at = None
        self._last_point = None
        self._last_timestamp = None
        self._last_distance = 0.0
        self.state.status = STATUS_IDLE
        return self.get_state()

    def finish(self, auto=False):
        self.state.status = STATUS_FINISHED
        self.state.finished_at = datetime.now(timezone.utc).isoformat()

        history_service.add_history({
            "run_id": self.state.run_id,
            "target_m": round(self.state.target_m, 1),
            "distance_m": round(self.state.distance_m, 1),
            "time": format_time(self.state.elapsed_time),
            "top_speed": round(self.state.top_speed, 2),
            "status": "Selesai" if auto else "Stop Manual",
        })
        return self.get_state()

race_service = RaceService()
