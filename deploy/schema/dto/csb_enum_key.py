# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    csb_enum_key fields

base_info:
    __author__ = PyGo
    __time__ = 2026/7/12 20:17
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = csb_enum_key.py

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


csb_ek_list_fields: List = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "key", "type": ft.STR, "name": "key", "null": False},
    {"key": "remark", "type": ft.STR, "name": "remark", "null": False},
    {"key": "lock", "type": ft.BOOL, "name": "status", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]


csb_ek_detail_fields: List = [
    {"key": "md5"},
    {"key": "key"},
    {"key": "remark"},
    {"key": "introduction"},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]