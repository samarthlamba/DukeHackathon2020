import numpy as np
import time
import cv2
import os
import urllib3
import ssl
from collections import Counter
import gtts 
from playsound import playsound 
from collections import Counter
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

localObjects = []
objects = []
oldBoxCount = 0
video_capture = None
frameSize = None
W = None
H = None
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

def initYoloV3():
    global weightsPath, configPath, LabelsPath, Labels, confidenceDef, thresholdDef, net, labelColors, layerNames
    
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
    speech = "There is "
    for k in objectArray:
        if(k not in wroteObject):
            wroteObject.append(k);
            speech = speech + str(objectArray.count(k)) + " " + str(k) + ", " + "and "
    if(speech[-4: len(speech)] == "and "):
            speech = speech[0: len(speech)-6]
    sound_request = gtts.gTTS(speech)
    if os.path.exists("narration.mp3"):
        os.remove("narration.mp3")
    sound_request.save("narration.mp3")
    playsound("narration.mp3")
    return speech
            
def analyzeFrame(frame, displayBoundingBox = True, displayClassName = True, displayConfidence = True):
    print("analyzeFrame started")
    global H, W, localObjects, oldBoxCount
    
    # init
    oldLocalObjectsLength = len(localObjects)
    localObjects = []
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

    if(True): 
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidenceDef, thresholdDef)

        if len(idxs) > 0:
            for i in idxs.flatten():
                # (x, y) = (boxes[i][0], boxes[i][1])
                # (w, h) = (boxes[i][2], boxes[i][3])

                # if (displayBoundingBox):
                #     color = [int(c) for c in labelColors[classIDs[i]]]
                #     cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                # if(displayClassName and displayConfidence):
                #     text = "{}: {:.4f}".format(Labels[classIDs[i]], confidences[i])
                #     cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                # elif(displayClassName):
                #     text = str(f"{Labels[classIDs[i]]}:")
                #     cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                localObjects.append(Labels[classIDs[i]])
                counter(objects, localObjects)
        #if(len(localObjects) != oldLocalObjectsLength):   
        toSpeech(localObjects)
        print(localObjects)
        oldBoxCount = len(boxes)

def initialize():
    global video_capture, frameSize, ip_field, W, H
    # Camera Settings
    camera_Width  = 640 # 1024 # 1280 # 640
    camera_Heigth = 480 # 780  # 960  # 480
    frameSize = (camera_Width, camera_Heigth)

    print(ip_field.get())
    video_capture = cv2.VideoCapture('http://' + ip_field.get() + '/video')
    # time.sleep(2.0)
    (W, H) = (None, None)

def analysis_loop():
    global video_capture, frameSize, ip_field, root
    i = 0
    lastAmount = len(objects)
    detectionEnabled = True

    display_img = tk.Label(app_frame, image = ImageTk.PhotoImage(Image.open("opencv_frame.png")))
    display_img.pack(side = "bottom", fill = "both", expand = "yes")
    while True:
        print("sleeping")
        # start_time = time.time()
        
        video_capture.release()
        time.sleep(3);
        video_capture = cv2.VideoCapture('http://' + ip_field.get() + '/video')
        print("not sleeping")
    
        ret, frameOrig = video_capture.read()
        frame = cv2.resize(frameOrig, frameSize)
        cv2.imshow('GuideDog Image Recognition', frame)
        img_name = "opencv_frame.png"
        cv2.imwrite(img_name, frameOrig)
        if(detectionEnabled):
            analyzeFrame(frame)

        
        # cv2.imsave("annotated_image.png")

        # key controller
        key = cv2.waitKey(1) & 0xFF    
        if key == ord("d"):
            if (detectionEnabled == True):
                detectionEnabled = False
            else:
                detectionEnabled = True

        if key == ord("q"):
            break

def run():
    initialize()
    analysis_loop()

root = tk.Tk()
root.resizable(False, False)
root.title("GuideDog")
canvas = tk.Canvas(root, height = 200, width = 500)
canvas.pack()
app_frame = tk.Frame(root)
app_frame.place(relwidth = .95, relheight = .95, relx = .025, rely = .025)
ip_field_label = tk.Label(app_frame, text = "Enter the IP address that appears when streaming begins on the IP Camera app.\n")
ip_field_label.pack()
ip_field = tk.Entry(app_frame, width = 30)
ip_field.pack()
start_button = tk.Button(app_frame, text = "Start", height = 1, width = 5, command = run)
start_button.place(x = 210, y = 80)

if __name__ == "__main__":
    root.mainloop()
    video_capture.release()
    cv2.destroyAllWindows()



