# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user fields

base_info:
    __author__ = PyGo
    __time__ = 2025/12/17 22:37
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user.py

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


xtb_user_detail_fields: List = [
    {"key": "id", "type": ft.INT},
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId"},
    {"key": "name"},
    {"key": "md5"},
    {"key": "sex"},
    {"key": "email"},
    {"key": "phone"},
    {"key": "department", "null": True},
    {"key": "avatar"},
    {"key": "introduction"},
    {"key": "role", "type": ft.SPLITLIST, "name": "role", "null": True}
]


xtb_user_login_fields: List = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId"},
    {"key": "password"},
    {"key": "name"},
    {"key": "sex"},
    {"key": "email"},
    {"key": "phone"},
    {"key": "avatar"},
    {"key": "introduction"},
    {"key": "role", "type": ft.SPLITLIST, "null": True},
    {"key": "status", "type": ft.BOOL},
]

