# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_role fields

base_info:
    __author__ = PyGo
    __time__ = 2026/4/2 23:38
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_role.py

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


xtb_role_detail_fields: List = [
   {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "engname", "type": ft.STR, "name": "engname", "null": False},
    {"key": "chnname", "type": ft.STR, "name": "chnname", "null": False},
    {"key": "introduction", "type": ft.STR, "name": "introduction", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
    # {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    # {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    # {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    # {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True}
]

