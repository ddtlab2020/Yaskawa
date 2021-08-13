from tkinter import *
from fs100 import *
robot = FS100("192.168.0.81")


window = Tk()
window.title('Kalkulator')
#window.geometry('355x475')
window.geometry('625x1000')
window.state('normal')
window.bind('<Escape>', lambda event: window.state('normal'))
window.bind('<F11>', lambda event: window.state('zoomed'))
window.configure(bg='#262626')
#window.iconbitmap('')
window.resizable(False,False)
expression = ''


def press(num):
    global expression
    if(num=="r"):
        xZamik=FS100.Variable(FS100.VarType.DOUBLE, 0, 0)
        yZamik=FS100.Variable(FS100.VarType.DOUBLE, 1, 0)
        robot.write_variable(xZamik)
        robot.write_variable(yZamik)

    elif(num=='h'):
        Stop=FS100.Variable(FS100.VarType.BYTE, 5, 1)
        robot.write_variable(Stop)
        pos = []
        pos.append((185000,0,125000,1800000,0,0,0))
        #print(pos)
        status = {}
        if FS100.ERROR_SUCCESS == robot.get_status(status):
            #print(status)
            if not status['servo_on']:
                robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)

        robot.move(None, FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, 
            FS100.MOVE_COORDINATE_SYSTEM_BASE,FS100.MOVE_SPEED_CLASS_PERCENT, 3000,pos)
    else:
        expression = expression + str(num)
        equation.set(expression)
def equalpress():
    global expression
    Stop=FS100.Variable(FS100.VarType.BYTE, 5, 0)
    robot.write_variable(Stop)
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)

    robot.select_job("CRKE-TEST")
    robot.play_job()
    try:
        yZamik=FS100.Variable(FS100.VarType.DOUBLE, 1,0)
        robot.write_variable(yZamik)
        
        total = str(round(eval(expression),2))
        expression+="="+total
        equation.set(total)
        
        stevec=0
        while(stevec<len(expression)):
            
            isReady= FS100.Variable(FS100.VarType.BYTE, 3)
            robot.read_variable(isReady)

            znak=FS100.Variable(FS100.VarType.BYTE, 3, ord(expression[stevec])+100)
            #print(ord(expression[stevec]))
            if(isReady.val==0):
            
                robot.write_variable(znak)
                stevec+=1
                #POSLEMO v ROKO
        
        xZamikRead=FS100.Variable(FS100.VarType.DOUBLE, 0)
        robot.read_variable(xZamikRead)
        xZamikWrite=FS100.Variable(FS100.VarType.DOUBLE, 0, xZamikRead.val-30000)
        robot.write_variable(xZamikWrite)

        expression = ''

        
        
    except:
        equation.set('error')
        expression = ''
def clear():
    global expression
    expression = ''
    equation.set('0')
button_frame = Frame(window,bg='#262626')
button_frame.pack()
equation = StringVar()
equation.set('0')
expression_field = Entry(button_frame,textvariable=equation,justify='right',font=('arial',38,'bold'))
button1 = Button(button_frame,text='1',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(1))
button2 = Button(button_frame,text='2',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(2))
button3 = Button(button_frame,text='3',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(3))
addition = Button(button_frame,text='+',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press('+'))
button4 = Button(button_frame,text='4',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(4))
button5 = Button(button_frame,text='5',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(5))
button6 = Button(button_frame,text='6',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(6))
subtract = Button(button_frame,text='-',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press('-'))
button7 = Button(button_frame,text='7',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(7))
button8 = Button(button_frame,text='8',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(8))
button9 = Button(button_frame,text='9',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(9))
multiply = Button(button_frame,text='*',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press('*'))
button0 = Button(button_frame,text='0',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press(0))
decimal = Button(button_frame,text='.',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press('.'))
clear = Button(button_frame,text='C',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=clear)
division = Button(button_frame,text='/',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=9,height=3,command=lambda:press('/'))
equal = Button(button_frame,text='=',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=38,height=3,command=equalpress)
reset = Button(button_frame,text='Reset Position',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=38,height=3,command=lambda:press('r'))
home = Button(button_frame,text='Home Position',font=('times new roman',21),relief='ridge',bd=1,bg='#cccccc',width=38,height=3,command=lambda:press('h'))
expression_field.grid(row=0,column=0,columnspan=4,ipadx=8,ipady=25,pady=12)
button1.grid(row=1,column=0)
button2.grid(row=1,column=1)
button3.grid(row=1,column=2)
addition.grid(row=1,column=3)
button4.grid(row=2,column=0)
button5.grid(row=2,column=1)
button6.grid(row=2,column=2)
subtract.grid(row=2,column=3)
button7.grid(row=3,column=0)
button8.grid(row=3,column=1)
button9.grid(row=3,column=2)
multiply.grid(row=3,column=3)
button0.grid(row=4,column=0)
decimal.grid(row=4,column=1)
clear.grid(row=4,column=2)
division.grid(row=4,column=3)
equal.grid(row=5,column=0,columnspan=4)
reset.grid(row=6,column=0,columnspan=4)
home.grid(row=7,column=0,columnspan=4)
window.mainloop()