# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_department fields

base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:49
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_department.py

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


xtb_depart_tree_fields: List = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "name", "type": ft.STR, "name": "label", "null": False},
    {"key": "description", "type": ft.STR, "name": "description", "null": True},
    {"key": "pid", "type": ft.INT, "name": "pid", "null": False},
    {"key": "leaf", "type": ft.BOOL, "name": "leaf", "null": True},
    {"key": "lock", "type": ft.BOOL, "name": "disabled", "null": True},
    {"key": "level", "type": ft.INT, "name": "level", "null": True},
    {"key": "dept_path", "type": ft.STR, "name": "deptPath", "null": True},
    {"key": "manage_rtx", "type": ft.SPLITLIST, "name": "manageRtx", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
]