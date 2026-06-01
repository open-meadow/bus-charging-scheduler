from constants import DISTANCES

def to_minutes(time_string):
    hours, minutes = map(int, time_string.split(":"))
    return hours * 60 + minutes

def get_distance_between(start, end):
    return abs(
        DISTANCES[end] - DISTANCES[start]
    )