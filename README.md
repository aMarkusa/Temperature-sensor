# Temperature-sensor
<img src="https://user-images.githubusercontent.com/83133831/193098295-48000a53-1d1a-4c58-ba3d-38c6667dbdef.jpg" width="300" height="236"><img src="https://user-images.githubusercontent.com/83133831/193100037-602079ae-ad3d-472c-a1f7-1796f2eac732.jpg" width="503" height="236">

## Description
Breakout board for temperature sensor.
The board is powered directly through micro-USB. The host PC communicates with the temperature sensor through a USB to I2C converter. 
A python script (implemented with micropython) running on the host PC reads the temperature from the sensor, and displays it on the I2C-LCD.

### PCB
PCD designed in KiCad and ordered from JLCPCB. Design files in project repository.

### BOM
- USB3075-30-A micro-USB connector
- MCP2221A USB to I2C converter
- TMP101 temperature sensor
- 3x 5k resistor
- 2x 470nF capacitor
- 1x 10nF capacitor
- 2.54mm pinheaders


## Reflections
This was a really fun project, as the hardware was quite simple and I had to put more emphasis on the software. 
The end product is not that practical as it requires a PC to run the script, but I got to learn more about digital electronics through this project.  
The most labour-intensive part was displaying the temperature values on the display. Becaues I made the decision to not use any libraries for this, I had to dig into how the LCD-logic works,
 and which bytes correspond to which characters. 
