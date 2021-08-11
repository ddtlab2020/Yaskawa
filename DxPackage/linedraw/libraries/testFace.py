import cv2
import face_detection
import time
print(face_detection.available_detectors)
detector = face_detection.build_detector("DSFDDetector", confidence_threshold=.5, nms_iou_threshold=.3)
# BGR to RGB
#im = cv2.imread("path_to_im.jpg")[:, :, ::-1]


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# Capture frame-by-frame

while True:
    ret, frame = cap.read()
    startTime=time.time()
    detections = detector.detect(frame) #[xmin, ymin, xmax, ymax, detection_confidence]

    print(detections)
    print(time.time()-startTime)
