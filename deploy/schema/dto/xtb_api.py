# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_api fields

base_info:
    __author__ = PyGo
    __time__ = 2026/7/20 00:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_api.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import List
from deploy.utils.enumeration import FieldTypeEnum as ft


xtb_api_list_fields: List = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "blueprint", "type": ft.STR, "name": "blueprint", "null": False},
    {"key": "apiname", "type": ft.STR, "name": "apiname", "null": False},
    {"key": "endpoint", "type": ft.STR, "name": "endpoint", "null": False},
    {"key": "path", "type": ft.STR, "name": "path", "null": False},
    {"key": "method", "type": ft.STR, "name": "method", "null": False},
    {"key": "short", "type": ft.STR, "name": "short", "null": True},
    {"key": "long", "type": ft.STR, "name": "long", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
]


xtb_api_detail_fields: List = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "blueprint", "type": ft.STR, "name": "blueprint", "null": False},
    {"key": "apiname", "type": ft.STR, "name": "apiname", "null": False},
    {"key": "endpoint", "type": ft.STR, "name": "endpoint", "null": False},
    {"key": "path", "type": ft.STR, "name": "path", "null": False},
    {"key": "method", "type": ft.STR, "name": "method", "null": False},
    {"key": "short", "type": ft.STR, "name": "short", "null": True},
    {"key": "long", "type": ft.STR, "name": "long", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
]


xtb_api_download_fields: List = [
    {"key": "blueprint", "type": ft.STR, "name": "blueprint", "null": False},
    {"key": "apiname", "type": ft.STR, "name": "apiname", "null": False},
    {"key": "endpoint", "type": ft.STR, "name": "endpoint", "null": False},
    {"key": "path", "type": ft.STR, "name": "path", "null": False},
    {"key": "method", "type": ft.STR, "name": "method", "null": False},
    {"key": "short", "type": ft.STR, "name": "short", "null": True},
    {"key": "long", "type": ft.STR, "name": "long", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
]
