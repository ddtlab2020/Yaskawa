
import socket
from dx_fast_eth_server import * 
import time
print("Listening ....")
objekt=DxFastEthServer("192.168.0.81")
vsebina="DDTLAB"
while True:
    while True:
        for i in vsebina:        
            if(i=='Č'):
                objekt.writeVar('B', 3, 191)
            else:
                objekt.writeVar('B', 3, ord(i) + 100)
            print(str( objekt.readVar('B', 3)))
            print("Successful writing")
            
            time.sleep(6)
