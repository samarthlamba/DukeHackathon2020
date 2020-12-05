# Bruno Capuano 2020
# display the camera feed using OpenCV
# display FPS
# load YOLO object detector trained with COCO Dataset (80 classes)
# analyze each camera frame using YoloV3 searching for banana classes

import numpy as np
import time
import cv2
import os
from collections import Counter
objects = []
def initYoloV3():
    global labelColors, layerNames, net
    
    # random color collection for each class label
    np.random.seed(42)
    labelColors = np.random.randint(0, 255, size=(len(Labels), 3), dtype="uint8")

    # load model
    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    layerNames = net.getLayerNames()
    layerNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def counter(largeObject, localObject):
    for k in localObject:
        if(localObject.count(k) > largeObject.count(k)):
            while(localObject.count(k) != largeObject.count(k)):
                largeObject.append(k)
                
                
def toSpeech(objectArray):
    wroteObject = []
    speech = "There are "
    for k in objectArray:
        wroteObject.append(k);
        speech = speech + str(objectArray.count(k)) + " " + str(k) + ", " + "and "
    if(speech[-4: len(speech)] == "and "):
            speech = speech[0: len(speech)-5]
    return speech
            
def analyzeFrame(frame, displayBoundingBox = True, displayClassName = True, displayConfidence = True):
    global H, W
    localObjects = []
    # init
    if W is None or H is None:
        (H, W) = frame.shape[:2]
    if net is None:
        initYoloV3()

    yoloV3ImgSize = (416, 416)
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, yoloV3ImgSize, swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(layerNames)
    end = time.time()

    boxes = []
    confidences = []
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > confidenceDef:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidenceDef, thresholdDef)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            if (displayBoundingBox):
                color = [int(c) for c in labelColors[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            if(displayClassName and displayConfidence):
                text = "{}: {:.4f}".format(Labels[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            elif(displayClassName):
                text = str(f"{Labels[classIDs[i]]}:")
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            localObjects.append(Labels[classIDs[i]])
            counter(objects, localObjects)
        
        print(objects);


# Camera Settings
camera_Width  = 640 # 1024 # 1280 # 640
camera_Heigth = 480 # 780  # 960  # 480
frameSize = (camera_Width, camera_Heigth)
video_capture = cv2.VideoCapture(1)
time.sleep(2.0)
(W, H) = (None, None)

# YOLO Settings
weightsPath   = "yolov3.weights"
configPath    = "yolov3.cfg"
LabelsPath    = "coco.names"
Labels        = open(LabelsPath).read().strip().split("\n")
confidenceDef = 0.5
thresholdDef  = 0.3
net           = (None)
labelColors   = (None)
layerNames    = (None)

i = 0
detectionEnabled = True
while True:
    i = i + 1 
    start_time = time.time()

    ret, frameOrig = video_capture.read()
    frame = cv2.resize(frameOrig, frameSize)

    if(detectionEnabled):
        analyzeFrame(frame)

    if (time.time() - start_time ) > 0:
        fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, fpsInfo, (10, 20), font, 0.4, (255, 255, 255), 1)

    cv2.imshow('@elbruno - YoloV3 Object Detection', frame)

    # key controller
    key = cv2.waitKey(1) & 0xFF    
    if key == ord("d"):
        if (detectionEnabled == True):
            detectionEnabled = False
        else:
            detectionEnabled = True

    if key == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()



