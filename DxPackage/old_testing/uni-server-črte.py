
import socket
from dx_fast_eth_server import * 
HOST="localhost"
PORT=65432
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
#s.listen(10)
print("Listening ....")
#conn, addr = s.accept()
objekt=DxFastEthServer("192.168.0.81")
#self.logger.info(addr)
while True:
    while True:
        command,address = s.recvfrom(100000)
        print(str(address))
        command = str(command)
        kje = command.index("x05Key_")
        vsebina = command[kje + 1 : kje + 8][-1]
        print("Received commands: " + vsebina)
        if(vsebina=='F'):
            #FORWARD
            objekt.writeVar('B', 3, 1)
            
        elif(vsebina=='B'):
            #BACK
            objekt.writeVar('B', 3, 2)
            
        elif(vsebina=='L'):
            #LEFT
            objekt.writeVar('B', 3, 3)
            
        elif(vsebina=='R'):
            #RIGHT
            objekt.writeVar('B', 3, 4)
            
        elif(vsebina=='U'):
            #UP
            objekt.writeVar('B', 3, 5)  
            
        elif(vsebina=='D'):
            #DOWN
            objekt.writeVar('B', 3, 6)
        print(str( objekt.readVar('B', 3)))
