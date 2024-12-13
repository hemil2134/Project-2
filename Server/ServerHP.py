'''This is the server, should run first, in sperarte thonny instance,
gets client (pi) data'''

import socket
import json, time

sock = socket.socket()
print("Socket created ... ")

port = 1500
#sock.bind(('', port))
sock.bind(('127.0.0.1', port)) # to run on Pi with local client
sock.listen(5)

print('socket is listening')
c, addr = sock.accept()
print('got connection from ', addr) # locks to client I.P

def main():
    while True:
        jsonReceived = c.recv(1024)
        print("Json received (byte type) -- >", jsonReceived)
        if jsonReceived == b'':
            print("Oop's")
            exit()
        data = json.loads(jsonReceived) #creates the Json string
        ret = json.dumps(data, indent=4) # makes it pretty
        ret1 = data["thing"][0]["temp"] # extracts, content of thing/temp
        ret2 = data["volts"] # extracts, content of volts
        ret3 = data["temp-core"] # extracts, content of core-temp

        print(ret1) #prints You're
        print(ret2)#prints v value
        print(ret3)#prints core value
        time.sleep(1)

if __name__== '_main_':
    try:
        main()
    except KeyboardInterrupt:
        print("Bye .... ")
        exit()
