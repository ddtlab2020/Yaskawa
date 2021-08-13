from cv2 import *
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test",cv2.WINDOW_NORMAL)
    cv2.resizeWindow('cam-test', 640, 480) 
    imshow("cam-test",img)
    waitKey(0)
    destroyWindow("cam-test")
    imwrite("images/testImage.jpg",img) #save image