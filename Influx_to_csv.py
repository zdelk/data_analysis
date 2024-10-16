# Author
# Python Script to Export Sensor Data from InfluxDB

import csv
from influxdb_client import InfluxDBClient

# Connection Params for InfluxDB
url = "http://192.168.1.203:8086"
token = "aDVYN_ZuSubXa4FuXdOK_YQk5WDTk-Xl30vZOQZi0Utn5-15OrqO2MWK9iASrwC4cEOzCsDvMWzGGCTDdXvCqQ=="
org = "Southface"
bucket = "SensorBucket"

# Time Range for export (will add usr input)
start = "-30m"
stop = "now()"



# List of metrics (measurements and fields) to pull
metrics = [
    {"measurement": "airgradient_co2_ppm"},
    {"measurement": "airgradient_humidity_compensated_percent"},
    {"measurement": "airgradient_humidity_percent"},
    {"measurement": "airgradient_temperature_celsius"},
    {"measurement": "airgradient_co2_ppm"},
    {"measurement": "airgradient_humidity_compensated_percent"},
    {"measurement": "airgradient_humidity_percent"},
    {"measurement": "airgradient_nox_index"},
    {"measurement": "airgradient_nox_raw"},
    {"measurement": "airgradient_pm0d3_p100ml"},
    {"measurement": "airgradient_pm10_ugm3"},
    {"measurement": "airgradient_pm1_ugm3"},
    {"measurement": "airgradient_pm2d5_ugm3"},
    {"measurement": "airgradient_temperature_compensated_celsius"},
    {"measurement": "airgradient_tvoc_index"},
    {"measurement": "airgradient_tvoc_raw"},
]


# Create the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# Define a Flux query to retrieve multiple metrics together
query = """from(bucket: "SensorBucket")
  |> range(start: -24h)
  |> filter(fn: (r) => r["_measurement"] == "airgradient_temperature_celsius"
    or r["_measurement"] == "airgradient_co2_ppm"
    or r["_measurement"] == "airgradient_humidity_compensated_percent"
    or r["_measurement"] == "airgradient_humidity_percent"
    or r["_measurement"] == "airgradient_nox_index"
    or r["_measurement"] == "airgradient_nox_raw"
    or r["_measurement"] == "airgradient_pm0d3_p100ml"
    or r["_measurement"] == "airgradient_pm10_ugm3"
    or r["_measurement"] == "airgradient_pm1_ugm3"
    or r["_measurement"] == "airgradient_pm2d5_ugm3"
    or r["_measurement"] == "airgradient_temperature_compensated_celsius"
    or r["_measurement"] == "airgradient_tvoc_index"
    or r["_measurement"] == "airgradient_tvoc_raw")
  |> filter(fn: (r) => r["_field"] == "gauge")
"""

# Run the query
query_api = client.query_api()
tables = query_api.query(query)





# Process results into a dictionary with timestamps as keys
data_dict = {}

for table in tables:
    for record in table.records:
        # print(record)
        time = record.get_time()
        # print(time)
        value = record.get_value()
        # print(value)
        measurement = record.get_measurement()


        # Initialize dictionary entry for the time if it doesn't exist
        if time not in data_dict:
            data_dict[time] = {}
        
        # Store the value for the corresponding field
        data_dict[time][measurement] = value


with open('influxdb_export.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write header
    header = ["time"] + [metric['measurement'] for metric in metrics]
    csvwriter.writerow(header)

    # Write data rows
    for time, values in data_dict.items():
        row = [time] + [values.get(metric['measurement'], None) for metric in metrics]
        csvwriter.writerow(row)

print("Data exported to influxdb_export.csv")

client.close()