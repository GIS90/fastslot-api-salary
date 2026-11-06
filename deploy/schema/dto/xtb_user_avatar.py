# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    dto fields of table xtb_user_avatar

base_info:
    __author__ = PyGo
    __time__ = 2026/11/06 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user_avatar.py

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


xtb_user_avatar_detail_fields: List = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "type", "type": ft.STR, "name": "type", "null": True},
    {"key": "summary", "type": ft.STR, "name": "summary", "null": True},
    {"key": "tag", "type": ft.STR, "name": "tag", "null": True},
    {"key": "url", "type": ft.STR, "name": "url", "null": False},
    {"key": "or_url", "type": ft.STR, "name": "orUrl", "null": False},
    {"key": "format", "type": ft.STR, "name": "format", "null": True},
    {"key": "width", "type": ft.INT, "name": "width", "null": True},
    {"key": "height", "type": ft.INT, "name": "height", "null": True},
    {"key": "size", "type": ft.INT, "name": "size", "null": True},
    {"key": "count", "type": ft.INT, "name": "count", "null": True},
    {"key": "status", "type": ft.BOOL, "name": "status", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
]

xtb_user_avatar_list_fields: List = xtb_user_avatar_detail_fields + [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
]
