# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import datetime
import cv2

counter_id=0

from pymongo import MongoClient
import datetime
# client = MongoClient()
# client = MongoClient('localhost', 27017)

from database_operations import database_operations as db

import time, os
from threading import Thread, current_thread
from multiprocessing import Process, current_process

import tkinter as tk
from tkinter import ttk

from tk_table import data

import time



file1 = open("Mongo_database_config.txt", "r+")

t = file1.read()
mongo_config = t.split("\n")

if len(mongo_config)>1:

    url=mongo_config[1]
else:
    print("*** Please enter MongoDB connection string in Mongo_database_config.txt file and save...*** ")    

database_object=db(url)
database_object.create_connection()
database_object.connect_database()


def video_processing():
    idx=0
    global database_object,counter_id
    
    # args = {
    #     'prototxt': 'C:\\Users\\swd7788\\PycharmProjects\\object_detection\\real-time-object-detection\\MobileNetSSD_deploy.prototxt.txt',
    #     'model': 'C:\\Users\swd7788\\PycharmProjects\\object_detection\\real-time-object-detection\\MobileNetSSD_deploy.caffemodel',
    #     'confidence': 0.2
    # }
    
    args = {
        'prototxt': 'MobileNetSSD_deploy.prototxt.txt',
        'model': 'MobileNetSSD_deploy.caffemodel',
        'confidence': 0.9
    }
    import os
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
    
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    
    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
    
    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    fps = FPS().start()
    
    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
    
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
    
        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
    
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]
    
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
    
                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                # print(label)
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    
                # print(CLASSES[idx])
                
            if idx:
                if CLASSES[idx]=="bottle":
                    if confidence> 0.1:
                        print("bottle_detected")
                        print(confidence)
                        if confidence>args["confidence"]:        
                            insert_data={"sku_id":str(counter_id),"Unit_id":"u1","status":"Good","timestamp":str(datetime.datetime.now())}
                            
                        else:
                            insert_data={"sku_id":str(counter_id),"Unit_id":"u1","status":"Bad","timestamp":str(datetime.datetime.now())}
                    
                    
                        record_id2=database_object.insert_data(insert_data)
                        counter_id+=1
        
        # show the output frame
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1) & 0xFF
    
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        # update the FPS counter
        fps.update()
    
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    
    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    exit(0)


def UI_display():
    global database_object
    
    database_data=database_object.find_data()
    data(database_data)


t1 = Thread(target = video_processing, args =())
t1.start()

t2 = Thread(target = UI_display, args =())
t2.start()    
t2.join()
   
    


 

