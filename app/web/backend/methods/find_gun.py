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
    path_detect_model = os.path.join(script_directory, '..', 'yolo', 'yolovX.pt')
    path_cls_model = os.path.join(script_directory, '..', 'yolo', 'yolovCLS.pt')
    model_detect = YOLO(path_detect_model)
    model_cls = YOLO(path_cls_model)
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
            frame_crop = frame.copy()
            frame_area = frame.shape[0] * frame.shape[1]
            if frameId % math.floor(frame_rate) == 1:
                results = model_detect(frame, conf=0.4, device="0")
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
                                probs = results_cls[0].probs.data.cpu().numpy()
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
                    timestamp = int(time.time())
                    _, buffer = cv.imencode('.jpg', frame_with_boxes)
                    encoded_frame = base64.b64encode(buffer).decode('utf-8')
                    classes = [detect_names[class_name] for class_name in classes]
                    if 'weapon' in classes:
                        print(results[0].boxes.conf)
                        ws_msg: TWSEventData = {
                                'event': 'video_weapon',
                                'data': {'img': encoded_frame,'filename': f'{timestamp}.jpg', 'class': classes, 'poses': poses},
                        }
                        await cm.broadcast(ws_msg)
                ws_msg: TWSEventData = {
                                'event': 'progress',
                                'data': {'progress': processed},
                        }
                await cm.broadcast(ws_msg)
    except Exception as e:
        print(e)