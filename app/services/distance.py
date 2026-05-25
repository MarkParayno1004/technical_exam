from haversine import Unit, haversine


def distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Return great-circle distance in kilometers between two coordinate pairs."""
    return haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)
