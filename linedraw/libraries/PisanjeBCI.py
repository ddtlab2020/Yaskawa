
import socket
from dx_fast_eth_server import * 

run=True
def stop():
    global run
    print("Stopping writing BCI program....")
    run=False

def start():
    global run
    HOST="localhost"
    PORT=65432
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    #s.listen(10)
    #print("Listening ....")
    #conn, addr = s.accept()
    objekt=DxFastEthServer("192.168.0.81")
    print("Running writing BCI program....")
    #self.logger.info(addr)
    run=True
    while run:
        while run:
            command,address = s.recvfrom(100000)
            #print(str(address))
            command = str(command)
            
            kje = command.index("x06Key_")
            vsebina = command[kje + 1 : kje + 8][-1]
            print("Received commands: " + vsebina)
            if(vsebina=='Č'):
                objekt.writeVar('B', 3, 191)
            else:
                objekt.writeVar('B', 3, ord(vsebina) + 100)
            print(str( objekt.readVar('B', 3)))
    
    print("Shutting down socket....")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
            
if __name__=="__main__":
    start()




    


        
