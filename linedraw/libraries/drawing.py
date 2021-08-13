import linedraw
from copy import copy,deepcopy
from fs100 import *
from cv2 import *
from PIL import Image, ImageDraw, ImageOps



lastPosition = (0.0,0.0,0.0,0.0,0.0,0.0,0.0) 
takingPicture = False

robot = FS100("192.168.0.81")

def moveToPos(posAr):
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        #print(status)
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
        robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
            FS100.MOVE_SPEED_CLASS_PERCENT, 3000, posAr)
            
def isNotMoving():
    status = {}
    pos_info = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        status = robot.getTravel_status_cb()
        #print("status from Draw",status)
        return status
    return False 

def makePictureAndGetCoordinates():
    
    # initialize the camera
    cam = VideoCapture(1)
    namedWindow("cam-test",cv2.WINDOW_NORMAL)
    cv2.resizeWindow('cam-test', 1280, 720) 
    while(True):
            # 0 -> index of camera
        s, img = cam.read()
        if s:    # frame captured without any errors    
            imshow("cam-test",img)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                imwrite("images/testImage.jpg",img) 
                break

            
            
    cv2.destroyAllWindows()

    imwrite("images/testImage.jpg",img) #save image

    time.sleep(1)
    imgLocation="images/testImage"
    imgType=".jpg"
    image=Image.open(imgLocation+imgType)
    rotatedIm=image.rotate(90,expand=True)
    imgNew=imgLocation+"New"+imgType
    rotatedIm.save(imgNew)
    # Convert image to line array
    lines = linedraw.sketch(imgNew)
    #linedraw.visualize(lines)
    #for i in lines:
    #    print(i)
    #    print("\n")    
    #print(lines)
    w = lines[0]
    h = lines[1]

    usefulDrawingSizeX = 160.0  #MAX x on paper
    usefulDrawingSizeY = 160.0 #MAX y on paper
    #outputAr = deepcopy(lines[2])
    if w!=h:  
        usefulDrawingSizeY = 270.0  #270

    brushLift = 20000
    #CALIBRATION FOR TOOL Z AXIS
    z=41000 #marker
    #z=62000 #pencil
    
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
    return outputAr

while True: 
    
    if not isNotMoving():
        outputAr = makePictureAndGetCoordinates()
        moveToPos(outputAr)
        startProgram = False
        #print("=== Call again ===========")

        

    