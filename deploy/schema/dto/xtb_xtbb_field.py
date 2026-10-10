# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_xtbb_field fields

base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtbb_field.py

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


xtb_xtbb_field_list_fields: List = [
    {"key": "field", "type": ft.STR, "name": "field", "null": False},
    {"key": "name_zh", "type": ft.STR, "name": "nameZh", "null": False},
    {"key": "name_ch", "type": ft.STR, "name": "nameCh", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "xtbb", "type": ft.STR, "name": "xtbb", "null": False},
    {"key": "remark", "type": ft.STR, "name": "remark", "null": False},
    {"key": "width", "type": ft.FLOAT, "name": "width", "null": True},
    {"key": "fixed", "type": ft.STR, "name": "fixed", "null": True},
    {"key": "list", "type": ft.BOOL, "name": "list", "null": True},
    {"key": "list_type", "type": ft.STR, "name": "listType", "null": True},
    {"key": "export", "type": ft.BOOL, "name": "export", "null": True},
    {"key": "export_type", "type": ft.STR, "name": "exportType", "null": True},
    {"key": "null", "type": ft.BOOL, "name": "null", "null": True},
    {"key": "id_auto", "type": ft.BOOL, "name": "idAuto", "null": True},
    {"key": "extend", "type": ft.BOOL, "name": "extend", "null": True},
    {"key": "filter", "type": ft.STR, "name": "filter", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
]


xtb_xtbb_field_detail_fields: List = [
    {"key": "field"},
    {"key": "name_zh"},
    {"key": "name_ch"},
    {"key": "md5"},
    {"key": "xtbb"},
    {"key": "remark"},
    {"key": "width", "type": ft.FLOAT, "name": "width", "null": True},
    {"key": "fixed"},
    {"key": "list", "type": ft.BOOL, "name": "list", "null": True},
    {"key": "list_type"},
    {"key": "export", "type": ft.BOOL, "name": "export", "null": True},
    {"key": "export_type"},
    {"key": "null", "type": ft.BOOL, "name": "null", "null": True},
    {"key": "id_auto", "type": ft.BOOL, "name": "idAuto", "null": True},
    {"key": "extend", "type": ft.BOOL, "name": "extend", "null": True},
    {"key": "filter"},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
]


xtb_xtbb_field_view_fields: List = [
    {"key": "field"},
    {"key": "name_zh"},
    {"key": "name_ch"},
    {"key": "md5"},
    {"key": "xtbb"},
    {"key": "remark"},
    {"key": "width", "type": ft.FLOAT, "name": "width", "null": True},
    {"key": "fixed"},
    {"key": "list", "type": ft.BOOL, "name": "list", "null": True},
    {"key": "list_type"},
    {"key": "export", "type": ft.BOOL, "name": "export", "null": True},
    {"key": "export_type"},
    {"key": "null", "type": ft.BOOL, "name": "null", "null": True},
    {"key": "id_auto", "type": ft.BOOL, "name": "idAuto", "null": True},
    {"key": "extend", "type": ft.BOOL, "name": "extend", "null": True},
    {"key": "filter"},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True}
]
