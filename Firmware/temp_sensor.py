import os
import board
import busio
from time import sleep
os.environ["BLINKA_MCP2221"] = "1"  # Setting environment variable


def main():
    temp_address = 0x48  # I2C address of TMP101
    lcd_address = 0x27  # I2C address of LCD
    global i2c
    i2c = busio.I2C(board.SCL, board.SDA)  # Creating I2C object
    i2c.writeto(temp_address, bytes([0x01, 0x20]), stop=False)  # Starting communication with TMP101 and setting res to 0.25
    init(lcd_address)  # Initializing the LCD
    while 1:
        temperature = read_temp(temp_address)  # Reading the temperature
        write(lcd_address, temperature)  # Writing the temperature to the LCD


def read_temp(address):
    decimals = {  # Dict for converting the binary reading with 0.25 resolution to degrees
        0: "0",
        64: "25",
        128: "5",
        192: "75"
    }
    i2c.writeto(address, bytes([0x00]), stop=False)  # Go to temp. register
    result = bytearray(2)  # Sensor returns 2 bytes
    i2c.readfrom_into(address, result)  # Read
    whole_number = result[0]
    decimal = decimals[result[1]]
    temp_measurement = str(whole_number) + str(decimal)  # Adds the readings without decimal(easier to add later)

    return temp_measurement


def init(lcd_address):
    commands = {  # All the commands used in the init stage for the LCD
      "setD": "11001000",
      "setE": "11001100",
      "4bitD": "01001000",
      "4bitE": "01001100",
      "clear1D": "00001000",
      "clear1E": "00001100",
      "clear2D": "00011000",
      "clear2E": "00011100",
      "home1D": "00001000",
      "home1E": "00001100",
      "home2D": "00101000",
      "home2E": "00101100",
      "ON1D": "00001000",
      "ON1E": "00001100",
      "ON2D": "11001000",
      "ON2E": "11001100",
    }
# LCD is used in 4-bit mode. This means i have to send the data-bytes in nibbles.
# FLow: Send data with Ena = LOW -> Send same data with Ena = HIGH -> Send data with Ena = LOW. Repeat for second nibble
# First higher nibble, then lower 

    for i in range(3):
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["setD"], 2)]), stop=False)  # Function set
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["setE"], 2)]), stop=False)
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["setD"], 2)]), stop=False)

    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["4bitD"], 2)]), stop=False)  # Set 4-bit mode
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["4bitE"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["4bitD"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["home1D"], 2)]), stop=False)  # Set cursor to (0,0)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home1D"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["home2D"], 2)]), stop=False)  # Set cursor to (0,0)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home2D"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["ON1D"], 2)]), stop=False)  # Display on
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["ON1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["ON1D"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["ON2D"], 2)]), stop=False)  # Display on
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["ON2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["ON2D"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["clear1D"], 2)]), stop=False)  # Clear the screen
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["clear1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["clear1D"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["clear2D"], 2)]), stop=False)  # Clear the screen
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["clear2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["clear2D"], 2)]), stop=False)
    sleep(0.01)


# LCD is used in 4-bit mode. This means i have to send the data-bytes in nibbles.
# FLow: Send data with Ena = LOW -> Send same data with Ena = HIGH -> Send data with Ena = LOW. Repeat for second nibble
# First higher nibble, then lower

def write(lcd_address, temperature):  # Writing the letter 'H' to the lcd
    l_nibble = {  # All lower nibbles for the numbers
        0: "0000",
        1: "0001",
        2: "0010",
        3: "0011",
        4: "0100",
        5: "0101",
        6: "0110",
        7: "0111",
        8: "1000",
        9: "1001"
    }

    commands = {  # Other commands used
        "home1D": "00001000",
        "home1E": "00001100",
        "home2D": "00101000",
        "home2E": "00101100",
        "degree1D": "11011001",
        "degree1E": "11011101",
        "degree2D": "11111001",
        "degree2E": "11111101",
        "C1D": "01001001",  # Celsius sign
        "C1E": "01001101",
        "C2D": "00111001",
        "C2E": "00111101",
        "P1D": "00101001",  # Decimal point
        "P1E": "00101101",
        "P2D": "11101001",
        "P2E": "11101101",
        "E1D": "00011001",  # Empty char used for clearing one character on lcd
        "E1E": "00011101",
        "E2D": "00111001",
        "E2E": "00111101"
    }

    h_nibble = "0011"  # Higher nibble. Same for all numbers
    Ena = "1101"  # lsb for Ena = HIGH
    Data = "1001"  # lsb for Ena = LOW

    data_byte1 = h_nibble + Data
    ena_byte1 = h_nibble + Ena

    digits = [int(d) for d in str(temperature)]  # List with all l_nibble keys
    for i in range(len(digits)):
        data_byte2 = l_nibble[digits[i]] + Data
        ena_byte2 = l_nibble[digits[i]] + Ena
        if i == 2:
            i2c.writeto(lcd_address, bytes([int(commands["P1D"], 2)]), stop=False)  # Write point as third char
            sleep(0.01)
            i2c.writeto(lcd_address, bytes([int(commands["P1E"], 2)]), stop=False)
            sleep(0.01)
            i2c.writeto(lcd_address, bytes([int(commands["P1D"], 2)]), stop=False)
            sleep(0.02)

            i2c.writeto(lcd_address, bytes([int(commands["P2D"], 2)]), stop=False)
            sleep(0.01)
            i2c.writeto(lcd_address, bytes([int(commands["P2E"], 2)]), stop=False)
            sleep(0.01)
            i2c.writeto(lcd_address, bytes([int(commands["P2D"], 2)]), stop=True)
            sleep(0.01)

        i2c.writeto(lcd_address, bytes([int(data_byte1, 2)]), stop=False)  # write temp char
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(ena_byte1, 2)]), stop=False)
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(data_byte1, 2)]), stop=False)
        sleep(0.02)

        i2c.writeto(lcd_address, bytes([int(data_byte2, 2)]), stop=False)  # write temp char
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(ena_byte2, 2)]), stop=False)
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(data_byte2, 2)]), stop=True)
        sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["degree1D"], 2)]), stop=False)  # Degree sign
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["degree1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["degree1D"], 2)]), stop=False)
    sleep(0.02)

    i2c.writeto(lcd_address, bytes([int(commands["degree2D"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["degree2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["degree2D"], 2)]), stop=True)
    sleep(0.02)

    i2c.writeto(lcd_address, bytes([int(commands["C1D"], 2)]), stop=False)  # Celsius sign
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["C1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["C1D"], 2)]), stop=False)
    sleep(0.02)

    i2c.writeto(lcd_address, bytes([int(commands["C2D"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["C2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["C2D"], 2)]), stop=True)
    sleep(0.02)

    if len(digits) == 3:
        i2c.writeto(lcd_address, bytes([int(commands["E1D"], 2)]), stop=False)  # remove extra C if just one decimal
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["E1E"], 2)]), stop=False)
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["E1D"], 2)]), stop=False)
        sleep(0.02)

        i2c.writeto(lcd_address, bytes([int(commands["E2D"], 2)]), stop=False)
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["E2E"], 2)]), stop=False)
        sleep(0.01)
        i2c.writeto(lcd_address, bytes([int(commands["E2D"], 2)]), stop=True)
        sleep(0.02)

    i2c.writeto(lcd_address, bytes([int(commands["home1D"], 2)]), stop=False)  # Set cursor to (0,0)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home1D"], 2)]), stop=False)
    sleep(0.02)

    i2c.writeto(lcd_address, bytes([int(commands["home2D"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["home2D"], 2)]), stop=False)
    sleep(0.5)


def error(lcd_address):  # turn off lcd if error
    commands = {
        "OFF1D": "00001000",
        "OFF1E": "00001100",
        "OFF2D": "00001000",
        "OFF2E": "00001100",
    }

    i2c.writeto(lcd_address, bytes([int(commands["OFF1D"], 2)]), stop=False)  # Display on
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["OFF1E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["OFF1D"], 2)]), stop=False)
    sleep(0.01)

    i2c.writeto(lcd_address, bytes([int(commands["OFF2D"], 2)]), stop=False)  # Display on
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["OFF2E"], 2)]), stop=False)
    sleep(0.01)
    i2c.writeto(lcd_address, bytes([int(commands["OFF2D"], 2)]), stop=True)
    sleep(0.01)


main()
