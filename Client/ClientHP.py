import socket
import sys
import json, time
import os, io
from random import randint as randint
from pathlib import Path
import PySimpleGUI as sg

from pathlib import Path

IS_RPI = Path("/etc/rpi-issue").exists() # used to check - we're using the Pi
print(IS_RPI)

if (IS_RPI):
    print("Correct Hardware")
    try:
        sock = socket. socket()
    except socket.error as err:
        print('Socket error because of %s' %(err))

port = 1500
address = "127.0.0.1"

# Function to get the CPU temperature
def measure_temp():
    t = os.popen('vcgencmd measure_temp').readline()
    temp = float(t.replace("temp=","").replace("'C\n",""))
    return temp

# Function to get core voltage
def measure_volts_core():
    v = os.popen('vcgencmd measure_volts core').readline()
    volts = float(v.replace("volt=", "").replace("volts=", "").replace("V\n", "").strip())
    return volts

# Function to get SDRAM voltage
def measure_volts_sdram_i():
    vsd = os.popen('vcgencmd measure_volts sdram_p').readline()
    vsdvolts = float(vsd.replace("volt=", "").replace("volts=", "").replace("V\n", "").strip())
    return vsdvolts

# Function to get memory allocated to the ARM CPU
def memory_arm():
    ma = os.popen('vcgencmd get_mem arm').readline()
    ma2 = float(ma.replace("arm=","").replace("M\n",""))
    return ma2

# Function to get the clock frequency of the ARM CPU
def clock_frequency_arm():
    cfa = os.popen('vcgencmd measure_clock arm').readline()
    cfa2 = float(cfa.replace("frequency(48)=",""))
    return cfa2

try:
    sock.connect((address, port))
    for i in range(50):
        jsonResult = {"temp-core":measure_temp(),
                      "volts":measure_volts_core(),
                      "sdram volts":measure_volts_sdram_i(),
                      "arm":memory_arm(),
                      "frequency":clock_frequency_arm(),
                      "it": i # Iteration count
                      }
        
        # Convert JSON object to a string
        jsonResult = json.dumps(jsonResult)
        
        # Convert JSON string to bytes for sending
        jsonbyte = bytearray(jsonResult,"UTF-8")
        sock.send(jsonbyte) # Send data to the server
        time.sleep(2) # Wait for 2 seconds before sending the next set of data

except socket.gaierror: # If there is a network error
    print('There an error resolving the host') # Print error message
    sock.close() # Close the socket
    
finally:
    # Clean up and close everything
    sock.close() # Close the socket  