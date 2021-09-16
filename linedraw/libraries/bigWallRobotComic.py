import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont,QImage, QPixmap,QPolygon, QFontDatabase,QPen,QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import * 
import cv2
from cv2 import *
import socket
import requests

from svgpathtools import svg2paths2
import pyttsx3
# external libraries
import cairo
from PyQt5.QtGui import QFont, QFontMetrics
from svgpath2mpl import parse_path
from xml.dom import minidom
from PyQt5.QtWidgets import QApplication

import svgutils
from svgutils.compose import Figure
import svgutils.transform as sg
import sys
import re
from svgmanip import Element

def convert_to_pixels(measurement):
    value = float(re.search(r'[0-9\.]+', measurement).group())
    if measurement.endswith("px"):
        return value
    elif measurement.endswith("mm"):
        return value * 3.7795275591
    else:
        # unit not supported
        return value

def moveSVGdown(w, h):
    #svg = svgutils.transform.fromfile('C:/Users/300ju/Desktop/DxPackage/linedraw/output/outOriginal.svg')
    originalSVG = svgutils.compose.SVG('C:/Users/300ju/Desktop/DxPackage/linedraw/output/outOriginal.svg')

    # moves down 100+
    # first param is width, second is height, negative moves it up
    originalSVG.move(0, 180)
    figure = svgutils.compose.Figure(h, w + 180, originalSVG)
    figure.save("C:/Users/300ju/Desktop/DxPackage/linedraw/output/outOriginalMoved.svg")

def mergeSVGs():
    #image = sg.fromfile("C:/Users/300ju/Desktop/DxPackage/linedraw/output/outOriginal.svg")       
    image = sg.fromfile("C:/Users/300ju/Desktop/DxPackage/linedraw/output/outOriginalMoved.svg")
    text = sg.fromfile("C:/Users/300ju/Documents/comicVarMar/outputTextPath.svg")
    question = sg.fromfile("C:/Users/300ju/Documents/comicVarMar/outputTextQuestionPath.svg")
    textBorder = sg.fromfile("C:/Users/300ju/Desktop/DxPackage/linedraw/output/rect.svg")
        
    """
    width = convert_to_pixels(image.get_size()[0])
    height = convert_to_pixels(image.get_size()[1])
    logo_width = convert_to_pixels(text.get_size()[0])
    logo_height = convert_to_pixels(text.get_size()[1])
    """
    root = text.getroot()
    root.moveto(1, 1)

    root2 = textBorder.getroot()
    root2.moveto(1, 1)

    root3 = question.getroot()
    root3.moveto(1, 1)

    image.append([root2])
    image.append([root3])
    image.append([root])
    
    image.save('C:/Users/300ju/Desktop/DxPackage/linedraw/output/merged.svg')
    print("merged svgs")

class bigWallRobotComic(QWidget):

    def __init__(self):
        super().__init__()

        #self.textSize = 50
        self.textSize = 14
        self.folderPath = "c://Users//300ju//Documents//comicVarMar//"
        
        fontId = QFontDatabase.addApplicationFont(self.folderPath+"cnc_v.ttf")
        if fontId < 0:
            print('font not loaded')
        else:
            print(fontId)
            self.familyCNCfont = QFontDatabase.applicationFontFamilies(fontId)
            print(self.familyCNCfont[0])

        self.cameraImage = None
        self.initUI()

    def initUI(self):
        self.text = "Make siluette from text"
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Drawing text')
        self.show()
    
    def updateText(self,text):
        self.comicText = text

    def updateData(self,image):
        self.cameraImage = image

    def paintEvent(self, event):
        widthWin = self.rect().width() #3840 #self.baseSize().width()
        heightWin = self.rect().height() #2160 #self.baseSize().height()
        qp = QPainter()
        qp.begin(self)
        try:
            cv2image = cv2.cvtColor(self.cameraImage, cv2.COLOR_BGR2RGBA)
            h, w, channels = cv2image.shape
            #center = cv2image.shape / 2
            #x = center[1] - w/2
            #y = center[0] - h/2
            #crop_img = cv2image[y:y+h, x:x+w].copy()
            self.QtImg = QImage(cv2image.data, self.cameraImage.shape[1], self.cameraImage.shape[0],QImage.Format_RGB32)
            pixmap = QPixmap.fromImage(self.QtImg)
            qp.drawPixmap(0,0,400,500, pixmap)
        except:
            print("Not load image QT")
        #points = [QPoint(0,0),QPoint(0,1000),QPoint(1000,1000),QPoint(1000,0),QPoint(0,0)]  
        #qp.translate(QPoint(widthWin*0.5,0))
        #qp.setBrush(Qt.white) # filling color
        #qp.drawPolygon(QPolygon(points))
        #qp.translate(QPoint(-widthWin*0.5,0))
        #qp.setBrush(Qt.black)
        #qp.drawRect(0,(heightWin*0.8),widthWin,(heightWin*0.2))

        qp.translate(QPoint(0,(-heightWin*0.2)))
        self.drawComicText(event, qp)
        qp.translate(QPoint(0,(heightWin*0.6)))
        
        self.drawInstructionsText(event, qp)
        qp.end()
    
    def computeWidthText(self, text):
        print("compute text")
        font = QFont("CNC Vector",self.textSize)
        fm = QFontMetrics(font)
        width = int(fm.width(text))
        print(width)
        #height=fm.height()
        return width

    def loadSVGPaths(self,file):
        paths, attributes, svg_attributes = svg2paths2(file)
        print(len(paths),len(attributes))
        lines = []
        for path in paths:
            lines.append(parse_path(path.d()).vertices)
        return lines

    def textToSVG(self,xTranslate,yTranslate, text, widthText, z, type):
        print(text)
        #global lines
        textAr = []
        # Calculate number lines
        widthTextComputed = self.computeWidthText(text)
        print(widthTextComputed)
        
        if True: #widthText < widthTextComputed:
            print("single line text")
            #print("not dividing!")
            # textAr.append(text)
            textAr = text.split("\n")
        else:
            print("divide text")
            words =  text.split(" ")
            newLine = words[0]
            #for word in words:
            #    if computeWidthText(newLine)<width
        print("start cairo")

        fileName = "outputTextPath.svg"
        if type != "robot":
            fileName = "outputTextQuestionPath.svg"

        with cairo.SVGSurface(self.folderPath + fileName, 700, 700) as surface:
            # creating a cairo context object for SVG surface
            # useing Context method
            Context = cairo.Context(surface)
            
            # setting color of the context
            Context.set_source_rgb(1, 0, 0)
            
            # approximate text height
            Context.set_font_size(self.textSize)
            
            # Font Style
            Context.select_font_face("CNC Vector", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            margin = 0
            for textLine in textAr:
                print("texline:"+textLine)
                # position for the text
                print("Size: "+str(self.textSize))
                #Context.move_to(5, 45 * (textSize+5))
                
                # text eva response
                Context.move_to(320, 30 + margin)
                if type != "robot":
                    Context.move_to(30, 30 + margin) # question
                
                margin = margin + 20
                                
                # displays the text
                Context.text_path(textLine)
                #Context.rectangle(20, 20, 120, 80)

                # Width of outline
                Context.set_line_width(2)
                
                # stroke out the color and width property
                Context.stroke()
                #value=surface.get_document_unit()
                
                path=Context.copy_path()

        # printing message when file is saved
        print("File Saved")
        
        doc = minidom.parse(self.folderPath + fileName)  # parseString also exists

        path_strings = [path.getAttribute('d') for path
                        in doc.getElementsByTagName('path')]
        #print(path_strings)
        doc.unlink()

        print("file loaded")
        #print(path_strings[0])

        #print(path_strings[0])

        lines = []
        pathAr =  str(path_strings[0]).split("M")[1:]
        print("total lines:",len(pathAr))
        #print(parse_path("M"+pathAr[0] ).vertices)
        for path in pathAr:
            pathVertices = parse_path("M"+path).vertices
            lines.append(pathVertices)
        ''' '''
        
        #lines = self.loadSVGPaths(self.folderPath+"outputTextPath.svg")
        print("lines separate")
        rotateAndScaleLinesAr = [] 
        
        scaleFont = (1000 * 0.25) #0.35
        for l in lines:
            rotateAndScaleLine = []
            for point in l:
                rotateAndScaleLine.append([(point[1]*scaleFont)+xTranslate,(point[0]*scaleFont)+yTranslate])
            rotateAndScaleLinesAr.append(rotateAndScaleLine)
        # copy transformed lines    
        lines = rotateAndScaleLinesAr 
        self.textLinesAr = lines
        linesForArm = self.prepareJoinArLinesForArm(lines,z)
        return linesForArm
    
    def textToSVGWallRobot(self,xTranslate,yTranslate, text, widthText, z, type):
        print(text)
        #global lines
        textAr = []
        # Calculate number lines
        widthTextComputed = self.computeWidthText(text)
        print(widthTextComputed)
        
        if True: #widthText < widthTextComputed:
            print("single line text")
            #print("not dividing!")
            # textAr.append(text)
            textAr = text.split("\n")
        else:
            print("divide text")
            words =  text.split(" ")
            newLine = words[0]
            #for word in words:
            #    if computeWidthText(newLine)<width
        print("start cairo")

        fileName = "outputTextPath.svg"
        if type != "robot":
            fileName = "outputTextQuestionPath.svg"

        with cairo.SVGSurface(self.folderPath + fileName, 700, 700) as surface:
            # creating a cairo context object for SVG surface
            # useing Context method
            Context = cairo.Context(surface)
            
            # setting color of the context
            Context.set_source_rgb(1, 0, 0)
            
            # approximate text height
            Context.set_font_size(self.textSize)
            
            # Font Style
            Context.select_font_face("CNC Vector", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            
            margin = 0
            for textLine in textAr:
                print("texline:"+textLine)
                # position for the text
                print("Size: "+str(self.textSize))
                #Context.move_to(5, 45 * (textSize+5))
                
                # text eva response
                Context.move_to(320, 30 + margin)
                if type != "robot":
                    Context.move_to(30, 30 + margin) # question
                
                margin = margin + 20
                                
                # displays the text
                Context.text_path(textLine)
                #Context.rectangle(20, 20, 120, 80)

                # Width of outline
                Context.set_line_width(2)
                
                # stroke out the color and width property
                Context.stroke()
                #value=surface.get_document_unit()
                
                path=Context.copy_path()

        # printing message when file is saved
        print("File Saved")
        
        doc = minidom.parse(self.folderPath + fileName)  # parseString also exists

        path_strings = [path.getAttribute('d') for path
                        in doc.getElementsByTagName('path')]
        #print(path_strings)
        doc.unlink()

        print("file loaded")
        #print(path_strings[0])

        #print(path_strings[0])

        lines = []
        pathAr =  str(path_strings[0]).split("M")[1:]
        print("total lines:",len(pathAr))
        #print(parse_path("M"+pathAr[0] ).vertices)
        for path in pathAr:
            pathVertices = parse_path("M"+path).vertices
            lines.append(pathVertices)
        ''' '''
        
        #lines = self.loadSVGPaths(self.folderPath+"outputTextPath.svg")
        print("lines separate")
        rotateAndScaleLinesAr = [] 
        
        scaleFont = (1000 * 0.25) #0.35
        for l in lines:
            rotateAndScaleLine = []
            for point in l:
                rotateAndScaleLine.append([(point[1]*scaleFont)+xTranslate,(point[0]*scaleFont)+yTranslate])
            rotateAndScaleLinesAr.append(rotateAndScaleLine)
        # copy transformed lines    
        lines = rotateAndScaleLinesAr 
        self.textLinesAr = lines
        linesForArm = self.prepareJoinArLinesForArm(lines,z)
        return linesForArm

    def sendENAText(self,text):
        text = text.replace(" ","%20",999)
        r = requests.get('http://localhost:5000/test/'+text)
        return r.text

    def prepareDrawing(self,posx,posy,w,h,toolType,homePositionAr, lines):
        usefulDrawingSizeX = 130.0  #MAX x on paper
        usefulDrawingSizeY = 160.0 #160#MAX y on paper
        #outputAr = deepcopy(lines[2])
        if w!=h:  
            print("horizontal")
            usefulDrawingSizeY = 200.0  #270

        brushLift = 20000
        #CALIBRATION FOR TOOL Z AXIS
        #z=41000 #marker
        #z=62000 #pencil
        #z = 77502
        z=toolType
        print("z: ",z)
        print("Width: "+str(w))
        print("Height: "+str(h))
        print("Position x: "+str(posx))
        
        #z=65000
        #z=85000
        #adjustable black marker
        
        indexi = 0
        outputAr = []
        for i in lines: 
            indexj = 0
            for j in i:
                #185000+160000
                #x = int((j[0]*1000.0)*0.7 + posx)
                #y = int((j[1]*1000.0)*0.7 + posy)
                x = (((((j[0]* 0.5)/w)*usefulDrawingSizeX) )*1000.0) - ((usefulDrawingSizeX*0.5)*1000.0) +posx
                y = (((((j[1]* 0.5)/h)*usefulDrawingSizeY) )*1000.0) - ((usefulDrawingSizeY*0.5)*1000.0)
                #TOP border X LIMIT 345000(185000+usefulDrawingX)
                if indexj==0:
                    outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                else:
                    outputAr.append((round(x),round(y),z,1800000,0,0,0))
                indexj += 1
            
            indexi += 1
                
        # test merge svg
        #moveSVGdown(w, h)
        #mergeSVGs()
            
        # add Home
        outputAr.append(homePositionAr)
        return outputAr

    def prepareDrawingRobotWall(self,posx,posy,w,h,toolType,homePositionAr, lines):
        usefulDrawingSizeX = 130.0  #MAX x on paper
        usefulDrawingSizeY = 160.0 #160#MAX y on paper
        #outputAr = deepcopy(lines[2])
        if w!=h:  
            print("horizontal")
            usefulDrawingSizeY = 200.0  #270

        brushLift = 10000
        #CALIBRATION FOR TOOL Z AXIS
        #z=41000 #marker
        #z=62000 #pencil
        #z = 77502
        z=0
        print("z: ",z)
        print("Width: "+str(w))
        print("Height: "+str(h))
        print("Position x: "+str(posx))
        
        #z=65000
        #z=85000
        #adjustable black marker
        
        indexi = 0
        outputAr = []
        for i in lines: 
            indexj = 0
            for j in i:
                #185000+160000
                #x = int((j[0]*1000.0)*0.7 + posx)
                #y = int((j[1]*1000.0)*0.7 + posy)
                x = (((((j[0]* 0.5)/w)*usefulDrawingSizeX) )*1000.0) - ((usefulDrawingSizeX*0.5)*1000.0)+posx
                y = (((((j[1]* 0.5)/h)*usefulDrawingSizeY) )*1000.0) - ((usefulDrawingSizeY*0.5)*1000.0)+120000
                #TOP border X LIMIT 345000(185000+usefulDrawingX)
                if indexj==0:
                    outputAr.append((round(x),round(y),z-brushLift,1800000,0,0,0))
                else:
                    outputAr.append((round(x),round(y),z,1800000,0,0,0))
                indexj += 1
            
            indexi += 1
                
        # test merge svg
        #moveSVGdown(w, h)
        #mergeSVGs()
            
        # add Home
        #outputAr.append(homePositionAr)
        return outputAr

    def drawComicText(self, event, qp):
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('CNC Vector', 20))
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)

    
    def drawInstructionsText(self, event, qp):
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('CNC Vector',40))
        qp.drawText(event.rect(), Qt.AlignCenter, "Pose in the photo reacting on the comic text")

    def changeLineAxis(self,ar):
        tempAr = []
        for l in ar:
            tempLineAr =[]
            tempAr.append([int(l[1]),int(l[0])])
        return tempAr

    def prepareJoinArLinesForArm(self,ar, z):
        tempAr = []
        #prepare lines
        for l in ar:
            tempAr.append(self.prepareLinesForArm(l,z))
        # join array
        joinAr = []
        for l in tempAr:
            joinAr +=l
        return joinAr

    def prepareLinesForArm(self,ar, z):
        tempAr = []
        for l in ar:
            tempAr.append([int(l[0]),int(l[1]),int(z),1800000,0,0,0])
        tempAr.append([int(l[0]),int(l[1]),int(z+10000),1800000,0,0,0])
        return tempAr

    def prepareLinesForArmWallRobot(self,ar, z):
        tempAr = []
        z=0
        for l in ar:
            tempAr.append([int(l[0]),int(l[1]),int(z),1800000,0,0,0])
        tempAr.append([int(l[0]),int(l[1]),int(z-10000),1800000,0,0,0])
        return tempAr

    def comicBox(self,posx,posy,widthText,heightText,z):
        arrowHeighComicBox = 15000.0
        arrowWidthComicBox = 15000.0
        posxLeft = posx
        posxRight = posx+widthText
        posyBottom = posy+heightText
        lines = []
        # Vertex 1: box top-left
        startPosition = [posxLeft,posy]
        lines.append(startPosition)
        # Vertex 2: box top-right
        lines.append([posxRight,posy])
        # Vertex 3: bottom-right
        lines.append([posxRight,posy+heightText])
        # Vertex 4: arrow left-side
        lines.append([posx+widthText*0.5+arrowWidthComicBox*0.5,posyBottom])
        # Vertex 5: arrow bottom side (this point is in center of X axis)
        lines.append([posx+widthText*0.5-arrowWidthComicBox*0.5,posyBottom+arrowHeighComicBox])
        # Vertex 6: arrow right-side
        lines.append([posx+widthText*0.5-arrowWidthComicBox*0.5,posyBottom])
        # Vertex 7: box bottom-left
        lines.append([posxLeft,posyBottom])
        # Closing vertex
        lines.append(startPosition)
        self.comicBoxAr = self.changeLineAxis(lines)
        linesForArm = self.prepareLinesForArm(self.comicBoxAr,z)
        return linesForArm

    def comicBoxRobotWall(self,posx,posy,widthText,heightText,z):
        arrowHeighComicBox = 15000.0
        arrowWidthComicBox = 15000.0
        posxLeft = posx
        posxRight = posx+widthText
        posyBottom = posy+heightText
        lines = []
        # Vertex 1: box top-left
        startPosition = [posxLeft,posy]
        lines.append(startPosition)
        # Vertex 2: box top-right
        lines.append([posxLeft,posy+widthText])
        # Vertex 3: bottom-right
        lines.append([posxLeft-heightText,posy+widthText])
        # Vertex 4: arrow left-side
        #lines.append([posxLeft-heightText,posy-widthText*0.5-arrowWidthComicBox*0.5])
        # Vertex 5: arrow bottom side (this point is in center of X axis)
        #lines.append([posx+widthText*0.5-arrowWidthComicBox*0.5,])
        # Vertex 6: arrow right-side
        #lines.append([posx+widthText*0.5-arrowWidthComicBox*0.5,posyBottom])
        # Vertex 7: box bottom-left
        lines.append([posxLeft-heightText,posy])
        # Closing vertex
        lines.append(startPosition)
        #self.comicBoxAr = self.changeLineAxis(lines)
        self.comicBoxAr=lines
        linesForArm = self.prepareLinesForArmWallRobot(self.comicBoxAr,z)
        return linesForArm



def sendTextToEva(self,text):
    UDP_IP = "192.168.1.38"
    UDP_PORT = 65432
    MESSAGE = text
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

#sendTextToEva("I am stupid and I don't know are I am doing")

def speakText(self,text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()