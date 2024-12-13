'''This is the server, should run first, in sperarte thonny instance,
gets client (pi) data'''

import socket
import json, time
import PySimpleGUI as sg
from random import randint

sock = socket.socket()
print("Socket created ... ")

port = 1500
sock.bind(('127.0.0.1', port)) # to run on Pi with local client
sock.listen(5)

print('socket is listening')
c, addr = sock.accept()
print('got connection from ', addr) # locks to client I.P

def main():
    while True:
        # Receive data from the client
        jsonReceived = c.recv(1024)
        if not jsonReceived: # If no data is received
            print("Sorry lost connection with Client")
            break
        
        try:
            # Convert the received data from JSON format to Python dictionary
            data = json.loads(jsonReceived)
            
            # Extract data values from the dictionary
            it2 = data.get("it")
            temp = data.get("temp-core") 
            volts = data.get("volts")  
            sdram_volts = data.get("sdram volts")  
            arm_memory = data.get("arm")  
            frequency = data.get("frequency")  
            
            # Format the data for display
            display_text = (
                f"Iteration: {it2}\n"
                f"Core Temp: {temp} C\n"
                f"Core Voltage: {volts} V\n"
                f"SDRAM Voltage: {sdram_volts} V\n"
                f"ARM Memory: {arm_memory} MB\n"
                f"ARM Frequency: {frequency} Hz\n"
            )
            
        except KeyError as e:
            # If a key is missing in the received JSON data, print an error message
            print("Missing key in received JSON:", e)
        
        time.sleep(1) # Wait for 1 second before repeating

# Run the main function when the script is executed
if __name__== '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye .... ")
        sock.close()
