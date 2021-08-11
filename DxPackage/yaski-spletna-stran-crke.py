
import socket
import random
import time
from dx_fast_eth_server import * 
import mysql.connector



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



#Bind socket to host
HOST="localhost"
PORT=65432
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
print("Listening ....")

#Connection to Yaskawa arm
objekt=DxFastEthServer("192.168.0.81")

print("Running")
run=True
deleteAll()
while (run):
    data=readQuery()
    
    if(data!=""):
        
        besede=data[1]
        #Send individual letter to arm until string is empty
        while(len(besede)>0):
            #print(besede)
            if(str( objekt.readVar('B', 3))=="0"):
                #print(ord(str(besede[0])))
                #Some character don't have ord values (" ",'Š','Č','Ž')
                if(besede[0]==" "):
                    print("here empty")
                    objekt.writeVar('B',3,100)
                    #Change B3 variable to custom number set in Yaskawa controller
                elif(besede[0]=='Š'):
                    print("here Š",besede[0])
                    objekt.writeVar('B',3,100)
                elif(besede[0]=='Č'):
                    print("here Č")
                    objekt.writeVar('B',3,100)
                elif(besede[0]=='Ž'):
                    print("here Ž")
                    objekt.writeVar('B',3,100)
                else:
                    print(ord(str(besede[0]))+100)
                    #Normal characters send ord value+100 to variable in controller (A=165,B=166,......)
                    objekt.writeVar('B',3,ord(str(besede[0]))+100)

                #Delete character at index 0 from table row
                besede=besede.replace(str(besede[0]),"",1)
        #Delete row when its empty
        deleteQuery(data[0])
           


                    
        
            
            
            



        



