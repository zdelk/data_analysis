# Hardware
Pi: Raspberry Pi model 4b 1Gb with 64gb sd
 - Link: https://www.microcenter.com/product/665122/raspberry-pi-4-model-b

Wifi Adapter: BrosTrend 650Mbps Linux Compatible WiFi Adapter
 -  Link: https://www.amazon.com/dp/B01GC8XH0S?ref=ppx_yo2ov_dt_b_fed_asin_title

IAQ Sensor: AirGradient ONE Indoor Monitor I-9PSL 9th Gen (kit)
 -  Link: https://www.airgradient.com/indoor/


# Sensor Setup
Build instruction Link: https://www.airgradient.com/documentation/one-v9/

The AirGradient sensor was purchased as a presoldered kit. The provided build instructions were used. No extra sensors have been added to the system at this point. 

After the sensor was put together, the usb to usb-c cable was used to connect the sensor to my laptop. The Default AirGradient software was flashed to the system. 

After flashing the sensor broadcasts a wifi signal that was connected to (airgradient-XXXXXXXX). When connected to the sensors broadcast, a WebUI comes up which allows you to connect the sensor to wifi. The available networks are displayed but you can also connect to hidden networks provided you have the SSID and password. 

This sensor was connected to the wifi being brodcasted by the Raspberry Pi (See Rapsberry Pi Setup: Hotspot). 
SSID: sfpiap
password: testpass (will probably update later)

There is an option on the sensor setup to publish data to AirGradient API. I left it enabled for the time being to test
After connecting to the internet, the sensor should start collecting data.
By default, the sensor publishes data to \<sensor-ip-address\>:80/metrics (also to \<sensor-ip-address\>:80/measures/current but that one doesn't seem to work for prometheus). 

To find the Ip address of the sensor on the local(hotspot) network you can run 'arp -a'. The sensor can be found by its MAC address (its the same as the wifi connection). Use 'curl -h http://\<sensor-ip-address\>:80/metrics' to verify the sensor is publishing data. Once verified, add the sensor ip address to the the prometheus scape config file. 


### Note:
At one point there was an issue where the sensor wasn't publishing data to the AirGradient API. 
The purple light on the sensor was on as well. I'm not 100% sure why this was happening. 
I belive it was Port confliction with the Airgradient API and Influxdb

# Raspberry Pi Setup
Operating System: Debian GNU/Linux 12 (bookworm)
Kernel: Linux 6.6.51+rpt-rpi-v8
Architecture: arm64

## Raspberry Pi Initialization
Used 'Raspberry Pi Imager' to flash the OS to a blank 64gb microSD card
Made sure to enable ssh on setting.

## Hotspot
Adapter Used: "https://www.amazon.com/dp/B01GC8XH0S?ref=ppx_yo2ov_dt_b_fed_asin_title"

Followed the first half of this tutorial:
https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/
Note: Used the adapter for the hotspot broadcast
Ran 'nmcli device' and the adapter came up as 'wlxcc641aeb9931'.
So the 'Create hotspot network' step is a bit different.

	$ sudo nmcli device wifi hotspot ssid <hotspot name> password <hotspot password> ifname wlxcc641aeb9931 

The rest of the setup was the same the tutorial up to the 'Configure connection portal' which I didn't do. (might do later)

## Prometheus
Guide: https://pimylifeup.com/raspberry-pi-prometheus/

Changed download to: https://github.com/prometheus/prometheus/releases/download/v2.55.0/prometheus-2.55.0.linux-arm64.tar.gz

Skipped the 'Installing the Node Exporter Software' and 'Setting up the Node Exporter as a Service' sections

Also added the Airgradient job to 'prometheus.yml' 

```
  - job_name: 'airgradient_metric'
    metrics_path: /metrics
    scrape_interval: 15s
    static_configs:
      - targets: ['<Sensor-Ip-address>:80']
```

Notes:
 - LocalPage: http://localhost:9090
 - Tested with "/measures/current". Didn't seem to work
 - Prometheus is needed for Grafana
 - Might not be needed for Influxdb if using Telegraf. Need to test a bit more

## Grafana
Guide: https://pimylifeup.com/raspberry-pi-grafana/

Followed the full guide. It just goes through how to get web interface running. Doesnt go into adding data.
### Add Data Source
 - Go to http://<Pi-Ip-address>:3000
 - On left side look for Connections -> Data Source
 - Add new data source
 - Click/Find Prometheus
 - Give it a name. Put 'http://localhost:9090' for Connection
 - Scroll to bottom and 'Save and Test'. Should show green
 - Back to Data Sources. The one you added should show up. 
 - Click 'Build a dashboard'
 - Click 'Import dashboard'
 - Enter '20658' for 'URL or ID' and click 'Load' (premade dashboard I found)
 - Choose the data source you just added
 - Go to dashboards and it should show up
 - Should be good to go after that
 

### Notes:
 - LocalPage: http://localhost:3000
 - Just used for visualization

## Influxdb (v2)
Guide: https://pimylifeup.com/raspberry-pi-influxdb/

Chose to use v2. Not crazy about it. Might switch to v1

When setting it up you will have to enter a organization name. Used for scrapes/Telegraf

After following the guide and logging into Influxdb
 - Go to 'Load Data' -> 'Bucket'
 - 'Create Bucket' and give it a name
 - Go to 'API Tokens' -> 'Generate API Token' -> 'Custom API Token'
	- Give token a name
	- For Permissions, check Read/Write for the bucket you made
	- Click 'Generate' copy the provided key somewhere for later

After this you have to set up Telegraf (See Telegraf then come back)

 - With Telegraf configured and running
 - Go to 'Data Explorer'
 - Click on your bucket. airgradient_\<metrics\> should show
 - Click one and then click 'Submit' should see data graph
 
That's it for the Influxdb set up. A python script is used for exporting this data.

Notes:
 - LocalPage: http://localhost:8086
 - Might switch to v1


## Telegraf
 - Install Telegraf
 - Update /etc/telegraf/telegraf.conf
 - Restart Telegraf
 
## Tailscale
Lets traffic get out of local network.  
Install it on the pi then download the app on whatever device you are using.

