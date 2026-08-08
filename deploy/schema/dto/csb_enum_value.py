# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    csb_enum_value fields

base_info:
    __author__ = PyGo
    __time__ = 2026/7/12 20:17
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = csb_enum_value.py

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


csb_ev_list_fields: List = [
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "key", "type": ft.STR, "name": "key", "null": False},
    {"key": "value", "type": ft.STR, "name": "value", "null": False},
    {"key": "remark", "type": ft.STR, "name": "remark", "null": False},
    {"key": "lock", "type": ft.BOOL, "name": "status", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]


csb_ev_detail_fields: List = [
    {"key": "name"},
    {"key": "md5"},
    {"key": "key"},
    {"key": "value"},
    {"key": "remark"},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]


xtb_ev_download_fields: List =  [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "ek_key", "type": ft.STR, "name": "字典分类标识", "null": False},
    {"key": "ek_value", "type": ft.STR, "name": "字典分类名称", "null": False},
    {"key": "ev_key", "type": ft.STR, "name": "字典枚举标识", "null": False},
    {"key": "ev_value", "type": ft.STR, "name": "字典枚举名称", "null": False},
    {"key": "remark", "type": ft.STR, "name": "字典枚举描述", "null": False},
    {"key": "lock", "type": ft.LOCK_TEXT, "name": "状态", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "顺序编号", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "更新人", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "更新时间", "null": True}
]