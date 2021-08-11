
import socket
import random
import time
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
print("Running")
poteze=[1,2,3,4,5,6,7,8,9]
barve=[1,2,3]
water=1

run=True
while (run):
    if(str( objekt.readVar('B', 3))=="0"):
        if(water==1):
            objekt.writeVar('B',5,1)
            water=0 
        time.sleep(2) 
        lokacijaX=random.randint(-60,60) #-100,100
        lokacijaY=random.randint(-115,115) #-155,155
        objekt.writeVar('D', 5,lokacijaX*1000)
        objekt.writeVar('D', 6,lokacijaY*1000)
        print("LocationX: "+str(lokacijaX))
        print("LocationY: "+str(lokacijaY))
        poteza=random.choice(poteze)
        barva=random.choice(barve)
        print("Poteza "+str(poteza)+ "Barva: "+str(barva))
        objekt.writeVar('B',4,barva) 
        objekt.writeVar('B',3,poteza)
        
        





        
