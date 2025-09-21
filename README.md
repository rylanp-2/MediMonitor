# MediMonitor
> An ENGR 120 Project developed and presented by Rylan, Riley and Theo in the spring 2025 academic term.

## About the Project
This was developed by the the three of us for a class project
We were required to use a Raspberry Pi Pico microcontroller to build a proof-of-concept smart device to modernize hospitals in BC. We needed to use at least three sensors, one physical acutator, and an interactive web interface.

These parameters resulted in our creation of **MediMonitor**, a device that accurately reads the temperature and humidity (through a DHT11 temperature and humidity sensor and two thermistors) in medication refrigerators. The device sends this live data to the web-UI, which allows the user to configure the desired temperature for the storage of any applicable medicine, and a status history is displayed so the integrity of the medicine can be accurately assessed.

The states of the device are stored in flash memory, allowing it to be recovered in any event of power failure.

![See here for schematic design.](.github/Schematic.pdf)

### Project Distribution
Each aspect of the design and implementation was developed by all three members, however each member had a focus:
- **Riley:** Web-UI design and function, Server-Client communications, Device configuration
- **Rylan:** Server-side hardware interactions, Hardware implementation
- **Theo:** Server-side hardware interactions, Hardware design, File IO/logging

Additionally, each team member:
- Provided support for each other
- Collaborated on group presentation/reports
- Contributed to each aspect of the design process

## Important Note
All commits to the repository were done by "Tinklman," which was Riley on his computer, as he was tracking all changes to the code. Instead of a shared git repository, files were shared using a syncthing directory and through the Raspberry Pi itself.


