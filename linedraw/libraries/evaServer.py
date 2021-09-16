import socket

def sendMessage():
    clientSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    clientSocket.connect(("192.168.1.38",65432))
    data="test"
    clientSocket.send(data.encode())
    clientSocket.close()



if __name__=='__main__':
    sendMessage