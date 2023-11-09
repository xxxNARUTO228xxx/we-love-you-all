# -*- coding: utf-8 -*-
"""WebSocket endpoint."""

__all__ = [
    'ws_endpoint'
]

import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from core.ws_con_manager import TWSClientId, TWSEventData, WSConnectionManager

log = logging.getLogger('app.api.socket')

cm = WSConnectionManager()

router = APIRouter()

loop = asyncio.get_event_loop()



async def consume(cm: WSConnectionManager):
    """
    Отправк кадров с rtsp потока

    Args:
        cm (WSConnectionManager): сокеты.
    """

    log.info('Start websocket connect.')
    log.info('Start consuming')
    # finally:
    #     log.error('Stop consuming')


@router.on_event("startup")
async def startup() -> None:
    """Set up on startup."""
    asyncio.create_task(consume(cm))


@router.on_event("shutdown")
async def shutdown_event():
    """Stop all subscriptions."""


@router.websocket("/{client_id}")
async def ws_endpoint(
        ws: WebSocket,
        client_id: TWSClientId,
        # db: Session = Depends(deps.get_db),
):
    """Create socket connection."""

    await cm.connect(client_id, ws)

    try:
        while True:
                data: TWSEventData = await ws.receive_json()
                if data['event'] == 'echo':
                    msg = RESULT_FRAME
                    await cm.send_message(msg, client_id)

    except WebSocketDisconnect:
        cm.disconnect(client_id)


@router.get("/reload_clients")
async def reload_clients():
    """Перезагрузка страницы на всех клиентах."""

    log.info('Reloading all clients')
    msg: TWSEventData = {
        'event': 'reload',
        'data': {},
    }
    await cm.broadcast(msg)
