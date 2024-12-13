import socket
import sys
import json, time
import os, io

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
#address = "192.168.10.121" # of server, so we can read the vcgencmd data
address = "127.0.0.1"# to run on Pi with local server

try:
    sock.connect((address, port))
    for i in range(10):
        v = os.popen('vcgencmd measure_volts ain1').readline() #gets from the os, using vcgencmd - the core-voltage
        core = os.popen('vcgencmd measure_temp').readline() #gets from the os, using vcgencmd - the core-temperature

        jsonResult = {"thing": [{"temp":"You're"}], "volts":v, "temp-core":core, "it =": i}

        jsonResult = json.dumps(jsonResult)

        jsonbyte = bytearray(jsonResult,"UTF-8")
        print("this Json byte, sent ->", jsonbyte)

        print(v, " it = ",i, " ",core)
        #sock. send(jsonResult)
        sock.send(jsonbyte)
        time.sleep(5)

except socket.gaierror: # = short form for getaddrinfo()

    print('There an error resolving the host')
    sock.close()
finally:
    print("Sorry lost connection with server")
    exit()
