# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_xtbb fields

base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtbb.py

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


xtb_xtbb_detail_fields: List = [
    {"key": "name"},
    {"key": "table"},
    {"key": "md5"},
    {"key": "remark"},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]

