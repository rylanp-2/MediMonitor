import machine
import utime
import dht
import math


d = dht.DHT11(machine.Pin(15))
therm_black = machine.ADC(27)
thermistor = machine.ADC(26)

temp_upper = 26
temp_lower = 20
room_temp = 298.15
beta = 3960
R0 = 10000

global temp1
global temp2_C
global temp3
global hum
global avg_temp
global unix_time

reset = False
timer_on = False
hazard_time = 0


def read_temps():
    # DHT11 code:

    d.measure()  # Read data from the DHT11
    temp1 = d.temperature()  # Store temperature data in variable temp1
    hum = d.humidity()  # Store humidity data in variable hum

    # Thermistor 1 (black):

    therm1_reading = therm_black.read_u16()  # Read ADC input

    therm1_V = 3.3 * float(therm1_reading) / 65535  # Convert ADC input to voltage
    therm1_res = 10000 * therm1_V / (3.3 - therm1_V)  # Convert voltage to resistance
    temp2_K = 1 / (
        ((math.log(therm1_res / 10000)) / 3950) + (1 / (273.15 + 25))
    )  # Convert resistance to temperature in Kelvin
    temp2_C = (
        temp2_K - 273.15
    )  # Convert temperature in Kelvin to temperature in degrees Celsius

    # Thermistor 2 (orange):

    therm_reading = thermistor.read_u16()
    voltage = therm_reading * (3.3 / 65535)
    resistance = 10000 * voltage / (3.3 - voltage)

    Temp_kelvin = 1 / ((1 / room_temp) + (1 / beta) * math.log(resistance / R0))
    temp3 = Temp_kelvin - 273.15

    avg_temp = (
        temp1 + temp2_C + temp3
    ) / 3  # Calculate the average of the temperatures

    unix_time = utime.time()

    data = [temp1, temp2_C, temp3, avg_temp, hum, unix_time]

    tempstr = ", ".join([str(s) for s in data])

    return tempstr


temp_file = open("temps_test.txt", "a")

# while True:
#     temp_str = read_temps()
#
#     temp_file.write(temp_str)
#
#     print(temp_str)  # Print out all measured values
#     #     print("Danger:", str(timer_on), "Time:", hazard_time)
#     #
#     #
#     #     if (avg_temp <= 22):
#     #         reset = True
#     #
#     #     if (temp1 < temp_lower or temp2_C < temp_lower or temp3 < temp_lower):
#     #         print("too cold")
#     #
#     #     if (temp1 > temp_upper or temp2_C > temp_upper or temp3 > temp_upper):
#     #         print("too warm💀")
#     #         timer_on = True
#     #
#     #     if (timer_on == True):
#     #         hazard_time += 1
#     #
#     #     if (reset == True):
#     #         timer_on = False
#     #         hazard_time = 0
#     #         reset = False
#
#     utime.sleep(1)  # Repeat every 1 second

temp_file.close
