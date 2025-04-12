import sys
import os
import time

from collections import Counter

import numpy as np

import cv2
import imutils

from cv2.dnn import Net
from imutils.video import FPS

from .animal_classifier import AnimalClassifier

SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
                "dining-table", "dog", "horse", "motorbike", "person", "potted plant", "sheep", "sofa", "train",
                "monitor"]
        
REQ_CLASSES = ["bird", "cat", "cow", "dog", "horse", "sheep"]

class_model = SCRIPT_PATH + '/Models/ResNet_15_classifier.pth'
classifier = AnimalClassifier(class_model)

class AnimalDetector:
    proto = SCRIPT_PATH + '/Models/MobileNet_AnimalProto.txt'
    model = SCRIPT_PATH + '/Models/MobileNet_AnimalDetector.caffemodel'

    NET: Net = cv2.dnn.readNetFromCaffe(proto, model)
    
    def detect(cls, name, camera: str):
        vs = cv2.VideoCapture(camera, cv2.CAP_FFMPEG)
        time.sleep(2)
        fps = FPS().start()

        conf_thresh = 0.2
        count = []
        flag = 0
        c = 0
        animals = []  # Initialize counter
        while vs:
            success, frame = vs.read()
            if not success:
                break
            frame = imutils.resize(frame, width=500)
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

            AnimalDetector.NET.setInput(blob)
            detections = AnimalDetector.NET.forward()
            
            det = 0
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > conf_thresh:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    if CLASSES[idx] in REQ_CLASSES:
                        class_input = frame
                        class_input = cv2.cvtColor(class_input, cv2.COLOR_BGR2RGB)
                        class_output = classifier.detect(class_input)
                        animals.append(class_output)
                        
                        det = 1
                        label = "{}: {:.2f}%".format(class_output, confidence * 100)
                        cv2.rectangle(frame, (startX, startY), (endX, endY), (36, 255, 12), 2)
                        if (startY - 15) > 15:
                            y = (startY - 15)
                        else:
                            y = (startY + 15)
                        cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

            cv2.imshow( f'{name}: Press Q to Close', frame )
            #cv2.moveWindow(f'{name}: Press Q to Close', 100, 100)
            count.append(det)

            if flag == 1 and len(count) > c + (11 * 18):
                flag = 0
            if Counter(count[len(count) - 36:])[1] > 15 and flag == 0:
                print('Animals Detected!')
                flag = 1
                c = len(count)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            fps.update()
        animals = list(set(animals))
        fps.stop()
        print("Elapsed time: {:.2f}".format(fps.elapsed()))
        print("Approximate FPS: {:.2f}".format(fps.fps()))
        vs.release()
        cv2.destroyAllWindows()
        return animals