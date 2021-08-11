from fs100 import *
robot = FS100("192.168.0.81")
robot.select_job("COPIC-MAIN")
var_s1 = FS100.Variable(FS100.VarType.BYTE, 3, 1)
var_s2 = FS100.Variable(FS100.VarType.BYTE, 3, 1)

status = {}
if FS100.ERROR_SUCCESS == robot.get_status(status):
    #print(status)
    if not status['servo_on']:
        robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)

robot.play_job()
time.sleep(5)
robot.write_variable(var_s2)
robot.write_variable(var_s1)


print("hello")