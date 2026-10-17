import pandas as pd
import requests
import matplotlib.pyplot as plt

# Read Frost Client ID from file
with open("frost_client_id.txt", "r") as file:
    client_id = file.read().strip()

# Frost API endpoint
endpoint = "https://frost.met.no/observations/v0.jsonld"

# Parameters for the API request
parameters={
    "sources": "SN17850",
    "elements": "air_temperature",
    "referencetime": "2025-01-01/2025-12-31"
  }

# Request data from Frost API
response = requests.get(
    endpoint,
    params=parameters,
    auth=(client_id, "")        
)

# Check status code
print("Status code:", response.status_code)

# Convert response to JSON
json_data = response.json()

# Extract data
rows = []

for item in json_data["data"]:
    rows.append({
        "date": item["referenceTime"],
        "temperature": item["observations"][0]["value"]
    })

# Create DataFrame
df_temp = pd.DataFrame(rows)

# Convert dates
df_temp["date"] = pd.to_datetime(df_temp["date"])

# Display first rows
print("\nFirst 5 rows:")
print(df_temp.head())

# Plot temperature
plt.figure(figsize=(12, 5))

plt.plot(
    df_temp["date"],
    df_temp["temperature"],
    color="red"
)

plt.title("Daily Mean Temperature in 2025")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.show()

# Summary statistics
summary = pd.DataFrame({
    "Statistic": ["Mean", "Median", "Minimum", "Maximum"],
    "Temperature": [
        df_temp["temperature"].mean(),
        df_temp["temperature"].median(),
        df_temp["temperature"].min(),
        df_temp["temperature"].max()
    ]
})

print("\nTemperature Summary Statistics:")
print(summary)
  # Replace with your desired weather station ID