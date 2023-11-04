import os
from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    TITLE: str = 'Api Service for garbage analyzer'
    DESCRIPTION: str = '''Development of an algorithm for counting the number of unique objects 
    of each category of solid waste, focusing on the provided data (RGB + multispectral images).'''
    VERSION: str = '0.0'

    DEBUG: bool = os.environ.get('DEBUG', True)
    TIME_ZONE: str = 'UTC'

    DATETIME_FORMAT: str = os.environ.get('DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S.%f%z')
    URL: str = os.environ.get('URL', '')

    POSTGRES_CONNECT: str = os.environ['POSTGRES_CONNECT']
    SCHEMES: list = ('public', 'auth', 'analyzer_model')
    POOL: int = os.environ.get('POOL', 50)
    MAX_OVER: int = os.environ.get('MAX_OVER', 100)

    ORIGINS: list = ['*', 'http:/localhost']
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list = ['*']
    ALLOW_HEADERS: list = ['*']

    STATIC_FILES: str = os.environ.get('STATIC_FILES', '/code/static')

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES:', 60 * 60 * 24 * 7))
    ALGORITHM: str = os.environ.get('ALGORITHM', '"HS256"')
    SECURITY_KEY: str = os.environ['SECURITY_KEY']

    class Config:
        case_sensitive = True


api_settings = ApiSettings()
