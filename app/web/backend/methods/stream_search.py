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
    path_cls_model = os.path.join(script_directory, '..', 'yolo', 'yolovCLS.pt')
    model = YOLO(path_model)
    model_cls = YOLO(path_cls_model)
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
            frame_crop = frame.copy()
            frame_area = frame.shape[0] * frame.shape[1]
            if frameId % math.floor(frame_rate) == 5:
                results = model(frame, conf=0.3, device="0")
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
                detect_names = results[0].names
                if len(boxes) > 0:
                    frame_with_boxes = frame.copy()
                    poses = []
                    for (box, class_name) in zip(boxes, classes):
                        x1, y1, x2, y2 = box
                        if class_name == 0:
                            box_area = (x2 - x1) * (y2 - y1)
                            cv.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            text = f'{detect_names[class_name]}'
                            if box_area < frame_area:
                                cropped_image = frame_crop[y1:y2, x1:x2]
                                results_cls = model_cls(cropped_image, device="0")
                                print(results_cls)
                                probs = results_cls[0].probs.data.cpu().numpy()
                                print(probs)
                                if probs is not None and len(probs) > 0:
                                    names_cls = results_cls[0].names
                                    shooter_conf = probs[1]
                                    base_conf = probs[0]
                                    if shooter_conf > base_conf:
                                        poses.append(names_cls[1])
                                        cv.putText(frame_with_boxes, f'{text}, {names_cls[1]}', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    elif shooter_conf < base_conf:
                                        poses.append(names_cls[0])
                                        cv.putText(frame_with_boxes, f'{text}, {names_cls[0]}', (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            else:
                                cv.putText(frame_with_boxes, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        cv.rectangle(frame_with_boxes, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        text = f'{detect_names[class_name]}'
                        cv.putText(frame_with_boxes, text, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                _, buffer = cv.imencode('.jpg', frame)
                encoded_frame = base64.b64encode(buffer).decode('utf-8')
                if old_frame != encoded_frame:
                    ws_msg: TWSEventData = {
                                'event': 'new_frame',
                                'data': encoded_frame,
                            }
                    old_frame = encoded_frame
                    await cm.broadcast(ws_msg)
                classes = [detect_names[class_name] for class_name in classes]
                timestamp = time.time()
                if 'weapon' in classes:
                        ws_msg: TWSEventData = {
                                'event': 'weapon_detect',
                                'data': {'img': encoded_frame,'filename': f'{timestamp}.jpg', 'class': classes, 'poses': poses},
                        }
                        await cm.broadcast(ws_msg)
    except Exception as e:
        print(e)