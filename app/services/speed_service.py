class SpeedService:
    @staticmethod
    def calculate_speed(distance_m, elapsed_seconds):
        elapsed_seconds = max(float(elapsed_seconds or 0), 0.001)
        return max(0.0, float(distance_m or 0.0) / elapsed_seconds)

    @staticmethod
    def calculate_segment_speed(segment_distance_m, segment_seconds):
        segment_seconds = max(float(segment_seconds or 0), 0.001)
        return max(0.0, float(segment_distance_m or 0.0) / segment_seconds)

speed_service = SpeedService()
