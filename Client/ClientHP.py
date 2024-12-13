import socket
import sys
import json, time
import os, io
from random import randint as randint
from pathlib import Path
import PySimpleGUI as sg

# Set up the GUI appearance
sg.theme('Light Yellow')
layout = [
    [sg.Text('Connection Status:')], # Label for connection status
    [sg.Text('Disconnected', key='-STATUS-', size=(20, 1), font=('Helvetica', 15))],  # Status display
    [sg.Exit(tooltip='Click to exit the program')] # Exit button
]

# Create the window with the specified layout
window = sg.Window('Client Status', layout, finalize=True)

# Check if the program is running on a Raspberry Pi
IS_RPI = Path("/etc/rpi-issue").exists() # File exists only on Raspberry Pi
print(IS_RPI) # Print whether it is running on Raspberry Pi

if (IS_RPI):
    print("Correct Hardware") 
    try:
        sock = socket. socket()
    except socket.error as err:
        print('Socket error because of %s' %(err))

# Network settings
port = 1500
address = "10.102.13.211" # IP address of the server

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
    sock.connect((address, port)) # Connect to the given IP and port
    window['-STATUS-'].update('Connected', text_color='green') # Update GUI to show connection status

    # Loop to send data 50 times
    for i in range(50):
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        
        # Gather data into a JSON object
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
    window['-STATUS-'].update('Error: Cannot resolve host', text_color='red') # Update GUI with error
    print('There an error resolving the host') # Print error message
    sock.close() # Close the socket
    
finally:
    # Clean up and close everything
    window['-STATUS-'].update('Disconnected', text_color='red') # Update GUI to show disconnection
    window.read(timeout=2000) # Keep the window open for 2 seconds
    sock.close() # Close the socket
    window.close() # Close the GUI window   
