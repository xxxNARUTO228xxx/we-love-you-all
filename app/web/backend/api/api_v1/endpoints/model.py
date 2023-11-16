# -*- coding: utf-8 -*-
"""API."""

__all__ = [

]

import logging
import shutil
from zipfile import ZipFile
from typing import Any
from io import BytesIO
import asyncio
import os

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from methods import find_gun
from methods.stream_search import stream_analyze, stop_event

router = APIRouter()
log = logging.getLogger('app')

output_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'video'))
output_directory_imgs = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'images_out'))
responce_out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
image_result = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'result'))


@router.post("/one_shot_predict")
async def create_upload_file(file: UploadFile = File(...)):
    """
    Интеграция с внешними сервисами - предсказание на основе одного изображения
    ----------
    file - изображение для предсказания

    Возвращает JSONResponse
    -------
    """
    try:
        temp_file_path = f"{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        os.makedirs(output_directory_imgs, exist_ok=True)
        target_path = os.path.join(output_directory_imgs, temp_file_path)
        os.replace(temp_file_path, target_path)
        result = await find_gun.image_analyze(target_path)

        return result
    except Exception as e:
        log.info('Ошибка ', e)
        return JSONResponse(content=str(e), status_code=400)


@router.post("/video_predict")
async def find_weapor_archive(file: UploadFile = File(...)):
    """
        Интеграция с внешними сервисами - предсказание на основе видео
        ----------
        file - видео для предсказания

        Возвращает JSONResponse
        -------
        """
    try:
        temp_file_path = f"{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
        os.replace(temp_file_path, os.path.join(output_directory, temp_file_path))
        result = await find_gun.video_analyze(temp_file_path)
        response_out_file = os.path.join(responce_out, 'output_video.mp4')

        return FileResponse(response_out_file, media_type='video/mp4')

    except Exception as e:
        log.info('Ошибка ', e)
        return JSONResponse(content=str(e), status_code=400)


@router.post("/archive")
async def find_weapor_archive(file: UploadFile = File(...)):
    """
           Обработка видео
           ----------
           file - видео для предсказания

           Возвращает JSONResponse
           -------
     """
    try:
        temp_file_path = f"{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())
        os.replace(temp_file_path, os.path.join(output_directory, temp_file_path))
        result = await find_gun.video_analyze(temp_file_path)
        response_out_file = os.path.join(responce_out, 'output_video.mp4')

        return FileResponse(response_out_file, media_type='video/mp4')

    except Exception as e:
        log.info('Ошибка ', e)
        return JSONResponse(content=str(e), status_code=400)


@router.get("/rtsp")
async def stream_read(rtsp_url: str = '') -> Any:
    """
              Обработка RTSP потока
              ----------
              rtsp_url - адрес видеокамеры

              Возвращает JSONResponse
              -------
    """
    try:
        if stop_event.is_set():
            stop_event.clear()
        asyncio.create_task(stream_analyze(rtsp_url))
        return {'items': 'rtsp поток запущен'}
    except Exception as e:
        return JSONResponse(content=str(e), status_code=400)


@router.get("/rtsp_stop")
async def stream_read(query: str = '') -> Any:
    """
          Остановка потока с камеры
          ----------
          query - запрос со статусом stop

          Возвращает JSONResponse
          -------
    """
    try:
        if query == 'stop':
            stop_event.set()
        return {'items': 'rtsp поток остановлен'}
    except Exception as e:
        return JSONResponse(content=str(e), status_code=400)


@router.get("/get_image")
async def stream_read(filename: str = '') -> Any:
    """
    Получение изображения в веб сервис
    :param filename:
    :return:
    """
    try:

        if filename != '':
            image_path = os.path.join(image_result, filename)
        return FileResponse(image_path, media_type='image/jpeg')
    except Exception as e:
        return JSONResponse(content=str(e), status_code=400)
