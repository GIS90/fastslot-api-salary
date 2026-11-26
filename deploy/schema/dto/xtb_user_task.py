# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user_task fields

base_info:
    __author__ = PyGo
    __time__ = 2026/6/8 21:33
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user_task.py

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


xtb_user_task_detail_fields: List = [
    {"key": "rtx_id", "name": "rtxId"},
    {"key": "md5"},
    {"key": "api"},
    {"key": "name"},
    {"key": "data"},
    {"key": "data_value", "type": ft.STR, "name": "dataText", "null": False},
    {"key": "task"},
    {"key": "task_value", "type": ft.STR, "name": "taskText", "null": False},
    {"key": "cost"},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime"}
]

