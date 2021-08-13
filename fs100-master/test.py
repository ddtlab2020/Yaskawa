import socket
import time
from fs100 import *
from 
robot=FS100("192.168.0.81")
pos_info = {}
while(True):
    
    
        #(185000, 0, 125000, 1800000, 0, 0, 0)
        #(339660, 15320, 164143, 1684970, -893683, 143329, 0)

    pos_info = {}
    if FS100.ERROR_SUCCESS == robot.read_position(pos_info):
        print(pos_info)

     '''   
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
    stops = [(185000, 0, 125000, 1800000, 0, 0, 0),
             (339660, 15320, 164143, 1684970, -893683, 143329, 0)]
    robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
               FS100.MOVE_SPEED_CLASS_PERCENT, 250, stops)
    
    time.sleep(1)

    if FS100.ERROR_SUCCESS == robot.get_status(status):
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
    stops = [(339660, 15320, 164143, 1684970, -893683, 143329, 0),
             (185000, 0, 125000, 1800000, 0, 0, 0)]
    robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, FS100.MOVE_COORDINATE_SYSTEM_ROBOT,
               FS100.MOVE_SPEED_CLASS_PERCENT, 250, stops)
    '''
