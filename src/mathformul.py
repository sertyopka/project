from math import radians, sin, cos, asin, sqrt

def haversine(lat1, lon1, lat2, lon2, R=6371):
    dphi = radians(lat2 - lat1)
    dlam = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlam/2)**2
    return 2 * R * asin(sqrt(a))
