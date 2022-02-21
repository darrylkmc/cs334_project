import socket
import time
import random

robotIP = '172.24.184.219'
port = 3310

#####################################################################
#STEP 2
#####################################################################
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((robotIP,port))

data = 'shri98'
s1.send(data.encode())


#####################################################################
#STEP 3
#####################################################################
iTCPPort2Connect = s1.recv(100).decode()
iTCPPort2Connect = int(iTCPPort2Connect)

print("TCP <%d> accepted." %iTCPPort2Connect)


listenPort = iTCPPort2Connect

# Create a TCP socket to listen connection
print("Creating TCP socket...")
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((robotIP, listenPort))
listenSocket.listen(5)
print("Done")

s2, address = listenSocket.accept()
robotIP = address[0]
print("\nClient from %s at port %d connected" %(robotIP,address[1]))

s1.close()
listenSocket.close()

#####################################################################
#STEP 4
#####################################################################
ports_to_send = s2.recv(100).decode()

ports_to_send = tuple(map(int, ports_to_send.split(',')))
iUDPPortRobot = int(ports_to_send[0])
iUDPPortStudent = int(ports_to_send[1])
x = str(random.randint(6,9))

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('',iUDPPortStudent)
s3.bind(addr)

s3.sendto(x.encode(),(robotIP,iUDPPortRobot))

print("\nReceiving UDP packet:")
message, address = s3.recvfrom(100)

print("Received: ", message)

s2.close()

#####################################################################
#STEP 5
#####################################################################
print("\nResending UDP packet to robot:")

for i in range(0,5):
    s3.sendto(message,(robotIP,iUDPPortRobot))
    time.sleep(1)
    print("UDP packet %d sent" %(i+1))

s3.close()
    

