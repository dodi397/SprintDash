from ..extensions import db
from ..models.history import HistoryEntry

class HistoryService:
    def list_history(self):
        rows = HistoryEntry.query.order_by(HistoryEntry.id.desc()).all()
        return [row.to_dict() for row in rows]

    def add_history(self, payload):
        row = HistoryEntry(
            run_id=payload.get("run_id", "N/A"),
            target_m=float(payload.get("target_m", 0)),
            distance_m=float(payload.get("distance_m", 0)),
            time_text=payload.get("time", "00:00.00"),
            top_speed=float(payload.get("top_speed", 0)),
            status=payload.get("status", "Selesai"),
        )
        db.session.add(row)
        db.session.commit()
        return row.to_dict()

    def clear(self):
        HistoryEntry.query.delete()
        db.session.commit()
        return True

history_service = HistoryService()
