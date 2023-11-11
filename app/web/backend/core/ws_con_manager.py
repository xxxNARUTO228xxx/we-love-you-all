# -*- coding: utf-8 -*-
"""Web socket connection manager."""


__all__ = [
    'TActiveConnections',
    'TWSEventData',
    'TWSClientId',
    'WSConnectionManager',
]

from typing import Any, Dict, Union

from fastapi import WebSocket, WebSocketDisconnect
from typing_extensions import TypedDict


class TActiveConnections(TypedDict):
    """
    Active ws. connections.

    Args:
        connection (WebSocket): connection.
    """

    connection: WebSocket


class TWSEventData(TypedDict):
    """
    TWSEvent model.

    Args:
        event (str): event name e.g. user_message
        data (Dict[str, Any]): some data
    """

    event: str
    data: Any


TWSClientId = Union[int, str]


class WSConnectionManager:
    """Connection manager for WebSockets."""

    def __init__(self):
        self.connections: Dict[TWSClientId, TActiveConnections] = {}

    async def connect(self, client_id: TWSClientId, websocket: WebSocket):
        """Connect."""
        await websocket.accept()
        self.connections[client_id] = {
            'connection': websocket,
        }

    def disconnect(self, client_id: TWSClientId):
        """Disconnect."""
        if client_id in self.connections:
            del self.connections[client_id]

    async def broadcast(self, message: TWSEventData):
        """Send message for all active clients."""
        for client_id in self.connections.keys():
            try:
                await self.send_message(message, client_id)
            except WebSocketDisconnect:
                self.disconnect(client_id)

    async def send_message(self, message: TWSEventData, client_id: TWSClientId):
        """Send message to client."""

        ws: WebSocket = self.connections[client_id]['connection']

        await ws.send_json(message)
