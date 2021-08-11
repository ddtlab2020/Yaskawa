# coding=utf-8


class UdpPacket():
    """
    UdpPacket
    Abstract class represent packet structure used in communication protocol between dx server and
    client application
    """
    def __init__(self, procDiv=1):
        """
        constructor method
        :return:            None
        """
        self.identifier = 'YERC'        #Identifier         4 Byte      (fixed to YERC)
        self.headSize = [0x20, 0x00]    #Header part size   2 Byte      Size of header part (fixed to 0x20)
        self.dataSize = [0x00, 0x00]    #Data part size     2 Byte      Size of data part (variable)
        self.reserve1 = 3               #Reserve 1          1 Byte      Fixed to “3”
        self.procDiv = procDiv          #Processing div     1 Byte      1: robot control, 2: file control
        self.ACK = 0                    #ACK                1 Byte      0: Request, 1: Other than request
        self.reqID = 0                  #Request ID         1 Byte      Identifying ID for command session
                                                                        # (increment this ID every time the client side outputs a
                                                                        # command. In reply to this, server side answers the received
                                                                        # value.)
        self.blockNo = [0, 0, 0, 0]     #Block No.          4 Byte      Request: 0
                                                                        # Answer: add 0x8000_0000 to the last packet.
                                                                        # Data transmission other than above: add 1
                                                                        # (max: 0x7fff_ffff)
        self.reserve2 = 99999999      #Reserve 2          8 Byte      Fixed to “99999999”


    def sizeData(self):
        return (self.dataSize[1] * 256 + self.dataSize[0] )

class UdpPacket_Req(UdpPacket):
    def __init__(self, subHeader, data=[]):
        """
        constructor method
        :param subHeader:   sub header part of packet ( depend on each request/answer )
        :param data:        data part of the packet ( optional, depend of the request/answer )
        :return:            None
        """
        UdpPacket.__init__(self)
        self.procDiv = subHeader ['procDiv']
        self.cmdNo = subHeader['cmdNo']
        self.inst = subHeader['inst']
        self.attr = subHeader['attr']
        self.service = subHeader['service']
        self.padding = subHeader['padding']

        self.dataSize[0]=len(data)
        self.data=data


    def special(self):
        """
        :return: string representation of the packet
        """
        #Prepare request packet
        # Identifier 4 Byte Fixed to “YERC”
        #Header part size 2Byte Size of header part (fixed to 0x20)
        #Data part size 2Byte Size of data part (variable)
        #Reserve 1 1Byte Fixed to “3”
        #Processing division 1Byte 1: robot control, 2: file control
        #ACK 1Byte 0: Reques 1: Other than request
        #Request ID 1Byte Identifying ID for command session
        #(increment this ID every time the client side outputs a
        #command. In reply to this, server side answers the received
        #value.) 
        #Block No. 4Byte Request: 0
        # Answer: add 0x8000_0000 to the last packet.
        # Data transmission other than above: add 1
        # (max: 0x7fff_ffff)
        #Reserve 2          8 Byte       Fixed to “99999999”
        
        byteOrder = 'little'

        l_str = (bytes(self.identifier, 'ascii') +
                self.headSize[0].to_bytes(1, byteorder=byteOrder) +           
                self.headSize[1].to_bytes(1, byteorder=byteOrder) +
                self.dataSize[0].to_bytes(1, byteorder=byteOrder) +           
                self.dataSize[1].to_bytes(1, byteorder=byteOrder) +
                self.reserve1.to_bytes(1, byteorder=byteOrder) +              
                self.procDiv.to_bytes(1, byteorder=byteOrder) +               
                self.ACK.to_bytes(1, byteorder=byteOrder) +
                                
                self.reqID.to_bytes(1, byteorder=byteOrder) +                
                                                            
                self.blockNo[0].to_bytes(1, byteorder=byteOrder) +             
                self.blockNo[1].to_bytes(1, byteorder=byteOrder) +                  
                self.blockNo[2].to_bytes(1, byteorder=byteOrder) +                  
                self.blockNo[3].to_bytes(1, byteorder=byteOrder) +                 
                self.reserve2.to_bytes(8, byteorder=byteOrder)  +                    
                self.cmdNo[0].to_bytes(1, byteorder=byteOrder) +
                self.cmdNo[1].to_bytes(1, byteorder=byteOrder) +
                self.inst[0].to_bytes(1, byteorder=byteOrder) +
                self.inst[1].to_bytes(1, byteorder=byteOrder) +
                self.attr.to_bytes(1, byteorder=byteOrder) +
                self.service.to_bytes(1, byteorder=byteOrder) +
                self.padding[0].to_bytes(1, byteorder=byteOrder) +
                self.padding[1].to_bytes(1, byteorder=byteOrder))

        if (isinstance(self.data, str)):
            #data is string
            l_str = (l_str + self.data)
        else:
            for i in range(self.dataSize[0]):
                l_str = (l_str + self.data[i].to_bytes(1, byteorder=byteOrder))



        return l_str

class UdpPacket_Ans(UdpPacket):
     def __init__(self, ans_str):

        UdpPacket.__init__(self)

        self.identifier = ans_str[0:4]
        self.headSize[0] = ans_str[4]
        self.headSize[1] = ans_str[5]
        self.dataSize[0] = ans_str[6]
        self.dataSize[1] = ans_str[7]
        self.reserve1 = ans_str[8]
        self.procDiv = ans_str[9]
        self.ACK = ans_str[10]
        self.reqID = ans_str[11]
        self.blockNo[0] = ans_str[12]
        self.blockNo[1] = ans_str[13]
        self.blockNo[2] = ans_str[14]
        self.blockNo[3] = ans_str[15]
        self.reserve2 = ans_str[16:24]

        self.service = ans_str[24]
        self.status = ans_str[25]
        self.add_status_size = ans_str[26]
        self.padding1 = ans_str[27]
        self.add_status=[0,0]
        self.add_status[0] = ans_str[28]
        self.add_status[1] = ans_str[29]
        self.padding2=[0,0]
        self.padding2[0] = ans_str[30]
        self.padding2[1] = ans_str[31]


        size = self.dataSize[1] * 256 + self.dataSize[0]
        if (size <= 479 ):
            self.data = [0] * size
            for i in range(size):
                self.data[i] = ans_str[32 + i]