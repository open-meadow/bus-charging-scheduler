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

def get_selected_buses():
    scenario_name = st.selectbox(
        "Pick scenario",
        list(SCENARIOS.keys())
    )

    return SCENARIOS[scenario_name]

def simulate_buses(bus):
    current_time = to_minutes(bus["departure"])
    charging_plan = ["B", "D"]
    events = []
    current_station = "Bengaluru"
    
    for station in charging_plan:
        
        distance_to_station = get_distance_between(current_station, station)
        travel_time = int((distance_to_station / SPEED) * 60)
        current_time += travel_time
        charge_start = current_time
        charge_end = charge_start + CHARGE_DURATION
        
        events.append(
            ChargingEvent(
                station=station,
                arrival_time=current_time,
                charge_start=charge_start,
                charge_end=charge_end,
                wait_time=CHARGE_DURATION
            )
        )
        
        current_time = charge_end
        current_station = station
    
    distance_to_destination = get_distance_between(
        current_station,
        "Kochi"
    )
    
    travel_time = int((distance_to_destination / SPEED) * 60)
    arrival_time = current_time + travel_time
    
    return {
        "bus_id": bus["id"],
        "charging_events": events,
        "arrival_time": arrival_time
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