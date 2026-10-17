import pandas as pd
import os
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv


load_dotenv()
client_id = os.getenv("client_id")
print(client_id)



# Retrives the wanted information and puts it in a dictionary
endpoint_avg = "https://frost.met.no/observations/v0.jsonld"
parameters_avg = {
    "sources": "SN17850",
    "elements": "mean(air_temperature P1D)",
    "referencetime": "2025-01-01/2025-12-31",
}

# Sends a get-request to Frost for the wanted information and decodes it
response_avg = requests.get(endpoint_avg, parameters_avg, auth=(client_id, ""))
json_data_avg = response_avg.json()
data_avg = json_data_avg["data"]

# Creates a dataframe
values_avg = pd.DataFrame()

frames_moving_avg = []
avg_values = []
frames_avg = []

# Retrives the wanted information and appends it to two lists
for e in range(len(data_avg)):
    # Retrives the relevant information from data_avg and appends it to a list
    row = pd.DataFrame(data_avg[e]["observations"])
    row["referencetime"] = pd.to_datetime(data_avg[e]["referenceTime"])
    row["sources"] = data_avg[e]["sourceId"]
    frames_avg.append(row)

    # Retrives the relevant information, appends it to a list, and calculates the last seven day moving average
    val = data_avg[e]["observations"][0]["value"]
    avg_values.append(val)
    last_seven = avg_values[-7:]
    last_seven_avg = sum(last_seven) / len(last_seven)

    # Appends the seven day moving average to a list
    data_avg[e]["observations"][0]["value"] = last_seven_avg
    avg_row = pd.DataFrame(data_avg[e]["observations"])
    avg_row["referencetime"] = pd.to_datetime(data_avg[e]["referenceTime"])
    avg_row["sources"] = data_avg[e]["sourceId"]
    frames_moving_avg.append(avg_row)
    seven_day_moving_avg = frames_moving_avg[::7]

# Combines several dataframes
values_avg = pd.concat(frames_avg, ignore_index=True)
moving_values = pd.concat(seven_day_moving_avg, ignore_index=True)

# Plots the values
ax = plt.subplot()
values_avg.plot.scatter(x="referencetime", y="value", s=4, ax=ax)
moving_values.plot(x="referencetime", y="value", ax=ax, color="red")
