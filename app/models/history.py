from datetime import datetime
from ..extensions import db

class HistoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    run_id = db.Column(db.String(32), nullable=False, index=True)
    target_m = db.Column(db.Float, nullable=False)
    distance_m = db.Column(db.Float, nullable=False)
    time_text = db.Column(db.String(32), nullable=False)
    top_speed = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(32), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.created_at.strftime("%d %b %Y %H:%M"),
            "target_m": round(self.target_m, 1),
            "distance_m": round(self.distance_m, 1),
            "time": self.time_text,
            "top_speed": round(self.top_speed, 2),
            "status": self.status,
            "run_id": self.run_id,
        }
