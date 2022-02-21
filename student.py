import socket
import time
import random

host = '172.24.184.219'
port = 3310

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host,port))

data = 'darrylmc'
s.send(data.encode())

iTCPPort2Connect = s.recv(100)

print("TCP <%s> accepted." %iTCPPort2Connect.decode())
iTCPPort2Connect = int(iTCPPort2Connect.decode())

listenPort = iTCPPort2Connect

# Create a TCP socket to listen connection
print("Creating TCP socket...")
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((host, listenPort))
listenSocket.listen(5)
print("Done")

s.close()

# accept connections from outside, a new socket is constructed
s1, address = listenSocket.accept()
robotIP = address[0]
print("\nClient from %s at port %d connected" %(robotIP,address[1]))
# Close the listen socket
# Usually you can use a loop to accept new connections
listenSocket.close()

ports_to_send = s1.recv(100).decode()

s1.close()

ports_to_send = tuple(map(int, ports_to_send.split(',')))
iUDPPortRobot = int(ports_to_send[0])
iUDPPortStudent = int(ports_to_send[1])
x = str(random.randint(6,9))

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('',iUDPPortStudent)
s3.bind(addr)

s3.sendto(x.encode(),(robotIP,iUDPPortRobot))

print("\nReceiving UDP packet:")
message, address = s3.recvfrom(int(x)*10)

print("Received: ", message)

print("\nSending UDP packet:")

for i in range(0,5):
    s3.sendto(message,(robotIP,iUDPPortRobot))
    time.sleep(1)
    print("UDP packet %d sent" %(i+1))

s3.close()
    

