# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_request fields

base_info:
    __author__ = PyGo
    __time__ = 2026/5/20 21:52
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_request.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.utils.enumeration import FieldTypeEnum as ft


profile_request_list_fields = [
    {"key": "ip", "type": ft.STR, "null": False},
    {"key": "method", "type": ft.STR, "null": True},
    {"key": "url", "type": ft.STR, "null": True},
    {"key": "cost", "type": ft.FLOAT, "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]