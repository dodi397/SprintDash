from dataclasses import dataclass, asdict, field

@dataclass
class RaceModel:
    target_m: float = 201.0
    distance_m: float = 0.0
    distance_ft: float = 0.0
    elapsed_time: float = 0.0
    current_speed: float = 0.0
    top_speed: float = 0.0
    status: str = "IDLE"
    gps_ready: bool = False
    gps_accuracy: float | None = None
    lat: float | None = None
    lon: float | None = None
    started_at: str | None = None
    finished_at: str | None = None
    run_id: str = "N/A"
    path: list = field(default_factory=list)
    armed_at_lat: float | None = None
    armed_at_lon: float | None = None
    timer_started: bool = False

    def to_dict(self):
        return asdict(self)
