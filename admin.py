#!/usr/bin/env python3
import uuid
import socket
from datetime import datetime, timedelta

# Time operations in python
# timestamp = datetime.fromisoformat(isotimestring)

# Extract local MAC address [DO NOT CHANGE]
MAC = ":".join(["{:02x}".format((uuid.getnode() >> ele) & 0xFF) for ele in range(0, 8 * 6, 8)][::-1]).upper()

# SERVER IP AND PORT NUMBER [DO NOT CHANGE VAR NAMES]
SERVER_IP = "10.0.0.100"
SERVER_PORT = 9000

isotimestring = datetime.now().isoformat()
timestamp = datetime.fromisoformat(isotimestring)

adminSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sentMessage = 'LIST '
print('Admin Sending -> '+ sentMessage)
adminSocket.sendto(sentMessage.encode(), (SERVER_IP, SERVER_PORT))

while True:
    # LISTENING FOR RESPONSE
    message, _ = adminSocket.recvfrom(7000)
    #print(message.decode())
    decodedMessage = message.decode()
    if decodedMessage != '':
      print('Admin Received <- '+decodedMessage)
adminSocket.close()