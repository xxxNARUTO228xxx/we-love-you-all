# -*- coding: utf-8 -*-
"""Утилиты."""

__all__ = [
    'get_uid',
]

import random
import string
import time
from typing import Union

UID_ALPHABET_LETTERS = string.ascii_lowercase
UID_ALPHABET = UID_ALPHABET_LETTERS + string.digits


def get_uid(k: int = 8, add_date: bool = True, digits_only: bool = False) -> Union[str, int]:
    """
    Создать UID.

    Возвращает случайный uid длины `k` из алфавита `UID_ALPHABET`.
    Первый символ - всегда буква из `UID_ALPHABET_LETTERS`

    Args:
        k (int, optional): uid length. Defaults to 8.
        add_date (bool, optional): add date to uid. Defaults to True.
        digits_only (bool, optional): uid from digits only. Defaults to False.

    Returns:
        stUnion[str, int]r: UID. Int if digits_only == True
    """

    if digits_only:
        uid = ''.join([str(random.randint(0, 9)) for _ in range(k)])  # nosec
    else:
        uid = random.choices(UID_ALPHABET_LETTERS, k=1)[0]  # nosec
        uid += ''.join(random.choices(UID_ALPHABET, k=k - 1))  # nosec
    if add_date:
        uid += str(int(time.time() * 1000000))

    if digits_only:
        uid = int(uid)  # type: ignore

    return uid
