# -*- coding: utf-8 -*-
"""App settings goes here."""


__all__ = [
    'settings',
]


import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """App settings."""

    INIT_LOG_DIR: bool = False  # удаление папки с логами при старте
    LOGGER_CONFIG: str = '../logger/logging-dev.yml'
    LOG_LEVEL: str = 'DEBUG'

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = 'localhost'
    SERVER_HOST: Union[AnyHttpUrl, str] = 'localhost'

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:8080', # type: ignore
        'http://127.0.0.1:8080', # type: ignore
        'http://127.0.0.1:8081', # type: ignore
        'http://localhost:8081'  # type: ignore
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'weapons_peoples'


    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
