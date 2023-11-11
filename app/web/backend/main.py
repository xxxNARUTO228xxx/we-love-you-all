# -*- coding: utf-8 -*-
"""Main. Start here."""

import os
import sys
from http import HTTPStatus

sys.path.append('..')
sys.path.append(os.path.join('..', '..'))

import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from logger.utils import format_log_message
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from core.config import settings
from utils.other import get_uid

log = logging.getLogger('app')

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    redoc_url='/redoc',
    docs_url='/swagger',
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# log all requests
@app.middleware('http')
async def log_requests(request: Request, call_next):
    """Log all requests."""

    uid = get_uid()
    log.info(
        'req_id=%s start request. method=%s, path=%s',
        uid,
        request.method,
        request.url.path
    )

    start_time = time.time()
    try:
        response = await call_next(request)
    except RuntimeError as exc:
        if str(exc) == 'No response returned.' and await request.is_disconnected():
            log.warning(
                'Error `No response returned` detected. But client is disconnected.'
            )
            return Response(status_code=HTTPStatus.NO_CONTENT)
        else:
            raise

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    log.info(
        'req_id=%s completed_in=%s ms status_code=%s',
        uid,
        formatted_process_time,
        response.status_code
    )

    return response

# Vue app
DIST_ROOT = './view/static/dist/spa'
app.mount('/js',
          StaticFiles(directory=f'{DIST_ROOT}/js'),
          name='js')

app.mount('/css',
          StaticFiles(directory=f'{DIST_ROOT}/css'),
          name='css')

app.mount('/fonts',
          StaticFiles(directory=f'{DIST_ROOT}/fonts'),
          name='fonts')

app.mount('/icons',
          StaticFiles(directory=f'{DIST_ROOT}/icons'),
          name='icons')


@app.get('/')
async def index_page(request: Request):
    """Return index html."""

    return FileResponse(f'{DIST_ROOT}/index.html')

@app.get('/rtsp')
async def index_page(request: Request):
    """Return index html."""

    return FileResponse(f'{DIST_ROOT}/index.html')


# health
@app.get('/healthcheck')
async def healthcheck():
    """Check app health."""
    status = 'healthy'
    result = {'status': status}
    log.info(format_log_message('healthcheck', result))

    return result


app.include_router(api_router, prefix=settings.API_V1_STR)
