

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
niz=""
#self.logger.info(addr)
while True:
    while True:
        command,address = s.recvfrom(10000)
        
        print(str(address))
        command = str(command)
        kje = command.index("x05Key_")
        vsebina = command[kje + 1 : kje + 8][-1]
        print("Received commands: " + vsebina)
        niz+=vsebina
        if(vsebina=="*" and len(niz)>1):
            i=0
            while(i<=len(niz)-1):
                if(objekt.readVar('B',3)==0):
                    objekt.writeVar('B', 3, ord(i) + 100)
                    print(objekt.readVar('B', 3))
                    i+=1
            niz=""

        
        




