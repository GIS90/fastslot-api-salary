# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    salary_dtalk fields

base_info:
    __author__ = PyGo
    __time__ = 2026/11/19 13:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = salary_dtalk.py

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


# 钉钉消息通知-详情字段
salary_dtalk_message_detail_fields: List = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "file_name", "type": ft.STR, "name": "fileName", "null": False},
    {"key": "cur_sheet", "type": ft.STR, "name": "curSheet", "null": True},
    {"key": "nsheet", "type": ft.INT, "name": "nsheet", "null": True},
]

# 钉钉机器人-详情字段
salary_dtalk_robot_detail_fields: List = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "key", "type": ft.STR, "name": "key", "null": False},
    {"key": "secret", "type": ft.STR, "name": "secret", "null": False},
    {"key": "select", "type": ft.BOOL, "name": "select", "null": True},
    {"key": "description", "type": ft.STR, "name": "description", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
]
