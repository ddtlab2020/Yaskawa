
import socket
import random
import time
from dx_fast_eth_server import * 

run=True

def stop():
    global run
    run=False
    print("Stopping painting BCI program....")

def start():
    global run
    HOST="localhost"
    PORT=65432
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    #s.listen(10)
    print("Listening ....")
    #conn, addr = s.accept()
    objekt=DxFastEthServer("192.168.0.81")
    #self.logger.info(addr)
    print("Running painting BCI program....")
    run=True
    water=1
    while (run):
        while(run):
            #
            command,address = s.recvfrom(100000)
            print(str(address))
            command = str(command)
            print(command)
            
            kje = command.index("x06Key_")
            vsebina = command[kje+7:kje+9]
            print("Received commands: " + vsebina)
            lokacijaX=random.randint(-60,60) #-100,100
            lokacijaY=random.randint(-115,115) #-155,155
            objekt.writeVar('D', 5,lokacijaX*1000)
            objekt.writeVar('D', 6,lokacijaY*1000)
            print("LocationX: "+str(lokacijaX))
            print("LocationY: "+str(lokacijaY))
            
            if(water==1):
                #objekt.writeVar('B',5,1)
                water=0
            if(vsebina=='0S'):
                objekt.writeVar('B',4,4)
                objekt.writeVar('B',3,11)
            if(vsebina[1]=='R'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,int(vsebina[0]))
            elif(vsebina[1]=='Y'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,int(vsebina[0]))
            elif(vsebina[1]=='B'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,int(vsebina[0]))
            water=1
    print("Shutting down socket....")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
        
if __name__=="__main__":
    start()




        
