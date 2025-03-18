# boot.py -- run on boot-up
import network
import machine
import config

led = machine.Pin(25, machine.Pin.OUT)

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
print(ap.ifconfig("addr4"))
led.value(1)

config.ip = ap.ifconfig("addr4")[0]


# Monitor new connections
def check_clients():
    clients = ap.status("stations")  # List of connected clients
    if clients:
        print("Connected devices:", clients)
