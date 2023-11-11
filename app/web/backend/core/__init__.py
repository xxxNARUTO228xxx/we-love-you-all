# -*- coding: utf-8 -*-
"""All imports from files."""

import logging

from logger.utils import init_logger

from .config import settings

init_logger(
    config_file=settings.LOGGER_CONFIG,
    delete_log_dir=settings.INIT_LOG_DIR,
    app_name='weapon_people',
)

log = logging.getLogger('app')
log.setLevel(settings.LOG_LEVEL)

log.info('--NEW START--')
