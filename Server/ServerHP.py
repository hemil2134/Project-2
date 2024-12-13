import socket
import json, time
import PySimpleGUI as sg
from random import randint

# Unicode symbols for LED states
CIRCLE = '⚫'  # LED is ON
CIRCLE_OUTLINE = '⚪' # LED is OFF

#GUI Setup
sg.theme('Light Yellow')

# Function to create an LED display in the GUI
def LED(color, key):
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)

# Define the layout of the GUI window
layout = [
    [sg.Text('Data')],
    [sg.Multiline(
        'Waiting for data...',
        size=(50, 10),  # Size of the data display box
        justification='center',
        font=("Helvetica", 15),
        key='-OUTPUT-'  # Key to update this area later
    )],
    [sg.Text('LED Status:'), LED('Blue', '-LED-')],  # LED display
    [sg.Exit(tooltip='Click to exit the program')]  # Exit button
]

# Create the GUI window
window = sg.Window('Server Status', layout, finalize=True)

# Create a socket to communicate with the client
sock = socket.socket()
print("Socket created ... ")

port = 1500
sock.bind(('10.102.13.211', port)) # Server IP address and port
sock.listen(5) # Allow up to 5 connection requests

print('socket is listening')

# Accept a connection from the client
c, addr = sock.accept()
print('got connection from ', addr) 

def main():
    while True:
        # Check for GUI events
        event, values = window.read(timeout=100) 
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            # Exit the program if the user closes the window or clicks Exit
            print("Exiting...")
            window.close()
            break
        
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
            
            # Update the data display area in the GUI
            window['-OUTPUT-'].update(display_text)
            
            # change the LED state to ON or OFF
            window['-LED-'].update(CIRCLE if randint(1, 2) < 2 else CIRCLE_OUTLINE)
            
        except KeyError as e:
            # If a key is missing in the received JSON data, print an error message
            print("Missing key in received JSON:", e)
        
        time.sleep(1) # Wait for 1 second before repeating

# Run the main function when the script is executed
if __name__== '__main__':
    try:
        main()
        window.close()
    except KeyboardInterrupt:
        print("Bye .... ")
        window.close()
        sock.close()

