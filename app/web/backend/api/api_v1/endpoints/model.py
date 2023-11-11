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
responce_out = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
image_result = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'result'))

@router.post("/archive")
async def find_weapor_archive(file: UploadFile = File(...)) -> Any:
    """
    Api for archive.
    """
    log.info('Архив принят ')
    try:
        if file.filename.endswith('.zip'):
            archive_content = await file.read()
            with ZipFile(BytesIO(archive_content), 'r') as zip_file:
                for file_info in zip_file.infolist():
                    if file_info.filename.endswith('.wmv'):
                        zip_file.extract(file_info.filename, output_directory)
                    elif file_info.filename.endswith('.mp4'):
                        zip_file.extract(file_info.filename, output_directory)
                    elif file_info.filename.endswith('.avi'):
                        zip_file.extract(file_info.filename, output_directory)
                log.info('Видео определено ')
                log.info('Видео передано на обработку!')
                if os.path.exists(image_result):
                    shutil.rmtree(image_result)
                result = await find_gun.video_analyze(file_info.filename)
                extracted_file_path = os.path.join(output_directory, file_info.filename)
                os.remove(extracted_file_path)
                responce_out_file = os.path.join(responce_out, 'output_video.mp4')
   
        return FileResponse(responce_out_file, media_type='video/mp4')
    except Exception as e:
        log.info('Ошибка ', e)
        return JSONResponse(content=str(e), status_code=400)
    
@router.get("/rtsp")
async def stream_read(rtsp_url: str = '') -> Any:
    "Api for stream"
    try:
        if stop_event.is_set():
            stop_event.clear()
        asyncio.create_task(stream_analyze(rtsp_url))
        return {'items': 'rtsp поток запущен'}
    except Exception as e:
        return JSONResponse(content=str(e), status_code=400)
    

@router.get("/rtsp_stop")
async def stream_read(query: str = '') -> Any:
    "Api for stop stream"
    try:
        if query == 'stop':
            stop_event.set()
        return {'items': 'rtsp поток остановлен'}
    except Exception as e:
        return JSONResponse(content=str(e), status_code=400)
    

@router.get("/get_image")
async def stream_read(filename: str = '') -> Any:
    "Api for stop stream"
    try:

        if filename != '':
            image_path = os.path.join(image_result, filename)
        return  FileResponse(image_path, media_type='image/jpeg')
    except Exception as e:
        return JSONResponse(content=str(e), status_code=400)