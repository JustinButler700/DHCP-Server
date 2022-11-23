#!/usr/bin/env python3
import socket
from ipaddress import IPv4Interface
from datetime import datetime, timedelta

# Time operations in python
# isotimestring = datetime.now().isoformat()
# timestamp = datetime.fromisoformat(isotimestring)
# 60secfromnow = timestamp + timedelta(seconds=60)

# List containing all available IP addresses as strings
ip_addresses = [ip.exploded for ip in IPv4Interface("192.168.45.0/28").network.hosts()]
records = {} #Holds unique Mac's mapped to IPs
acks = {} #Holds the Ip's which have been acked
currentMac = ''
time = {} #holds time
index = 0 #counts every unique message
ipIndex = -1 #counts every unique ip
isdeclined = False
#Generates a new IP address
def newIp(): 
  global ipIndex
  if ipIndex <= len(ip_addresses):
    ipIndex += 1
    return str(ip_addresses[ipIndex])
  else:
    ipIndex = 0
    return 0
  pass

def newTime():
  isotimestring = datetime.now().isoformat()
  timestamp = datetime.fromisoformat(isotimestring)
  return timestamp
  pass
  
def offer():
  #Offer generates a new IP, so now we set it in the record
    return ('OFFER '+ str(currentMac) +' '+ str(records[currentMac]) +' '+ str(time.setdefault(currentMac,newTime())))
    pass
  
def decline():
    return ('DECLINE '+ str(currentMac) +' '+ str(records.setdefault(currentMac,newIp())) +' '+ str(time.setdefault(currentMac,newTime())))
    pass
  
def aknowledge():
    if(ipIndex != len(ip_addresses)-1):
        acks[currentMac]=True
        time[currentMac] = newTime()
        return ('ACKNOWLEDGE '+ str(currentMac) +' '+ str(records[currentMac]) +' '+ str(time.setdefault(currentMac,newTime())))
    else:
      return decline()
    pass
  
def list():
    print('list to Admin: ')
    tempMsg = ''
    count = 0
    for i in records.keys():
      tempMsg += ('IP: '+ str(records[i]))
      tempMsg += (' MAC:' + str(i)+' ')
      tempMsg += (' ACKED: ' + str(acks.setdefault(i,False)) + ' ')  
      tempMsg += (' EXPIRATION: ' + str(time.setdefault(i,newTime())+ timedelta(seconds=60))+'\n')
      if tempMsg and acks[i]:
          print('Server Sent -> '+tempMsg)
          server.sendto(tempMsg.encode(), clientAddress)
          count +=1
      tempMsg = ''
    if count == 0:
      server.sendto('CLIENTS HAVE RELEASED IPS / NO CLIENTS'.encode(), clientAddress)
    pass

def release():
    if (records.__contains__(currentMac)) and acks[currentMac]:
        time[currentMac] = newTime()
        acks[currentMac] = False
        return 'released'
    elif records.__contains__(currentMac):
      return 'alreadyreleased'
    else:
      pass
def renew():
  if records.__contains__(currentMac):
    time[currentMac] = newTime()
    return aknowledge()
  else:
    myIP = newIp()
    if(myIP != 0):
      time[currentMac] = newTime()
      records[currentMac] = myIP
      return aknowledge()
    else:
      global isdeclined
      acks[currentMac] = False
      isdeclined = True
      return decline()
    
  pass
# Calculate response based on message
def dhcp_operation(parsed_message):
    nextMsg = ''
    print('Server Sending -> ',end="")
    if parsed_message == 'LIST':
        list()
    elif parsed_message == 'DISCOVER':
        nextMsg = offer()
    elif parsed_message == "REQUEST":
        nextMsg = aknowledge()
    elif parsed_message == "LIST":
        list()
        nextMsg = ''
    elif parsed_message == "RELEASE":
        nextMsg = release()
    elif parsed_message == "RENEW":
        nextMsg = renew()
    return nextMsg


# Start a UDP server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid TIME_WAIT socket lock [DO NOT REMOVE]
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", 9000))
print("DHCP Server running...")

try:
    while True:
        global clientAddress
        isdeclined = False
        message, clientAddress = server.recvfrom(4096)
        print('Server Recieved <- ', end="")
        print(message.decode())
        myList = message.decode().split()
        for i in range(len(myList)):
            if(i == 1 and myList[i]):
              currentMac = myList[i]
              records.setdefault(myList[i], newIp())
        #we can ignore ip since they are already established
          
        response = dhcp_operation(myList[0])
        if myList[0] == "OFFER":
            index+=1
        server.sendto(response.encode(), clientAddress)
        if isdeclined:
          server.sendto(offer.encode(), clientAddress)
        print(response)   #not printing list str
except OSError:
    print('OS Error')
    pass
except KeyboardInterrupt:
    print('Keyboard Interrupt')
    pass

server.close()
