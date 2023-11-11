# -*- coding: utf-8 -*-
"""Base class for db model."""

__all__ = [
    'BaseClass',
]

from typing import Any

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseClass(object):
    """
    Base class for db model.

    Properties:
        id (Any): id.
    """

    metadata: Any
    id: Any
