import cv2
import sys
from fs100 import *
from dx_fast_eth_server import * 
import math

objekt=DxFastEthServer("192.168.0.81")
# Setup robot
robot = FS100("192.168.0.81")

# Setup computer vision
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(1) #Usb camera in laptop is 1

width, height = 800, 600
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

movingX=True
movingY=False
# Current position arm robot
robotCurrentPosition = {}
timeWithoutFace = time.time()
timeIdelingFace = time.time()

def moveToPos(posAr):
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        #print(status)
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
        robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
            FS100.MOVE_SPEED_CLASS_PERCENT, 3000, posAr)
            
def isNotMoving():
    pos_info = {}
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        robot.read_position(robotCurrentPosition)
        status = robot.getTravel_status_cb()
        return status
    return False 

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    '''faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )'''

    # Draw a rectangle around the faces
    countFaces = 0
    facePosition = False
    centerRectX = 0
    centerRectY = 0
    targetXFacePosition = 375
    targetYFacePosition = 275
    
    #square target
    cv2.rectangle(frame, (targetXFacePosition, targetYFacePosition), (targetXFacePosition+50, targetYFacePosition+50), (255, 0, 0), 2)

    # find close rect to target
    closeDistanceFaceTarget = 9999
    for (x, y, w, h) in faces:
        faceDist = math.hypot( (x - targetXFacePosition), (y - targetYFacePosition))
        if faceDist<closeDistanceFaceTarget and w>30:
            closeDistanceFaceTarget = faceDist
    # display faces
    for (x, y, w, h) in faces:
        #if countFaces == 0:
        # Select face target that is closer
        faceDist = math.hypot( (x - targetXFacePosition), (y - targetYFacePosition))
        if closeDistanceFaceTarget <= faceDist and w>30:
            facePosition = True
            centerRectX = (x + (w*0.5)-5) 
            centerRectY = (y + (h*0.5)-5)
            # Draw target Center
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #countFaces += 1
    
    if facePosition == False:
        var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, 0)
        var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, 0)
        robot.write_variable(var_z)
        robot.write_variable(var_x)
        # send B_iddle = 0 
        #print(time.time()-timeWithoutFace)
        if (time.time()-timeWithoutFace) > 5.000:
            var_i = FS100.Variable(FS100.VarType.DOUBLE, 10, 0)
            robot.write_variable(var_i)
            print("goes to idle")
            timeIdelingFace = time.time()
        
    # Calculate movement robot if robot had finish movement
    #print("Calculate position to move robot",robotCurrentPosition)
    #if not isNotMoving() and facePosition != None:
    if facePosition:
        #if time.time() - timeIdelingFace<0.25:
            
        timeWithoutFace = time.time()

        var_i = FS100.Variable(FS100.VarType.DOUBLE, 10, 1)
        robot.write_variable(var_i)
        # drawing 
        #print(centerRectX,centerRectY)
        
        dist = math.hypot( (centerRectX - targetXFacePosition), (centerRectY - targetYFacePosition))
        if dist < 50 :
            cv2.rectangle(frame, (targetXFacePosition, targetYFacePosition), (targetXFacePosition+50, targetYFacePosition+50), (255, 255, 0), 2)
            var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, 0)
            var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, 0)
            robot.write_variable(var_z)
            robot.write_variable(var_x)
            
        else:
            if(movingX):
                if(centerRectX-targetXFacePosition <=10 and centerRectX-targetXFacePosition >= -10 ):
                    movingX=False
                    movingY=True
                else:
                    print("move")
                    if centerRectX > targetXFacePosition:
                        #Change incremented position X to -200 and set y to 0
                        var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, -500)
                        var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, 0)
                        robot.write_variable(var_z)
                        robot.write_variable(var_x)
                        print("right")
                    else:
                        #Change incremented position X to 200 and set y to 0
                        print("left")
                        var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, 500)
                        var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, 0)
                        robot.write_variable(var_z)
                        robot.write_variable(var_x)

            if(movingY):
                if(centerRectY-targetYFacePosition <=10 and centerRectY-targetYFacePosition >= -10 ):
                    movingY=False
                    movingX=True

                if centerRectY > targetYFacePosition:
                    #Change incremented position Z to -200 and set x to 0
                    print("bottom")
                    var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, -500)
                    var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, 0)
                    robot.write_variable(var_x)
                    robot.write_variable(var_z)
                else:
                    #Change incremented position Z to -200 and set x to 0
                    print("top")
                    var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, 500)
                    var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, 0)
                    robot.write_variable(var_x)
                    robot.write_variable(var_z)
                    

            
        # Xminimum =-197263 and Xmaximum=197263 
        #var_x = FS100.Variable(FS100.VarType.DOUBLE, 11, 5000)
        # Zminimum = -20000 and Zmaximum=40000
        #var_z = FS100.Variable(FS100.VarType.DOUBLE, 12, 1000)
        # B_iddle = 0 b_Engage = 30000
        
        #robot.write_variable(var_x)
        #robot.write_variable(var_z)
        #robot.write_variable(var_i)
        
        robot.read_variable(var_i)
        #print("var_i={}".format(var_i.val))
        #From HOME position
        # if square is up which axis to change ( y) and direction (minus) 
        # if square is down which axis to change (y) and direction (plus)

        # if square is left which axis to change (x) and direction (plus or minus)
        # if square is right which axis to change (x) and direction (plus or minus)

        #moveToPos([(round(x),round(y),z,1800000,0,0,0)])
    # Display the resulting frame
    cv2.namedWindow("Video",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
var_i = FS100.Variable(FS100.VarType.DOUBLE, 10, 0)
robot.write_variable(var_i)
video_capture.release()
cv2.destroyAllWindows()