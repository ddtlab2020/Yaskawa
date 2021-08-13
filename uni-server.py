
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
        if(vsebina=='Č'):
            objekt.writeVar('B', 3, 191)
        else:
            objekt.writeVar('B', 3, ord(vsebina) + 100)
        print(str( objekt.readVar('B', 3)))





    


        
