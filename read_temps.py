import machine
import utime
import math
import dht


# Define the pins used for the thermistors and DHT11
therm_black = machine.ADC(27)
thermistor = machine.ADC(26)
d = dht.DHT11(machine.Pin(15))

global prev_time, prev_temp1, prev_hum

prev_time = utime.time() - 2
prev_temp1 = 20
prev_hum = 50

# Introduce constants used for the thermistor calculations
room_temp = 298.15
beta = 3960
R0 = 10000


def read_temps():
    
    global prev_time, prev_temp1, prev_hum
    
    
    
    # DHT11 code:
    
    unix_time = utime.time() # Retrieve the the number of seconds since the epoch
    
    # Compare the time of this measurement to the time of the last measurement
    # Update temp1 only if at least 2 seconds have passed since the last request (This is due to hardware constraints of the DHT11)
    if (unix_time > prev_time + 1):
        # Handle exceptions if the DHT11 malfunctions for whatever reason
        try: 
            d.measure()  # Read data from the DHT11
            temp1 = d.temperature()  # Store temperature data in variable temp1
            hum = d.humidity()  # Store humidity data in variable hum
            prev_time = unix_time
            prev_temp1 = temp1
            prev_hum = hum
        except Exception as e:
            print("Error reading DHT:", e)
            temp1 = prev_temp1
            hum = prev_hum
        
    else: # Otherwise use the previous values
        temp1 = prev_temp1
        hum = prev_hum
        unix_time = prev_time
        

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