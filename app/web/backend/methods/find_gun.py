# -*- coding: utf-8 -*-
import base64
import time
import math
import os

from ultralytics import YOLO
import cv2 as cv
from api.api_v1.endpoints.socket import cm
from core.ws_con_manager import TWSEventData



async def video_analyze(filename):
    result_list = []
    script_directory = os.path.dirname(os.path.abspath(__file__))
    path_video = os.path.join(script_directory, '..', 'video', filename)
    path_model = os.path.join(script_directory, '..', 'yolo', 'yolovX.pt')
    model = YOLO(path_model)
    cap = cv.VideoCapture(path_video)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    frame_rate = cap.get(5)
    try:
        while True:
            ret, frame = cap.read()
            frameId = cap.get(1)
            if not ret:
                break
            current_frame += 1
            processed = (current_frame / total_frames)
            if frameId % math.floor(frame_rate) == 1:
                results = model(frame, conf=0.3, device="0")
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
                names = results[0].names
                if len(boxes) > 0:
                    frame_with_boxes = frame.copy()
                    for (box, class_name) in zip(boxes, classes):
                        x1, y1, x2, y2 = box
                        if class_name == 0:
                            cv.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            text = f'{names[class_name]}'
                            cv.putText(frame_with_boxes, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        else:
                            cv.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            text = f'{names[class_name]}'
                            cv.putText(frame_with_boxes, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    timestamp = int(time.time())
                    _, buffer = cv.imencode('.jpg', frame_with_boxes)
                    encoded_frame = base64.b64encode(buffer).decode('utf-8')
                    classes = [names[class_name] for class_name in classes]
                    if 'weapon' in classes:
                        ws_msg: TWSEventData = {
                                'event': 'video_weapon',
                                'data': {'img': encoded_frame,'filename': f'{timestamp}.jpg', 'class': classes},
                        }
                        await cm.broadcast(ws_msg)
                ws_msg: TWSEventData = {
                                'event': 'progress',
                                'data': {'progress': processed},
                        }
                await cm.broadcast(ws_msg)
        return result_list
    except Exception as e:
        print(e)