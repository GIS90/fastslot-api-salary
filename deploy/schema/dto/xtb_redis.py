# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    xtb redis fields

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = xtb_redis.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！！
Life is short, I use python.

------------------------------------------------
"""
from typing import List

from deploy.utils.enumeration import FieldTypeEnum as ft


xtb_redis_config_list_fields: List = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "md5", "type": ft.STR, "null": False},
    {"key": "name", "type": ft.STR, "null": False},
    {"key": "host", "type": ft.STR, "null": False},
    {"key": "port", "type": ft.INT, "null": False},
    {"key": "db", "type": ft.INT, "name": "db", "null": False},
    {"key": "password", "type": ft.STR, "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": False},
    {"key": "summary", "type": ft.STR, "null": True},
    {"key": "lock", "type": ft.BOOL, "null": False},
    {"key": "lock", "type": ft.BOOL_TEXT, "name": "lockText", "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
]


xtb_redis_config_detail_fields: List = xtb_redis_config_list_fields


xtb_redis_rule_list_fields: List = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "md5", "type": ft.STR, "null": False},
    {"key": "name", "type": ft.STR, "null": False},
    {"key": "redis_md5", "type": ft.STR, "name": "redisMd5", "null": False},
    {"key": "config_name", "type": ft.STR, "name": "configName", "null": True},
    {"key": "match", "type": ft.STR, "null": False},
    {"key": "pattern", "type": ft.STR, "null": False},
    {"key": "max_keys", "type": ft.INT, "name": "maxKeys", "null": False},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": False},
    {"key": "summary", "type": ft.STR, "null": True},
    {"key": "lock", "type": ft.BOOL, "null": False},
    {"key": "lock", "type": ft.BOOL_TEXT, "name": "lockText", "null": False},
    {"key": "last_clean_time", "type": ft.DATETIME, "name": "lastCleanTime", "null": True},
    {"key": "last_clean_count", "type": ft.INT, "name": "lastCleanCount", "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
]


xtb_redis_rule_detail_fields: List = xtb_redis_rule_list_fields
