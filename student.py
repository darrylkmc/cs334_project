#MY NAME: Darryl McIntosh, MY PARTNER: Shrijan Pant

import socket
import time
import random

robotIP = '172.24.184.219'
port = 3310

#####################################################################
#STEP 2
#####################################################################

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#connect to ROBOT TCP Port 3310
s1.connect((robotIP,port))

#send blazerid
data = 'shri98'
print("\nSending BlazerID...")
s1.send(data.encode())
time.sleep(1)
print("BlazerID sent")


#####################################################################
#STEP 3
#####################################################################

#receive TCP port from robot for new connection
iTCPPort2Connect = s1.recv(100).decode()
iTCPPort2Connect = int(iTCPPort2Connect)

print("\nTCP <%d> accepted." %iTCPPort2Connect)

listenPort = iTCPPort2Connect

# Create a TCP socket to listen connection
print("\nCreating TCP listen socket...")
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind(('', listenPort))
listenSocket.listen(5)
print("Done")

# Accept connection from robot and create a new socket
s2, address = listenSocket.accept()
robotIP = address[0]
print("\nClient from %s at port %d connected" %(robotIP,address[1]))

s1.close()
listenSocket.close()

#####################################################################
#STEP 4
#####################################################################

#receive UDP ports from robot
ports_to_send = s2.recv(100).decode()

ports_to_send = tuple(map(int, ports_to_send.split(',')))
iUDPPortRobot = int(ports_to_send[0])
iUDPPortStudent = int(ports_to_send[1])

#generate an integer between 5 and 10, exclusive
x = str(random.randint(6,9))

#create UDP socket 
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('',iUDPPortStudent)
s3.bind(addr)

#send x to robot
s3.sendto(x.encode(),(robotIP,iUDPPortRobot))

#receive message from robot
print("\nReceiving UDP packet:")
message, address = s3.recvfrom(100)
print("Received: ", message.decode())

s2.close()

#####################################################################
#STEP 5
#####################################################################

#send message back to robot
print("\nResending UDP packet to robot:")

for i in range(0,5):
    s3.sendto(message,(robotIP,iUDPPortRobot))
    time.sleep(1)
    print("UDP packet %d sent" %(i+1))

s3.close()
exit(1)
    

