# -*- coding: utf-8 -*-
import asyncio
import base64
import math
import os
import time

import cv2 as cv
from ultralytics import YOLO

from core.ws_con_manager import TWSEventData
from api.api_v1.endpoints.socket import cm


stop_event = asyncio.Event()

async def stream_analyze(rtsp_url):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    path_model = os.path.join(script_directory, '..', 'yolo', 'yolovX.pt')
    model = YOLO(path_model)
    cap = cv.VideoCapture()
    url = rtsp_url
    cap.open(url, cv.CAP_FFMPEG)
    frame_rate = cap.get(5)
    cap.set(cv.CAP_PROP_FPS, 3)
    old_frame = ''
    try:
        while True:
            ret, frame = cap.read()
            frameId = cap.get(1)
            if stop_event.is_set():
                break
            if not ret:
                st = time.time()
                cap.release()
                cap.open(url, cv.CAP_FFMPEG)
                cap.set(cv.CAP_PROP_FPS, 3)
                print(
                    "tot time lost due to reinitialization : %s", time.time() - st
                )
                continue
            await asyncio.sleep(0.1)
            frame = cv.resize(frame, (640,640))
            if frameId % math.floor(frame_rate) == 5:
                results = model(frame, conf=0.3, device="0")
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
                names = results[0].names
                if len(boxes) > 0:
                    for (box, class_name) in zip(boxes, classes):
                        x1, y1, x2, y2 = box
                        if class_name == 0 :
                            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            text = f'{names[class_name]}'
                            cv.putText(frame, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        else:
                            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                            text = f'{names[class_name]}'
                            cv.putText(frame, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                _, buffer = cv.imencode('.jpg', frame)
                encoded_frame = base64.b64encode(buffer).decode('utf-8')
                if old_frame != encoded_frame:
                    ws_msg: TWSEventData = {
                                'event': 'new_frame',
                                'data': encoded_frame,
                            }
                    old_frame = encoded_frame
                    await cm.broadcast(ws_msg)
                classes = [names[class_name] for class_name in classes]
                timestamp = time.time()
                if 'weapon' in classes:
                        ws_msg: TWSEventData = {
                                'event': 'weapon_detect',
                                'data': {'img': encoded_frame,'filename': f'{timestamp}.jpg', 'class': classes},
                        }
                        await cm.broadcast(ws_msg)
    except Exception as e:
        pass