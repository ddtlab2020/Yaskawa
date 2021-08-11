
import socket
import random
import time
from typing_extensions import runtime
from dx_fast_eth_server import * 
import mysql.connector

run=True

#def updateDB():
#Connect to database 
def connectToDB():   
    hostDB="remotemysql.com"
    userDB="cRW5Uykw7k"
    passwordDB="1m3XDtFGIs"
    databaseDB="cRW5Uykw7k"
    db = mysql.connector.connect(
    host=hostDB,
    user=userDB,
    password=passwordDB,
    database=databaseDB
    )
    
    return(db)

#Read first result from query
def readQuery():
    db=connectToDB()
    sql=db.cursor()
    sql.execute("SELECT * FROM besede LIMIT 1")
    query=sql.fetchone()
    
    if(query==None):
        return("")
    else:
        return(query)
            
#Clear table
def deleteAll():
    db=connectToDB()
    sql=db.cursor()
    sql.execute("DELETE FROM besede")
    db.commit()

#Delete specific row from table
def deleteQuery(id):
    db=connectToDB()
    sql=db.cursor()
    sql.execute("DELETE FROM besede WHERE id_besede="+str(id))
    db.commit()

def stop():
    global run
    run=False
    print("Stopping writing program....")

'''def checkPosition():
    position={}
    robot.read_position(position)
    return(position['pos'])'''


def start():
    global run
    #print(checkPosition())
    #Bind socket to host
    HOST="localhost"
    PORT=65433
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))

    #Connection to Yaskawa arm
    objekt=DxFastEthServer("192.168.0.81")

    print("Running writing program....")
    run=True
    deleteAll()
    while (run):
        data=readQuery()
        if(data!=""):
            besede=data[1]
            print(besede[0])
            if(ord(besede[0])>=49 and ord(besede[0])<=57 or ord(besede[0])==45):
                besede=str(besede)+'='+str(eval(besede))
            #Send individual letter to arm until string is empty
            while(len(besede)>0):
                #print(besede)
                if(str( objekt.readVar('B', 3))=="0"):
                    print(besede[0])
                    #print(ord(str(besede[0])))
                    #Some character don't have ord values (" ",'Š','Č','Ž')
                    if(besede[0]==" "):
                        print("SPACE ")
                        objekt.writeVar('B',3,194)
                        #Change B3 variable to custom number set in Yaskawa controller
                    elif(besede[0]=='Š'):
                        print("here Š",besede[0])
                        objekt.writeVar('B',3,192)
                    elif(besede[0]=='Č'):
                        print("here Č")
                        objekt.writeVar('B',3,191)
                    elif(besede[0]=='Ž'):
                        print("here Ž")
                        objekt.writeVar('B',3,193)
                    else:
                        
                        #Normal characters send ord value+100 to variable in controller (A=165,B=166,......)
                        objekt.writeVar('B',3,ord(str(besede[0]))+100)

                    #Delete character at index 0 from table row
                    besede=besede.replace(str(besede[0]),"",1)
            #Delete row when its empty
            deleteQuery(data[0])
    print("Shuting down socket....")
    s.shutdown(socket.SHUT_RDWR)
    s.close()

if __name__=="__main__":
    start()
            


                    
        
            
            
            



        



