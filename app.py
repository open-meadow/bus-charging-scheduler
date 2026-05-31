import streamlit as st
import pandas as pd

from scenario_loader import SCENARIOS
from constants import SPEED, SEGMENTS, STATIONS, DISTANCES, CHARGE_DURATION
from models import ChargingEvent

def to_minutes(time_string):
    hours, minutes = map(int, time_string.split(":"))
    return hours * 60 + minutes

def get_distance_between(start, end):
    return abs(
        DISTANCES[end] - DISTANCES[start]
    )

def is_valid(plan):
    points = ["Bengaluru"] + plan + ["Kochi"]
    
    for i in range(len(points) - 1):
        distance = abs(DISTANCES[points[i + 1]] - DISTANCES[points[i]])
        if distance > MAX_RANGE:
            return False
    return True

def get_selected_buses():
    scenario_name = st.selectbox(
        "Pick scenario",
        list(SCENARIOS.keys())
    )

    return SCENARIOS[scenario_name]

def simulate_buses(bus, charging_plan=None):
    current_time = to_minutes(bus["departure"])
    current_station = "Bengaluru"

    timeline = []

    # default plan (temporary — later scheduler will generate this)
    if charging_plan is None:
        charging_plan = ["B", "D"]

    timeline.append({
        "event": "DEPART",
        "location": "Bengaluru",
        "time": current_time,
        "bus_id": bus["id"]
    })

    for station in STATIONS:
        # travel to next station
        distance = get_distance_between(current_station, station)
        travel_time = int((distance / SPEED) * 60)
        current_time += travel_time

        timeline.append({
            "event": "ARRIVE",
            "location": station,
            "time": current_time,
            "bus_id": bus["id"]
        })

        # charging decision happens HERE
        if station in charging_plan:
            charge_start = current_time
            charge_end = charge_start + CHARGE_DURATION

            timeline.append({
                "event": "CHARGE_START",
                "location": station,
                "time": charge_start,
                "bus_id": bus["id"]
            })

            timeline.append({
                "event": "CHARGE_END",
                "location": station,
                "time": charge_end,
                "bus_id": bus["id"]
            })

            current_time = charge_end

        current_station = station

    # final leg to Kochi
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
    

def generate_schedule(buses):
    schedule = []

    for bus in buses:
        current_time = to_minutes(bus["departure"])

        schedule.append({
            "bus_id": bus["id"],
            "event": "DEPART",
            "time": current_time,
            "location": "Bengaluru"
        })

        for index, distance in enumerate(SEGMENTS):
            travel_time = int((distance / SPEED) * 60)
            current_time += travel_time

            if index < len(STATIONS):
                location = STATIONS[index]
            else:
                location = "Kochi"

            schedule.append({
                "bus_id": bus["id"],
                "event": "ARRIVE",
                "time": current_time,
                "location": location
            })

    return schedule

def render_station_view(schedule):
    st.subheader("Station View")

    for station in STATIONS:
        st.markdown(f"### Station {station}")

        arrivals = [
            event
            for event in schedule
            if event["event"] == "ARRIVE"
            and event["location"] == station
        ]

        arrivals.sort(key=lambda event: event["time"])

        if arrivals:
            st.dataframe(pd.DataFrame(arrivals))
        else:
            st.write("No arrivals")


def main():
    st.title("Bus Charging Scheduler")

    buses = get_selected_buses()

    st.subheader("Input Buses")
    st.dataframe(pd.DataFrame(buses))

    st.subheader("Simulation Results")
    for bus in buses:
        result = simulate_buses(bus)
        st.write(result)

    schedule = generate_schedule(buses)

    st.subheader("Generated Schedule")
    st.dataframe(pd.DataFrame(schedule))

    render_station_view(schedule)


if __name__ == "__main__":
    main()