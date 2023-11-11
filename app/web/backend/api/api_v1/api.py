# -*- coding: utf-8 -*-
"""API routes."""

__all__ = [
    'api_router',
]

from fastapi import APIRouter

from api.api_v1.endpoints import socket, model

api_router = APIRouter()


api_router.include_router(socket.router, prefix="/ws", tags=["socket"])
api_router.include_router(model.router, prefix="/model", tags=["model"])

