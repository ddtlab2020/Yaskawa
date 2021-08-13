-
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
red=[]
yellow=[]
blue=[]
stroke1=['1','Q','W']
stroke2=['2','E','R']
stroke3=['3','T','Z']
stroke4=['4','U','I']
stroke5=['5','O','P']
stroke6=['6','A','S']
stroke7=['7','D','F']
stroke8=['8','G','H']
stroke9=['9','J','K']
stroke10='L'


water=1
while (True):
    while(True):
        #command[kje+7:kje+9]
        command,address = s.recvfrom(100000)
        print(str(address))
        command = str(command)
        kje = command.index("x05Key_")
        vsebina = command[kje + 1 : kje + 8][-1]
        print("Received commands: " + vsebina)
        lokacijaX=random.randint(-60,60) #-100,100
        lokacijaY=random.randint(-115,115) #-155,155
        objekt.writeVar('D', 5,lokacijaX*1000)
        objekt.writeVar('D', 6,lokacijaY*1000)
        print("LocationX: "+str(lokacijaX))
        print("LocationY: "+str(lokacijaY))
        
        if(water==1):
            objekt.writeVar('B',5,1)
            water=0
         if(vsebina=='Y'):
             objekt.writeVar('B',4,4)

        if(vsebina in stroke1):
            if(vsebina=='1'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,1)
            elif(vsebina=='Q'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,1)
            elif(vsebina=='W'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,1)
        
        if(vsebina in stroke2):
            if(vsebina=='2'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,2)
            elif(vsebina=='E'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,2)
            elif(vsebina=='R'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,2)
            
        if(vsebina in stroke3):
            if(vsebina=='3'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,3)
            elif(vsebina=='T'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,3)
            elif(vsebina=='Z'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,3)  
        
        if(vsebina in stroke4):
            if(vsebina=='4'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,4)
            elif(vsebina=='U'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,4)
            elif(vsebina=='I'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,4)
        
        if(vsebina in stroke5):
            if(vsebina=='5'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,5)
            elif(vsebina=='O'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,5)
            elif(vsebina=='P'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,5)

        if(vsebina in stroke6):
            if(vsebina=='6'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,6)
            elif(vsebina=='A'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,6)
            elif(vsebina=='S'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,6)
        
        if(vsebina in stroke7):
            if(vsebina=='7'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,7)
            elif(vsebina=='D'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,7)
            elif(vsebina=='F'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,7)
        
        if(vsebina in stroke8):
            if(vsebina=='8'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,8)
            elif(vsebina=='G'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,8)
            elif(vsebina=='H'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,8)
        
        if(vsebina in stroke9):
            if(vsebina=='9'):
                objekt.writeVar('B',4,1)
                objekt.writeVar('B',3,9)
            elif(vsebina=='J'):
                objekt.writeVar('B',4,2)
                objekt.writeVar('B',3,9)
            elif(vsebina=='K'):
                objekt.writeVar('B',4,3)
                objekt.writeVar('B',3,9)
        water=1
        






        
