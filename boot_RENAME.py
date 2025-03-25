# boot.py -- run on boot-up
import network
from machine import Pin
import config

led = Pin("LED", Pin.OUT)

# BEGIN basic networking

# Replace the following with your WIFI Credentials
SSID = "MediMonitor"
PASSWORD = "12345678"

print("Creating Accesspoint with the following", SSID, PASSWORD)

ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID, password=PASSWORD)
ap.active(True)  # Activate the access point

while not ap.active():
    pass

print("Connection is successful")
print(ap.ifconfig())
led.value(1)

config.ip = ap.ifconfig()[0]

# END


# Monitor new connections
def check_clients():
    clients = ap.status("stations")  # List of connected clients
    if clients:
        print("Connected devices:", clients)
