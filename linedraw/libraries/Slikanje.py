
import socket
import random
import time
from dx_fast_eth_server import * 

import mysql.connector

run=True

def readQuery():
    db = mysql.connector.connect(
    host="remotemysql.com",
    user="cRW5Uykw7k",
    password="1m3XDtFGIs",
    database="cRW5Uykw7k"
    )
    sql=db.cursor()
    
    sql.execute("SELECT * FROM poteze LIMIT 1")
    query=sql.fetchone()
    if(query==None):
        return("")
    else:
        return(query)
        
    
def deleteAll():
    db = mysql.connector.connect(
    host="remotemysql.com",
    user="cRW5Uykw7k",
    password="1m3XDtFGIs",
    database="cRW5Uykw7k"
    )
    sql=db.cursor()
    sql.execute("DELETE FROM poteze")
    db.commit()

def deleteQuery(id):
    db = mysql.connector.connect(
    host="remotemysql.com",
    user="cRW5Uykw7k",
    password="1m3XDtFGIs",
    database="cRW5Uykw7k"
    )
    sql=db.cursor()
    sql.execute("DELETE FROM poteze WHERE idPoteze="+str(id))
    db.commit()

def stop():
    global run
    run=False
    print("Stopping painting program....")
    

def start(): 
    global run       
    HOST="localhost"
    
    PORT=65432
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
   
    objekt=DxFastEthServer("192.168.0.81")
    #self.logger.info(addr)
    print("Running painting program....")
    water=1
    run=True
    deleteAll()
    
    while(run):
        data=readQuery()
        if(str( objekt.readVar('B', 3))=="0" and data!=""):
            if(water==1):
                objekt.writeVar('B',5,1)
                water=0 
            if(len(str(data[1]))>2):
                deleteQuery(data[0])
            else:
                lokacijaX=data[2] #-100,100
                lokacijaY=data[3] #-155,155
                objekt.writeVar('D', 5,int(lokacijaX)*1000)
                objekt.writeVar('D', 6,int(lokacijaY)*1000)
                print("LocationX: "+str(lokacijaX))
                print("LocationY: "+str(lokacijaY))
            
                print("Poteza "+str(data[1][0])+ " Barva: "+str(data[1][1]))
                print("-----------------------")
                if(data[1][1]=='R'):
                    objekt.writeVar('B',4,1)
                    objekt.writeVar('B',3,int(data[1][0]))
                    deleteQuery(data[0])

                elif(data[1][1]=='Y'):
                    objekt.writeVar('B',4,2)
                    objekt.writeVar('B',3,int(data[1][0]))
                    deleteQuery(data[0])
                    
                elif(data[1][1]=='B'):
                    objekt.writeVar('B',4,3)
                    objekt.writeVar('B',3,int(data[1][0]))
                    deleteQuery(data[0])

    print("Shutting down socket....")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
        
if __name__=="__main__":
    start()