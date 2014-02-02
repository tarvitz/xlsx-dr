"""
Helpers
"""
# coding: utf-8
from datetime import datetime


def encoder(obj):
    """ helper for json encode

    >>> encoder(datetime(2014, 01, 01, 10, 0, 0))
    '2014-01-01T10:00:00'
    >>> encoder(datetime(2014, 01, 01, 10, 34, 12))
    '2014-01-01T10:34:12'

    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
