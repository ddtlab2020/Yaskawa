from fs100 import *
import time
robot = FS100("192.168.0.81")
status = {}
if FS100.ERROR_SUCCESS == robot.get_status(status):
    if not status['servo_on']:
        robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
direction=""
old_direction=""
isDown=False

def moveToPos(direction):
    global robot,isDown
    
    if(direction=="Forward"):
        robot.move(None,FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS,FS100.MOVE_COORDINATE_SYSTEM_ROBOT,FS100.MOVE_SPEED_CLASS_MILLIMETER,400,[(10000,0,0,0,0,0,0)])
    elif(direction=="Backward"):
        robot.move(None,FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS,FS100.MOVE_COORDINATE_SYSTEM_ROBOT,FS100.MOVE_SPEED_CLASS_MILLIMETER,400,[(-10000,0,0,0,0,0,0)])
    elif(direction=="Left"):
        robot.move(None,FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS,FS100.MOVE_COORDINATE_SYSTEM_ROBOT,FS100.MOVE_SPEED_CLASS_MILLIMETER,400,[(0,10000,0,0,0,0,0)])
    elif(direction=="Right"):
        robot.move(None,FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS,FS100.MOVE_COORDINATE_SYSTEM_ROBOT,FS100.MOVE_SPEED_CLASS_MILLIMETER,400,[(0,-10000,0,0,0,0,0)])
    elif(direction=="Down"):
        if(isDown):
            
            print("Is down")
            #robot.move(None,FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS,FS100.MOVE_COORDINATE_SYSTEM_ROBOT,FS100.MOVE_SPEED_CLASS_MILLIMETER,400,[(0,0,10000,0,0,0,0)])
        else:
            #robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
            #FS100.MOVE_SPEED_CLASS_PERCENT, 100, [(185000,0,-76000,1800000,0,0,0)])
            isDown=True

            #3000
            #robot.move(None, FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT, FS100.MOVE_SPEED_CLASS_MILLIMETER, 250, stops)
            
def isMoving():
    global robot,direction,old_direction
    status = {}
    pos_info = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        status = robot.getTravel_status_cb()
        #print("status from Draw",status)
        return status
    return False 



if __name__ == '__main__':
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
    openf = open("C:/Users/300ju/Desktop/fileout.txt","w")
    openf.truncate()
    openf.close()
    while(True):
        openf = open("C:/Users/300ju/Desktop/fileout.txt","r+")
        content=openf.readlines()
        try:
            splitContent=content[len(content)-1].split(" ")
            print("LEFT: "+splitContent[0]+ " RIGHT: "+splitContent[11] + " FORWARD: "+splitContent[9] + " BACKWARD: "+splitContent[10] +" FINGER: "+splitContent[5])
            if(int(splitContent[0])>100):
                if(isMoving()==False):
                    moveToPos("Left")

            if(int(splitContent[11])>100):
                if(isMoving()==False):
                    moveToPos("Right")
            
            if(int(splitContent[9])>100):
                if(isMoving()==False):
                    moveToPos("Forward")

            if(int(splitContent[10])>100):
                if(isMoving()==False):
                    moveToPos("Backward")
            '''    
            if(int(splitContent[5])>100):
                if(isMoving()==False):
                    moveToPos("Down")'''
            openf.truncate()
            
            time.sleep(0.5)


        except:
            openf.truncate()

        #Direction is data from glove
        #time.sleep(1)
        if(isMoving()==True):
            if(old_direction != direction):
                robot.stop()
        
            

        


