from itertools import combinations

# from app import is_valid, simulate_buses
from constants import CHARGE_DURATION, DISTANCES, MAX_RANGE, SPEED, STATIONS
from helpers import get_distance_between, to_minutes

class Scheduler:
    def __init__(self, speed, stations, distances, max_range, charge_duration):
        self.speed = speed
        self.stations = stations
        self.distances = distances
        self.max_range = max_range
        self.charge_duration = charge_duration
        self.all_plans = self.generate_all_charging_plans()
        
    # check if generated plan is valid    
    def _is_valid(self, plan):
        points = ["Bengaluru"] + plan + ["Kochi"]
    
        for i in range(len(points) - 1):
            distance = abs(DISTANCES[points[i + 1]] - DISTANCES[points[i]])
            if distance > MAX_RANGE:
                return False
        
        return True

    # generate all plans    
    def _generate_all_charging_plans(self):
        valid_plans = []
    
        for i in range(len(self.stations) + 1):
            for combo in combinations(self.stations, i):
                plan = list(combo)
            
                if self._is_valid(plan):
                    valid_plans.append(plan)
    
        return valid_plans
    
    def simulate_buses(bus, charging_plan):
        current_time = to_minutes(bus["departure"])
        current_station = "Bengaluru"
        
        timeline = []
        timeline.append({
            "event": "DEPART",
            "location": current_station,
            "time": current_time,
            "bus_id": bus["id"]
        })
        
        for station in STATIONS:
            distance = get_distance_between(current_station, station)
            travel_time = int((distance/SPEED) * 60)
            current_time += travel_time
            
            # when any station is reached, append "ARRIVE"
            timeline.append({
                "event": "ARRIVE",
                "location": station,
                "time": current_time,
                "bus_id": bus["id"]
            })
            
            # charging decision happens here
            if station in charging_plan:
                current_time = current_time + CHARGE_DURATION
                
                timeline.append({
                    "event": "CHARGE",
                    "location": station,
                    "time": current_time,
                    "bus_id": bus["id"]
                })
            
            current_station = station
        
        distance = get_distance_between(current_station, "Kochi")
        travel_time = int((distance / SPEED) * 60)
        current_time += travel_time
        
        timeline.append({
            "event": "ARRIVE",
            "location": "Kochi",
            "time": current_time,
            "bus_id": bus["id"]
        })
        
        return {
            "bus_id": bus["id"],
            "timeline": timeline,
            "arrival_time": current_time
        }
    
    def schedule_bus(self, bus): 
        best_plan = None
        best_score = float("inf")
        
        for plan in self.all_plans:
            result = self.simulate_buses(bus, plan)
            score = self.score(result)
            
            if score < best_score:
                best_score = score
                best_plan = plan
                best_result = result
        
        return {
            "bus_id": bus["id"],
            "best_plan": best_plan,
            "best_score": best_score,
            "best_result": best_result
        }
    
    