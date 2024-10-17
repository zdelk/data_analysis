##=============================================================##
## Script Name  : query_and_email.py
## Author       : Zachary Delk
## Company      : Southface
## Project      : IAQ Sensor IOT w/RaspPi
## Created Date : 08/17/2024
## Version      : v0.1
## Description  :
##    This script runs a query on InfluxDB, exports the
##     results to a CSV file, and emails the file to a
##     specified recipient.
##
## Requirements :
##     - Python 3.x
##     - InfluxDB Python client
##     - smtplib for email functionality
##     - csv for writing data
##     - Updated secrets_q_e.py (ip-address, token, sender email,
##                               sender email password)
##     - Other dependencies as required
##
## Usage        :
##     python query_and_email.py
##
## Notes        :
##     - Update InfluxDB credentials and recipient email in the
##       configuration section.
##     - Updated secrets_q_e.py (ip-address, token, sender email,
##                               sender email password)
##     - Ensure all necessary packages are installed.
##=============================================================##
## PACKAGE IMPORTS ##
# Queary Packages #
from secrets_q_e import *
import csv  # Writing csvs
from influxdb_client import InfluxDBClient  # Interacting with InfluxDB

# Emailer Packages
import smtplib  # Use SMTP server
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from date_range import get_time_range

# ---------------------------------------------------------------#
# ------------Action Portion ------------------------------------#
# Queary Portion #

# Connection Parmas for Influx DB


# print("""How much data do you want?
#       Enter number and unit together
#       (Units: m, h, d, w)
#       Examples:
#       '30m' -> 30 minutes
#       '2h'  -> 2 hours
#       '5d'  -> 5 days """)

# Example usage
duration = input("Enter the time range (e.g., '30m', '2h', '5d'): ")
try:
    time_range = get_time_range(duration)
    print(time_range)
except ValueError as e:
    print(e)

# start = input("Timeframe: ")
# Time range for export
# start = "-30m" # CHANGE TO USR INPUT
# stop = "now()" # CHANGE TO USR INPUT

# Initilize InfluxDB client object
client = InfluxDBClient(url=url, token=token, org=org)

# Look into string formating to make this cleaner
query = f"""from(bucket: "{bucket}")
  |> range(start: -{duration})
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

## Run the query
# Each metric generates its own table
query_api = client.query_api()
tables = query_api.query(query)  # List of tables object

# Can close query clinet after tables object is created
client.close()
## Writing to .csv

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

## Data Dictionary Creation
# Initilize dictionary to put data in
# (Timestaps will be keys)
data_dict = {}

for table in tables:
    for record in tables.records:
        time = record.get_time()  # Need to edit to do local instead of UTC

        value = record.get_value()

        measurement = record.get_measurement()

        if time not in data_dict:
            data_dict[time] = {}

        data_dict[time][measurement] = value

filename = input("Name of file with extension (ie Test_File.csv): ")
# Writing data dictionary to csv file (Add usr input for name/outputpath)
with open(filename, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write header row
    header = ["time"] + [metric["measurment"] for metric in metrics]
    csvwriter.writerow(header)

    # Write data rows
    for time, values in data_dict.items():
        row = [time] + [values.get(metric["measurment"], None) for metric in metrics]
        csvwriter.writerow(row)

# ---------------------------------------------------------------#
## Email Section

# Recipient Addresses
toaddr = input("Enter email address to send file to: ")
print("File will sent to ", toaddr)

# Create MIMEMultipart object
msg = MIMEMultipart()

# Store sender email address
msg["From"] = fromaddr

# Store Recipient(s) email address
msg["To"] = toaddr

# Add Subject Line
msg["Subject"] = f"Sensor Data from {time_range}"

# String for body of email
body = f"""This email was sent from a raspberry pi.
        The attached file includes all data for all
        metrics from the sensor in the time frame of
        {time_range}"""

# Attaching body to msg instance
msg.attach(MIMEText(body, "plain"))

attachement = open(filename, "rb")

p = MIMEBase("application", "octet-stream")

encoders.encode_base64(p)

p.add_header("Content-Disposition", "attachment: filename = %s" % filename)

# Attaches instance 'p' to instance 'msg'
msg.attach(p)

# Start SMTP session
s = smtplib.SMTP("smtp.gmail.com", 587)  # 587 Port specific to gmail

# Security for rest of SMTP session
s.starttls()

# Authentication (For Gmail, app password required)
s.login(fromaddr, fromaddrpass)

# Covert Multipart msg to string
text = msg.as_string()

# Sends email
s.sendmail(fromaddr, toaddr, text)

# End SMTP session
s.quit()

print(f"Data exported to {filename} and send to {fromaddr}")