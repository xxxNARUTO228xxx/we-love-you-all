# -*- coding: utf-8 -*-

"""Logger utils."""

__all__ = [
    'init_logger',
    'format_log_message',
    'LoggerLevelFilter',
    'UDPLogstashHandler'
]

import bisect
import logging
import logging.config
import os
import pyclbr
import shutil
import sys
import traceback
from logging import LogRecord
from logging.handlers import DatagramHandler
from types import TracebackType
from typing import Optional, Type

import yaml

NO_CLASS = '<>'
NOT_AVAILABLE = '<>'


class UDPLogstashHandler(DatagramHandler, object):
    """Send data to Logstash with UDP."""

    def __init__(self,
                 host,
                 port=5000,
                 fmt_config={}):

        super().__init__(host, port)

    def makePickle(self, record: LogRecord):
        """Convert LogRecord to bytes."""

        b = bytes(self.format(record), 'utf-8')

        return b + b'\n'


class LogModule:
    """Add module name to log record."""

    def __init__(self, module):
        mod = pyclbr.readmodule_ex(module)
        line2func = []

        for classname, cls in mod.items():
            if isinstance(cls, pyclbr.Function):
                line2func.append((cls.lineno, NO_CLASS, cls.name))
            else:
                for methodname, start in cls.methods.items():
                    line2func.append((start, classname, methodname))

        line2func.sort()
        keys = [item[0] for item in line2func]
        self.line2func = line2func
        self.keys = keys

    def line_to_class(self, lineno):
        index = bisect.bisect(self.keys, lineno) - 1
        return self.line2func[index][1]


def lookup_class(module: str, funcname: str, lineno: int) -> str:
    """
    Lookup for module name and line number.

    Args:
        module (str): module name.
        funcname (str): function name.
        lineno (int): line number.

    Returns:
        str: class name
    """

    if funcname == '<module>':
        return NO_CLASS

    try:
        return LogModule(module).line_to_class(lineno)  # type: ignore
    except Exception:
        return NOT_AVAILABLE


class LogRecordExtended(LogRecord):
    """Extension of LogRecord."""

    className: str
    funcName: str


class LogRecordFactory:
    """Create and extend LogRecord."""

    def __init__(self, app_name: Optional[str] = None):
        self.app_name = app_name

    def __call__(self, *args, **kwargs) -> LogRecordExtended:
        record = LogRecordExtended(*args, **kwargs)

        record.className = lookup_class(
            record.module, record.funcName, record.lineno,
        )

        if record.className != NO_CLASS:
            record.funcName = f'{record.className}.{record.funcName}'

        if record.msg is not None:
            record.msg = str(record.msg).replace('\n', '')
            record.msg = str(record.msg).replace('\r', '')

        if self.app_name is not None:
            record.name = self.app_name + '.' + record.name

        return record


def exception_handler(exc_type: Type[BaseException], value: BaseException, tb: Optional[TracebackType]):
    """
    Обработчик исключений.

    Для того чтобы выводить в логгер не перехваченные ошибки приложения.

    Args:
        exc_type (type): Тип исключения.
        value (Exception): Ошибка.
        tb (traceback): Стек вызова.
    """

    logging.exception(' '.join(traceback.format_exception(exc_type, value, tb)))


def init_logger(config_file: str = './logging.yml',
                delete_log_dir: bool = False,
                log_dir: str = './log',
                app_name: Optional[str] = None):
    """
    Инициализировать логгер.

    Args:
        config_file(str, optional): *.yml файл конфига логгера.
                Defaults to './logging.yml'
        delete_log_dir(bool, optional): Удалять папку с файлами логов на старте
                (полезно если вы не хотите копить старые логи при разработке).
        log_dir(str, optional): Путь к папке с файлами логов. Defaults to './log'
        app_name(str, optional): Префикс для имени лога.
            Без него имя лога может быть таким - app.server, станет таким - my_service.app.server
            Это нужно для разделения логов, например в Elastic - куда сливаются логи всех приложений.
            Если не задан - не добавляется.
            Defaults to None.
    """

    with open(config_file, 'r') as f:
        log_config = yaml.safe_load(f.read())

        # filename becomes {log_dir}/{filename}
        K_FN = 'filename'
        K_HANDLER = 'handlers'
        CFG_PRE = 'cfg://'
        has_ny_file_output = False
        for h_name, h_conf in log_config[K_HANDLER].items():
            if K_FN in h_conf:
                has_ny_file_output = True
                fn = h_conf[K_FN]
                # if filename - link to vars
                if fn.startswith(CFG_PRE):
                    pt = fn.replace(CFG_PRE, '')
                    k_vars, k_filename = pt.split('.')
                    fn = log_config[k_vars][k_filename]

                log_config[K_HANDLER][h_name][K_FN] = f'{log_dir}/{fn}'

        if has_ny_file_output:
            if delete_log_dir:
                if os.path.exists(log_dir):
                    shutil.rmtree(log_dir)
                    print(f'Remove logging dir: "{os.getcwd()}/{log_dir}"')

            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                print(f'Create logging dir: "{os.getcwd()}/{log_dir}"')

        logging.setLogRecordFactory(LogRecordFactory(app_name))
        logging.config.dictConfig(log_config)

    # Install exception handler
    sys.excepthook = exception_handler


def format_log_message(*args) -> str:
    """
    Форматирует сообщения для лога.

    Конкатенирует все аргументы функции в строку.

    Returns:
        str: line
    """

    return '\t'.join([str(s) for s in args])


class LoggerLevelFilter():
    """
    Filter for logger level.

    If you want to send different logger levels
    to different handlers(different files, with formats)

    Arguments:
        level(str): one of logger levels(`DEBUG`, `INFO` e.t.c.)

        and_above(bool): set to `False` if you want to filter only one level
            `DEBUG` level == 10
            (https://docs.python.org/3.6/library/logging.html #logging-levels)
            when call `logger.debug('some')`
            when set to `True` will show only `DEBUG` messages(level == 10)
            when `False` will show more levels
                - `DEBUG`, `INFO`, `WARN`...(level >= 10)

    """

    def __init__(self, level=0, and_above=True):
        self.level = logging._checkLevel(level)
        self.and_above = and_above

    def filter(self, record: LogRecord):
        """
        Format record with `self.level`.

        Args:
            record (LogRecord): log record

        Returns:
            bool: compared to `self.level`
        """

        if self.and_above:
            return record.levelno >= self.level
        else:
            return record.levelno == self.level
