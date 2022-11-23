#!/usr/bin/env python3
import uuid
import socket
import sys 
from datetime import datetime, timedelta

# Time operations in python
# timestamp = datetime.fromisoformat(isotimestring)

# Extract local MAC address [DO NOT CHANGE]
MAC = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1]).upper()

# SERVER IP AND PORT NUMBER [DO NOT CHANGE VAR NAMES]
SERVER_IP = "10.0.0.100"
SERVER_PORT = 9000
Time = '0'
isotimestring = datetime.now().isoformat()
timestamp = datetime.fromisoformat(isotimestring)
exp = timestamp +timedelta(seconds = 60)


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def quit():
    print('Good bye!')
    clientSocket.close()
    sys.exit()

def release(MAC, SERVER_IP, Time):
    message = 'RELEASE' +' '+ MAC +' '+ SERVER_IP +' '+ Time
    clientSocket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

def renew(MAC, SERVER_IP, Time):
    if (datetime.fromisoformat(datetime.now().isoformat()) > exp):
        message = "DISCOVER " + MAC 
    else:
        message = 'RENEW' +' '+ MAC +' '+ SERVER_IP +' '+ Time
    print('Client sending -> ' + message)
    clientSocket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))


# Sending DISCOVER message
message = "DISCOVER " + MAC
print('client sending -> '+ message)
clientSocket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

while True:
    # LISTENING FOR RESPONSE
    message, _ = clientSocket.recvfrom(7000)
    #print(message.decode())

    decodedMessage = message.decode()
    myList = decodedMessage.split()

    if myList[0] == 'DECLINE': #check if declined
        print('Declined!')
        print(decodedMessage)
    
    elif myList[0] == 'OFFER':
        print('Client Recieved <-- ', end="")
        print(decodedMessage)
        receivedMac = myList[1]
        if receivedMac != MAC:
            print('Wrong macAddress!')
            print('My macAddress is: ' + MAC)
            print('Provided macAddress is: '+ receivedMac)
        else:
            ip = myList[2]
            #print(myList[4]) #debug
            Message = 'REQUEST' + ' '+MAC+ ' '+ ip + ' '+ myList[3] + ' '+ myList[4]
            print('Client Sending -> '+ Message)
            clientSocket.sendto(Message.encode(), (SERVER_IP, SERVER_PORT))


    elif myList[0] == 'ACKNOWLEDGE':
        print('Server Recieved <- '+decodedMessage)
        receivedMAC = myList[1]
        if receivedMAC != MAC:
            print('Wrong Mac Address')
            print('My macAddress is: ' + MAC)
            print('Provided Mac Address: ' + receivedMAC)
        else:
            ip = myList[2]
            Time = myList[3] + ' '+myList[4]
            print('... Address ' + ip + ' has been assigned to this client. ', end="")
            print('TTL: ' + str(datetime.fromisoformat(Time)+timedelta(seconds = 60)))
            
    
            userChoice = input("Choose an Option: 1: Release, 2: Renew, 3: Quit")
            if userChoice == '1':
              print('Release Selected')
              release(MAC, SERVER_IP, Time)
            elif userChoice == '2':
              print('Renew Selected')
              renew(MAC, SERVER_IP, Time)
            elif userChoice == '3':
              quit()
    else:
        userChoice = input("Choose an Option: 1: Release, 2: Renew, 3: Quit\n")
        if userChoice == '1':
              print('Release Selected')
              release(MAC, SERVER_IP, Time)
        elif userChoice == '2':
              print('Renew Selected')
              renew(MAC, SERVER_IP, Time)
        elif userChoice == '3':
            quit()
  

