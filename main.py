import numpy as np

from data import charging_demand_probabilities, arrival_probabilities

# Constants
charge_power = 11
num_chargepoints = 20
total_ticks = 35040

charge_dist_keys = list(charging_demand_probabilities.keys())
charge_dist_values = [(km / 100) * 18 for km in charging_demand_probabilities.values()]  # (kmh)

charge_probabilities = [float(k[:-1]) / 100 for k in charge_dist_keys]
charge_probabilities = np.array(charge_probabilities) / np.sum(charge_probabilities)

# simulation arrays
power_demand = np.zeros(total_ticks)
chargepoints_status = np.zeros(num_chargepoints)

for tick in range(total_ticks):
    hour_of_day = (tick // 4) % 24
    hour_key = list(arrival_probabilities.keys())[hour_of_day]

    evs_arriving = np.random.binomial(num_chargepoints, arrival_probabilities[hour_key] / 100)

    for i in range(evs_arriving):
        available_chargepoints = np.where(chargepoints_status == 0)[0]

        if len(available_chargepoints) > 0:
            charge_idx = np.random.choice(len(charge_dist_keys), p=charge_probabilities)
            charging_need_kwh = charge_dist_values[charge_idx]

            if charging_need_kwh > 0:
                charging_duration = charging_need_kwh / charge_power

                ticks_to_charge = int(charging_duration * 4)
                chosen_point = available_chargepoints[0]

                chargepoints_status[chosen_point] = ticks_to_charge

    power_demand[tick] = np.sum(chargepoints_status > 0) * charge_power

    chargepoints_status = np.maximum(chargepoints_status - 1, 0)

total_energy_consumed = np.sum(power_demand) * (15 / 60)
theoretical_max_power = charge_power * num_chargepoints
actual_max_power = np.max(power_demand)
concurrency_factor = actual_max_power / theoretical_max_power

print(f"Total energy consumed: {total_energy_consumed} kWh")
print(f"Theoretical maximum power demand: {theoretical_max_power} kW")
print(f"Actual maximum power demand: {actual_max_power} kW")
print(f"Concurrency factor: {concurrency_factor}")

# Reference: Some assistance provided by ChatGPT
