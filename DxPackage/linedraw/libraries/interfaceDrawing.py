from typing import Sized
import PIL
from PIL import ImageTk,Image, ImageDraw, ImageOps
import pytesseract
import cv2
from cv2 import *
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
import tksvg
from fs100 import *
import Slikanje
import Pisanje
import PisanjeBCI 
import SlikanjeBCI
import linedraw
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

from qtWindowComic import *

import drawAutomata  
import comic

# Comic 
import cairo
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from svgpath2mpl import parse_path
from xml.dom import minidom

'''
import linedraw

import Slikanje
import Pisanje
import PisanjeBCI
import SlikanjeBCI'''
import svgutils
import threading


# =================================================
robot = FS100("192.168.0.81")

app = QtWidgets.QApplication(sys.argv)
windowQT = qtWindowComic() #QtWidgets.QWidget()
windowQT.hide()


# =================================================
# Setup OpenCV
width, height = 800, 600
#width, height = 1920, 1080
camera=0
cap = cv2.VideoCapture(camera) #1 is usb camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# =================================================
# Setup windows Tkinter ()

# First window
root = Tk()
root.bind('<Escape>', lambda e: root.quit())
#lmain = Label(root)
#lmain.pack()

canvas = Canvas(root, width = 1280, height = 720)  
canvas.pack()  
root.geometry("+400+0")
root.minsize(800,600)

# Second window (Buttons)
root2 = Tk()
root2.title("Controls")
root2.bind('<Escape>', lambda e: root.quit())




root3 = Tk()
root3.title("Izberi program")
root3.bind('<Escape>', lambda e: root.quit())
choices = {'Slikanje','Slikanje BCI','Pisanje','Pisanje BCI','Risanje','Comic'}
tkvar = StringVar(root3)
popupMenu = OptionMenu(root3, tkvar, *choices)
popupMenu.config(font=("Times New Roman", 15))
napis = Label(root3, text="Izberi program: " ,font=("Times New Roman", 25))
napis.place(x=100,y=10)
popupMenu.place(x=100,y=50,width=200)
root3.minsize(400,200)
root3.geometry('400x200+0+0')
inputText=""
defaultImageLocation = "C:/Users/300ju/Desktop/DxPackage/linedraw/images/testImage.jpg"
imgLocation=defaultImageLocation
#root3.geometry("+50+0")

lmain = Label(root)
lmain.pack()
root2.minsize(400,400)
root2.geometry("+0+230")

currentProgram = "Izberi program"
textENA=""
threadStart = threading.Thread(target=Slikanje.start)
threadStop = threading.Thread(target=Slikanje.stop)
programRunning = False

# =================================================
# Global variables 

#marker=41000
#pencil=62000
#black marker=77502
#silver/gold marker=80689
  
toolType = 64664 #64000
svg_image = None
svg_image_display = None
machinePaused = False
toogleFullScreen = False

status = "waitingToTakePicture"
lines = None # Array of lines to be draw
homePositionAr = (185000,0,125000,1800000,0,0,0)

#myComic = comic()

# ===================================================

def moveToPosLinear(posAr):
    global robot
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        #print(status)
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
            print(len(posAr))
        robot.move(None, FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
            FS100.MOVE_SPEED_CLASS_MILLIMETER, 3000, posAr)

def moveToPosJoint(posAr):
    global robot
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        #print(status)
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
            print(len(posAr))
        robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
            FS100.MOVE_SPEED_CLASS_MILLIMETER, 9000, posAr)
            
            #3000
            
def isNotMoving():
    global robot
    status = {}
    pos_info = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        status = robot.getTravel_status_cb()
        #print("status from Draw",status)
        return status
    return False 

def OnPressed_ButStartProgram(event):
    global programRunning,popupMenu,threadStop,threadStart
    ButStartProgram.config(bg='red')
    setThreads()
    playCurrentJob()
    if(programRunning==False):
        ButStartProgram.config(bg='white', fg='blue')
        popupMenu.configure(state="disabled")
    else:
        threadStop.start()

    print('Start program')
    
    threadStart.start()
    programRunning=True

def OnHover_ButStartProgram(event):
    ButStartProgram.config(bg='darkgrey', fg='white')
def OnLeave_ButStartProgram(event):
    ButStartProgram.config(bg='white', fg='black')
ButStartProgram = Label(root2, text='Start program', bg='white', relief='groove',font=("Times New Roman", 20))
ButStartProgram.place(x=10, y=50, width=100)
ButStartProgram.bind('<Button-1>', OnPressed_ButStartProgram)
ButStartProgram.bind('<Enter>', OnHover_ButStartProgram)
ButStartProgram.bind('<Leave>', OnLeave_ButStartProgram)
ButStartProgram.pack()
ButStartProgram.forget()

entry1=Text(root2,font = "CNCVector 25 bold",width=20,height=3)

def OnPressed_ButReadText(event):
    global inputText,textENA
   
    ButReadText.config(bg='red')
    inputText=entry1.get("1.0",'end-1c')
    #print(inputText)
    #drawBox()
    #drawText()
    #drawComic()

    textENA = windowQT.sendENAText(inputText)
    
    #windowQT.sendTextToEva(textENA)
    print("USER: "+inputText)
    print("EVA: "+textENA)
    
def OnHover_ButReadText(event):
    ButReadText.config(bg='darkgrey', fg='white')
def OnLeave_ButReadText(event):
    ButReadText.config(bg='white', fg='black')
ButReadText = Label(root2, text='Read text', bg='white', relief='groove',font=("Times New Roman", 20))
ButReadText.place(x=10, y=50, width=100)
ButReadText.bind('<Button-1>', OnPressed_ButReadText)
ButReadText.bind('<Enter>', OnHover_ButReadText)
ButReadText.bind('<Leave>', OnLeave_ButReadText)
ButReadText.pack()
ButReadText.forget()

#entry1=Entry(root2,font = "CNCVector 20 bold",justify="center",width=25)


# Button Stop drawing
def OnPressed_ButStop(event):
    print('Stop drawing')
    global robot
    robot.stop()
    ButStop.config(bg='white', fg='grey')
def OnHover_ButStop(event):
    ButStop.config(bg='darkgrey', fg='white')
def OnLeave_ButStop(event):
    ButStop.config(bg='white', fg='black')
ButStop = Label(root2, text='Stop drawing', bg='white', relief='groove',font=("Times New Roman", 20))
ButStop.place(x=10, y=50, width=100)
ButStop.bind('<Button-1>', OnPressed_ButStop)
ButStop.bind('<Enter>', OnHover_ButStop)
ButStop.bind('<Leave>', OnLeave_ButStop)
ButStop.pack()
ButStop.forget()

def OnPressed_ButStopProgram(event):
    global programRunning,threadStop
    setThreads()
    if(programRunning):
        print('Stop program')
        ButStopProgram.config(bg='white', fg='grey')
        popupMenu.configure(state="active")
        programRunning=False
        threadStop.start()
        var_s1 = FS100.Variable(FS100.VarType.BYTE, 5, 1)
        robot.write_variable(var_s1)
    
def OnHover_ButStopProgram(event):
    global machinePaused
    if machinePaused:
        ButStopProgram.config(bg='green', fg='white')
    else:
        ButStopProgram.config(bg='red', fg='white')
def OnLeave_ButStopProgram(event):
    global machinePaused
    if machinePaused:
        ButStopProgram.config(bg='white', fg='grey')
    else:
        ButStopProgram.config(bg='white', fg='black')
ButStopProgram = Label(root2, text='Stop program', bg='white', relief='groove',font=("Times New Roman", 20))
ButStopProgram.place(x=10, y=80, width=100)
ButStopProgram.bind('<Button-1>', OnPressed_ButStopProgram)
ButStopProgram.bind('<Enter>', OnHover_ButStopProgram)
ButStopProgram.bind('<Leave>', OnLeave_ButStopProgram)
ButStopProgram.pack()
ButStopProgram.forget()

# Button Pause drawing
def OnPressed_ButPause(event):
    global machinePaused
    print('Pause drawing')
    ButPause.config(bg='white', fg='grey')
    machinePaused = not machinePaused
def OnHover_ButPause(event):
    global machinePaused
    if machinePaused:
        ButPause.config(bg='green', fg='white')
    else:
        ButPause.config(bg='red', fg='white')
def OnLeave_ButPause(event):
    global machinePaused
    if machinePaused:
        ButPause.config(bg='white', fg='grey')
    else:
        ButPause.config(bg='white', fg='black')
ButPause = Label(root2, text='Pause drawing', bg='white', relief='groove',font=("Times New Roman", 20))
ButPause.place(x=10, y=80, width=100)
ButPause.bind('<Button-1>', OnPressed_ButPause)
ButPause.bind('<Enter>', OnHover_ButPause)
ButPause.bind('<Leave>', OnLeave_ButPause)
ButPause.pack()
ButPause.forget()


# Button Take Camera Picture 
def OnPressed_ButTakePicture(event):
    global toolType, status, imgLocation
    print('Take picture')
    print("TOOL: ",toolType)
    imgLocation = defaultImageLocation
    ButTakePicture.config(bg='white', fg='grey') 
    if status != "waitingToAproveDrawing":
        status = "waitingToAproveDrawing"
        takePicture()
    else:
        status = "waitingToTakePicture"
    
def OnHover_ButTakePicture(event):
    ButTakePicture.config(bg='darkgrey', fg='white')
def OnLeave_ButTakePicture(event):
    ButTakePicture.config(bg='white', fg='black')
ButTakePicture = Label(root2, text='Take photo', bg='white', relief='groove',font=("Times New Roman", 20))
ButTakePicture.place(x=10, y=110, width=100)
ButTakePicture.bind('<Button-1>', OnPressed_ButTakePicture)
ButTakePicture.bind('<Enter>', OnHover_ButTakePicture)
ButTakePicture.bind('<Leave>', OnLeave_ButTakePicture)
ButTakePicture.pack()
ButTakePicture.forget()

# Button FullScreen
def OnPressed_ButFullScreen(event):
    global machinePaused

    if(len(app.screens())>1):
        windowQT.resize(500,500)
        windowQT.move(-1980,100)
        windowQT.show()
        s = app.screens()[1]
        # Display info about secondary screen 
        print('Screen Name: {} Size: {}x{} Available geometry {}x{} '.format(s.name(), s.size().width(), s.size().height(), s.availableGeometry().width(), s.availableGeometry().height()))
        #windowQT.windowHandle().setScreen(s)
        windowQT.showMaximized()
        windowQT.showFullScreen()

    
    print('Toggle fullscreen')
    ButFullScreen.config(bg='white', fg='grey')
    #toogleFullScreen = not toogleFullScreen
    #root.attributes("-alpha", 00)
     # maximize the window
    
    
    
def OnHover_ButFullScreen(event):
    global toogleFullScreen
    if toogleFullScreen:
        ButFullScreen.config(bg='green', fg='white')
    else:
        ButFullScreen.config(bg='red', fg='white')
def OnLeave_ButFullScreen(event):
    global toogleFullScreen
    if toogleFullScreen:
        ButFullScreen.config(bg='white', fg='grey')
    else:
        ButFullScreen.config(bg='white', fg='black')
ButFullScreen = Label(root2, text='Fullscreen', bg='white', relief='groove',font=("Times New Roman", 20))
ButFullScreen.place(x=10, y=140, width=100)
ButFullScreen.bind('<Button-1>', OnPressed_ButFullScreen)
ButFullScreen.bind('<Enter>', OnHover_ButFullScreen)
ButFullScreen.bind('<Leave>', OnLeave_ButFullScreen)
ButFullScreen.pack()
ButFullScreen.forget()

# Create the list of options 


#marker=41000
#pencil=62000
#black marker=77502
#silver/gold marker=80689
def cameraSelect():
    global camera,cap
    camera = cam.get()
    print("selected cam: "+str(camera))
    cap = cv2.VideoCapture(camera) #1 is usb camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    #print(toolType)
cam = IntVar(root2)
C1 = Radiobutton(root2, text="USB Camera", variable=cam, value=1,
                  command=cameraSelect,font=("Times New Roman", 15))
C1.pack()
C1.forget()

C2 = Radiobutton(root2, text="Webcam", variable=cam, value=0,
                  command=cameraSelect,font=("Times New Roman", 15))
C2.pack()
C2.forget()

def sel():
    global toolType
    
    toolType = var.get()
    lmain.config(text = toolType)
    #print(toolType)
var = IntVar(root2)

R1 = Radiobutton(root2, text="Brush", variable=var, value=62000,
                  command=sel,font=("Times New Roman", 15))
R1.pack()
R1.forget()
#R1.place(x=10, y=170)

#Marker
R2 = Radiobutton(root2, text="SmallMarker", variable=var, value=25481,
                  command=sel,font=("Times New Roman", 15))
R2.pack()
#R2.place(x=10, y=200)
R2.forget()

R3 = Radiobutton(root2, text="BlackMarker", variable=var, value=77502,
                  command=sel,font=("Times New Roman", 15))
R3.pack()
#R3.place(x=10, y=230)
R3.forget()

#64.664
R4 = Radiobutton(root2, text="Gold/Silver Marker", variable=var, value=64664,
                  command=sel,font=("Times New Roman", 15))
R4.pack()
#R4.place(x=10, y=260)
R4.forget()

R5 = Radiobutton(root2, text="Thick Marker", variable=var, value=60796,
                  command=sel,font=("Times New Roman", 15))
R5.pack()
#R5.place(x=10, y=290)
R5.forget()
#lmain.config(text = toolType)
#label.config(text = toolType)
# Display Camera

# Button Home
def OnPressed_ButHome(event):
    print('Home')
    pos = []
    pos.append(homePositionAr)
    moveToPosLinear(pos)
    ButHome.config(bg='white', fg='grey')
def OnHover_ButHome(event):
    ButHome.config(bg='darkgrey', fg='white')
def OnLeave_ButHome(event):
    ButHome.config(bg='white', fg='black')
ButHome = Label(root2, text='Home', bg='white', relief='groove',font=("Times New Roman", 20))
ButHome.place(x=10, y=290, width=100)
ButHome.bind('<Button-1>', OnPressed_ButHome)
ButHome.bind('<Enter>', OnHover_ButHome)
ButHome.bind('<Leave>', OnLeave_ButHome)
ButHome.pack()
ButHome.forget()

# Button Browse
def OnPressed_ButBrowse(event):
    global imgLocation, status
    print('Browse')
    pos = []
    pos.append(homePositionAr)
    moveToPosLinear(pos)

    # open file picker
    imgLocation =  filedialog.askopenfilename(initialdir = "C:/Users/300ju/Desktop/DxPackage/linedraw/images", title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    print(imgLocation)
    
    # draw photo
    if status != "waitingToAproveDrawing":
        status = "waitingToAproveDrawing"
        takePicture()
    else:
        status = "waitingToTakePicture"

    ButBrowse.config(bg='white', fg='grey')
def OnHover_ButBrowse(event):
    ButBrowse.config(bg='darkgrey', fg='white')
def OnLeave_ButBrowse(event):
    ButBrowse.config(bg='white', fg='black')
ButBrowse = Label(root2, text='Browse', bg='white', relief='groove',font=("Times New Roman", 20))
ButBrowse.place(x=10, y=30, width=200)
ButBrowse.bind('<Button-1>', OnPressed_ButBrowse)
ButBrowse.bind('<Enter>', OnHover_ButBrowse)
ButBrowse.bind('<Leave>', OnLeave_ButBrowse)
ButBrowse.pack()
ButBrowse.forget()

# Drawing 
def OnPressed_ButDrawing(event):
    global toolType,inputText,textENA,homePositionAr,lines
    print(toolType)
    if(toolType!=0):
        if(currentProgram=="Comic"):
            comicAr=windowQT.prepareDrawing(215000,0,lines[0],lines[1],toolType,homePositionAr,lines[2])
            print(comicAr)
            moveToPosJoint(comicAr)
        else:
            preparedLinesAr = prepareDrawing()
            moveToPosLinear(preparedLinesAr)
        print('Start drawing')
        status = "drawing" 
    else:
        showwarning(title="No tool selected", message="Please select a tool to draw with!")


def OnHover_ButDrawing(event):
    ButDrawing.config(bg='darkgrey', fg='white')
def OnLeave_ButDrawing(event):
    ButDrawing.config(bg='white', fg='black')
ButDrawing = Label(root2, text='Draw', bg='white', relief='groove',font=("Times New Roman", 20))
ButDrawing.place(x=10, y=310, width=100)
ButDrawing.bind('<Button-1>', OnPressed_ButDrawing)
ButDrawing.bind('<Enter>', OnHover_ButDrawing)
ButDrawing.bind('<Leave>', OnLeave_ButDrawing)
ButDrawing.pack()
ButDrawing.forget()

def OnPressed_ButDrawingBorderText(event):
    global toolType,inputText,textENA
    
    print(toolType)
    if(toolType!=0):
        if(currentProgram=="Comic"):
            boxArHuman=drawBox("user")
            boxArRobot=drawBox("robot")
            textArHuman=drawText("user",inputText)
            textArRobot=drawText("robot",textENA)
            
            coordAr=merge(boxArHuman,boxArRobot,textArHuman,textArRobot)
            moveToPosLinear(coordAr)
        else:
            preparedLinesAr = prepareDrawing()
            moveToPosLinear(preparedLinesAr)
        print('Start drawing')
        status = "drawing" 
    else:
        showwarning(title="No tool selected", message="Please select a tool to draw with!")


def OnHover_ButDrawingBorderText(event):
    ButDrawingBorderText.config(bg='darkgrey', fg='white')
def OnLeave_ButDrawingBorderText(event):
    ButDrawingBorderText.config(bg='white', fg='black')
ButDrawingBorderText = Label(root2, text='Draw border/text', bg='white', relief='groove',font=("Times New Roman", 20))
ButDrawingBorderText.place(x=10, y=310, width=100)
ButDrawingBorderText.bind('<Button-1>', OnPressed_ButDrawingBorderText)
ButDrawingBorderText.bind('<Enter>', OnHover_ButDrawingBorderText)
ButDrawingBorderText.bind('<Leave>', OnLeave_ButDrawingBorderText)
ButDrawingBorderText.pack()
ButDrawingBorderText.forget()

def takePicture():
    global lines, svg_image, svg_image_display,imgLocation
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    # Image to SVG
    
    imwrite("C:/Users/300ju/Desktop/DxPackage/linedraw/images/testImage.jpg",frame) 
    
    #imgLocation = "images/nora"
    #imgType = ".png"
    image = PIL.Image.open(imgLocation)
    rotatedIm = image.rotate(90,expand=True)
    #imgNew=imgLocation+"New"+imgType
    #rotatedIm.save(imgNew)
    # Convert image to line array
    #lines = linedraw.sketch(imgNew)
    
    #Get Render SVG (Normal)
    lines = linedraw.sketchIM(image)
    svg_image_display = tksvg.SvgImage(file="C:/Users/300ju/Desktop/DxPackage/linedraw/output/out.svg")
   
    #svg_image_display = svg_image_display.resize(newsize)

    #Get Render SVG (Normal)
    lines = linedraw.sketchIM(rotatedIm)
    svg_image = tksvg.SvgImage(file="C:/Users/300ju/Desktop/DxPackage/linedraw/output/out.svg")
    #newsize = (width, height)
    
    #Get Render SVG (Display)
    
    #svg_image_display = tksvg.SvgImage(file="./output/out.svg")
    #newsize = (width, height)
    #svg_image
    #svg_image_display = svg_image_display.resize(newsize)


def prepareDrawing():
    global lines,toolType

    w = lines[0]
    h = lines[1]
    
    usefulDrawingSizeX = 160.0  #MAX x on paper
    usefulDrawingSizeY = 160.0 #MAX y on paper
    #outputAr = deepcopy(lines[2])
    if w!=h:  
        print("horizontal")
        usefulDrawingSizeY = 270.0  #270

    brushLift = 20000
    #CALIBRATION FOR TOOL Z AXIS
    #z=41000 #marker
    #z=62000 #pencil
    #z = 77502
    
    toolType=64664
    z=toolType
    print("z: ",z)
    
     #gold/silver
    #z=58000 #Black adjustable
    indexi = 0
    outputAr = []
    for i in lines[2]: 
        indexj = 0
        for j in i:
            #185000+160000
            x = (((((j[0]* 0.5)/w)*usefulDrawingSizeX) )*1000.0) - ((usefulDrawingSizeX*0.5)*1000.0) + 185000
            y = (((((j[1]* 0.5)/h)*usefulDrawingSizeY) )*1000.0) - ((usefulDrawingSizeY*0.5)*1000.0)
            #TOP border X LIMIT 345000(185000+usefulDrawingX)
            if(x <185000+usefulDrawingSizeX*1000.0):
                if indexj==0:
                    outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                #if indexi==0 and indexj==0:
                #    print(j[0],x)
                #outputAr[indexi][indexj] = (round(x),round(y),z,1800000,0,0,0)
                #outputAr[indexi][indexj] = (round(x),round(y),z,1800000,0,0,0)
                
                outputAr.append((round(x),round(y),z,1800000,0,0,0))
                if(indexj==len(i)) :
                    outputAr.append((round(x),round(y),z+brushLift,1800000,0,0,0))
                    # if we want to change color 

            indexj += 1
        indexi += 1
    # add Home
    outputAr.append(homePositionAr)
    print(outputAr)
    return outputAr

def drawBox(type):
    global toolType
    if(type=="robot"):
        coordAr = windowQT.comicBox(45000,85000,100000,40000,toolType)
        return(coordAr)
    else:
        coordAr = windowQT.comicBox(-120000,85000,100000,40000,toolType)
        return(coordAr)
    #moveToPosLinear(coordAr)

def drawText(type,text):
    global toolType,inputText
    if(type=="robot"):
        xTranslate = 100000
        yTranslate = 60000
        coordAr = windowQT.textToSVG(xTranslate,yTranslate,text,200000-40000,toolType)
        return(coordAr)
    else:
        xTranslate = 100000
        yTranslate = -120000
        coordAr = windowQT.textToSVG(xTranslate,yTranslate,text,200000-40000,toolType)
        return(coordAr)
    #moveToPosJoint(coordAr)
    
def drawComic():
    global toolType,homePositionAr,lines
    print("lines send")
    print(lines[2])
    w = lines[0]
    h = lines[1]
    coordAr = windowQT.prepareDrawing(260000,0,w,h,toolType,homePositionAr, lines[2])
    print("lines received")
    print(coordAr)
    return(coordAr)
    #moveToPosJoint(coordAr)

def merge(boxHumanAr,textHumanAr,boxRobotAr,textRobotAr):
    coordAr=[]
    for i in boxHumanAr:
        coordAr.append(i)
    for i in boxRobotAr:
        coordAr.append(i)
    for i in textHumanAr:
        coordAr.append(i)
    for i in textRobotAr:
        coordAr.append(i)
    return(coordAr)

def show_frame():
    global status,cap
    if status == "waitingToTakePicture":
        #print("showing frame...")
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        #height,width,byts=frame.shape
        #print(height,width)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        windowQT.updateData(cv2image)
        windowQT.update()
        
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        canvas.delete('all')
        canvas.create_image(20,20, anchor=NW, image=imgtk) 
        canvas.image = imgtk

        #canvasFull.delete('all')
        #canvasFull.create_image(0,0, anchor=NW, image=imgfs) 
        #canvasFull.image = imgfs
        #lmain.imgtk = imgtk
        if currentProgram=="Comic":
                #myComic.
                text=""
                #print("Comic")
                #canvas.create_text(300, 20, text= "Comic text",fill="black",font=('Helvetica 15 bold'))
                #canvas.create_text(300, 350, text= "Try to pose for this comic text",fill="black",font=('Helvetica 15 bold'))
                
    if(status == "drawing" or status == "waitingToAproveDrawing"):
        #Get Render SVG
        if  svg_image_display != None:
            
            canvas.delete('all')
            canvas.create_image(20,20, anchor=NW, image=svg_image_display) 
            canvas.image = svg_image_display
            #lmain.svg_image = svg_image
            #lmain.configure(image=svg_image)
            if currentProgram=="Comic":
                #myComic.
                canvas.create_text(300, 20, text= inputText,fill="black",font=('Helvetica 15 bold'))
                
    canvas.after(200, show_frame)
    #canvasFull.after(200, show_frame)
    #lmain.after(2, show_frame)

def setThreads():
    global threadStart,threadStop
    if(currentProgram=="Slikanje"):
        threadStart=threading.Thread(target=Slikanje.start) 
        threadStop=threading.Thread(target=Slikanje.stop) 
        #thread.daemon=True
    elif(currentProgram=="Pisanje"):   
        threadStart=threading.Thread(target=Pisanje.start) 
        #thread.daemon=True
        threadStop=threading.Thread(target=Pisanje.stop) 
    elif(currentProgram=="Pisanje BCI"):   
        threadStart=threading.Thread(target=PisanjeBCI.start) 
        #thread.daemon=True
        threadStop=threading.Thread(target=PisanjeBCI.stop) 
    elif(currentProgram=="Slikanje BCI"):   
        threadStart=threading.Thread(target=SlikanjeBCI.start) 
        #thread.daemon=True
        threadStop=threading.Thread(target=SlikanjeBCI.stop)
    return(threadStart,threadStop)

def change_dropdown(*args):
    global currentProgram,threadStart,threadStop
    #if(threadStart.is_alive):
        #print("Thread is alive!")
        #threadStop.start()
    previousProgram=currentProgram
    
    
    if(programRunning==True):
        showwarning(title=previousProgram+" is still running", message="Please stop "+previousProgram+" program!")
        
    else:
        currentProgram = tkvar.get()
        if(currentProgram in ["Pisanje","Pisanje BCI","Slikanje","Slikanje BCI"]):
            setThreads()        
            hideRisanje()
            #threadStop.start()          
        elif(currentProgram=="Comic"):
            hideRisanje()
            showComic()
        else:
            showRisanje()
            #canvas.pack()
            #show_frame()

        #print(currentProgram)


def playCurrentJob():
    global currentProgram
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)

    if(currentProgram in ["Slikanje","Slikanje BCI"]):
        robot.select_job("COPIC-MAIN")
    elif(currentProgram in ["Pisanje","Pisanje BCI"]):
        robot.select_job("CRKE-TEST")
    robot.play_job()
    
def hideRisanje():
    ButStop.pack_forget()
    ButHome.pack_forget()
    ButPause.pack_forget()
    ButBrowse.pack_forget()
    ButTakePicture.pack_forget()
    ButFullScreen.pack_forget()
    ButDrawing.pack_forget()
    #canvas.pack_forget()
    C1.pack_forget()
    C2.pack_forget()
    R1.pack_forget()
    R2.pack_forget()
    R3.pack_forget()
    R4.pack_forget()
    R5.pack_forget()
    entry1.pack_forget()
    ButReadText.pack_forget()
    ButDrawingBorderText.pack_forget()
    ButStartProgram.pack()
    ButStopProgram.pack()
    
    

def showRisanje():
    ButStopProgram.forget()
    ButStartProgram.forget()
    ButHome.pack()
    ButBrowse.pack()
    ButFullScreen.pack()
    C1.pack()
    C2.pack()
    ButTakePicture.pack()
    R1.pack()
    R2.pack()
    R3.pack()
    R4.pack()
    R5.pack()
    ButDrawing.pack()
    ButStop.pack()
    entry1.pack_forget()
    ButReadText.pack_forget()
    ButDrawingBorderText.pack_forget()
    

def showComic():
    ButStopProgram.forget()
    ButStartProgram.forget()
    ButHome.pack()
    ButBrowse.pack()
    ButFullScreen.pack()
    C1.pack()
    C2.pack()
    entry1.pack()
    ButReadText.pack()
    ButDrawingBorderText.pack()
    ButTakePicture.pack()
    R1.pack()
    R2.pack()
    R3.pack()
    R4.pack()
    R5.pack()
    ButDrawing.pack()
    ButStop.pack()


    
    
tkvar.trace('w', change_dropdown)
'''   
#update second screen (Buttons)
def show_frame2():
    lmain.svg_image = svg_image
    lmain.configure(image=svg_image)
    lmain.after(10, show_frame2)
'''

if __name__ == '__main__':
    #while True:
    
    #show_frame2()
    show_frame()
    root.mainloop()
    
    