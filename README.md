# MediMonitor
> An ENGR 120 Project developed and presented by Riley, Rylan and Theo in the fall of 2024.

## About the Project
This was developed in tandem by the the three of us for a class project. The only requirements were as below:
1. Use the RPi Pico W microcontroller, and implement server code in MicroPython
2. Use (at minimum) three sensors for physical data, and three physical actuators
3. Allow the user to interact with the device remotely through a web-based interface
4. Respond to an hypothetical request for prototypes by HealthBC as a tech company
   - In this scenario, HealthBC was requesting a device to modernize aging BC hospital infrastructure; the device could implement new systems or layer ontop of exisiting tools

These parameters resulted in our creation of **MediMonitor**, a device that accurately reads the temperature (through a DHT11, and two thermistors), along with humidity for usage in medical storage cabnetry.  The device then sends this live data to the web-UI, which allows the user to configure the desired temperature for the storage of any applicable medicine. The device then saves these values, and reports a history of the temperature falling outside the desired range. The history is easily accessible through the web-UI.

The states of the device are stored in flash memory, allowing it to be recovered in any event of power failure.

![See here for schematic design.](.github/Schematic.pdf)

### Project Distribution
Each aspect of the design and implementation was developed in tandem by all members, however the designated roles of the team were what was mostly worked on by each member:
- **Riley:** Web-UI design and function, Server-Client communications, Device configuration
- **Rylan:** Server-sided hardware interactions, Hardware implementation
- **Theo:** Server-sided hardware interactions, Hardware design, File IO/logging

Additionally, each team member:
- Provided support for the roles stated above beyond their designanted person
- Collaborated on group presentation/reports
- Contributed to each aspect of the design process

## Important Note
All commits to the repository were done by "Tinklman". This was Riley's user on his computer, as he was tracking all changes to the code. **This does not mean he did all the work.** Instead of a shared git repository, files were shared with a shared syncthing directory, or through the Raspberry Pi itself.

The current state of the repository reflects that of the current memory of the Raspberry Pi Pico W, minus dotfiles and the README. 
