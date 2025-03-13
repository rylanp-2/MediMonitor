# boot.py -- run on boot-up
import network
import machine
import config

led = machine.Pin(25, machine.Pin.OUT)

# Replace the following with your WIFI Credentials
SSID = "MediMonitor"
PASSWORD = "1234"

print("Creating Accesspoint with the following", SSID, PASSWORD)

ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID, password=PASSWORD)
ap.active(True)  # Activate the access point

while ap.active() is False:
    pass
print("Connection is successful")
print(ap.ifconfig())
led.value(1)

config.ip = ap.ifconfig()
