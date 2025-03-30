import machine
import utime
import math
import dht


# Define the pins used for the thermistors and DHT11
therm_black = machine.ADC(27)
thermistor = machine.ADC(26)
# d = dht.DHT11(machine.Pin(15))


# Introduce constants used for the thermistor calculations
room_temp = 298.15
beta = 3960
R0 = 10000


def read_temps():
    
    # DHT11 code:

#     d.measure()  # Read data from the DHT11
#     temp1 = d.temperature()  # Store temperature data in variable temp1
#     hum = d.humidity()  # Store humidity data in variable hum

    hum = 50
    temp1 = 22
    
        

    # Thermistor 1 (black):

    therm1_reading = therm_black.read_u16()  # Read ADC input

    therm1_V = 3.3 * float(therm1_reading) / 65535  # Convert ADC input to voltage
    therm1_res = 10000 * therm1_V / (3.3 - therm1_V)  # Convert voltage to resistance
    temp2_K = 1 / (((math.log(therm1_res / 10000)) / 3950) + (1 / (273.15 + 25)))  # Convert resistance to temperature in Kelvin
    temp2_C = (temp2_K - 273.15)  # Convert temperature in Kelvin to temperature in degrees Celsius

    # Thermistor 2 (orange):

    therm_reading = thermistor.read_u16()
    voltage = therm_reading * (3.3 / 65535)
    resistance = 10000 * voltage / (3.3 - voltage)
    Temp_kelvin = 1 / ((1 / room_temp) + (1 / beta) * math.log(resistance / R0))
    temp3 = Temp_kelvin - 273.15

    # Calculate the average of the 3 temperatures
    avg_temp = (temp1 + temp2_C + temp3) / 3  # Calculate the average of the temperatures

    
    unix_time = utime.time() # Retrieve the the number of seconds since the epoch
    data = [temp1, temp2_C, temp3, avg_temp, hum, unix_time] # Put all measured values into a list

    return data # Return data as a list of values


def convert_list(data):
    tempstr = ", ".join([str(s) for s in data]) # Convert that list to a string
    return tempstr


def hum_status(hum):

    if(hum > 75):
        hum_status = 2
        
    elif(hum > 60):
        hum_status = 1
        
    else:
        hum_status = 0
        
    return hum_status