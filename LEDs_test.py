import machine
import utime
import math


#specify the pins which the LEDs connect to
gled = machine.Pin(14, machine.Pin.OUT)
rled = machine.Pin(12, machine.Pin.OUT)
yled = machine.Pin(13, machine.Pin.OUT)


def LEDs(temp1, temp2, temp3):
    
    #open a filestream containing the data from a config file for the threshold values
    with open("/static/config", "r") as filestream:
        for line in filestream:
            current_line = line.split(", ")
            high_bound = int(current_line[0])
            low_bound = int(current_line[1])

    #determine the warning range of the system
    warning_range = (high_bound - low_bound)/4
    high_warning = high_bound - warning_range
    low_warning = low_bound + warning_range

    
    # Turn on the correct LED based on the temperature the temperature of each of the thermistors
    
    if (temp1 <= low_bound or temp1 >= high_bound or temp2 <= low_bound or temp2 >= high_bound or temp3 <= low_bound or temp3 >= high_bound):
        rled.value(1)
        yled.value(0)
        gled.value(0)
        status = 2 # Set the status to 2 (critical)
    elif (temp1 <= low_warning or high_warning <= temp1 or temp2 <= low_warning or high_warning <= temp2 or temp3 <= low_warning or high_warning <= temp3):
        rled.value(0)
        yled.value(1)
        gled.value(0)
        status = 1 # Set the status to 1 (warning)
    else:
        rled.value(0)
        yled.value(0)
        gled.value(1)
        status = 0 # Set the status to 0 (all good)

    return status