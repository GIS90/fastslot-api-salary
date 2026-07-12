# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/6/6 21:55
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtcs.py

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


xtb_xtcs_list_fields = [
    {"key": "key", "type": ft.STR, "name": "key", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "remark", "type": ft.STR, "name": "remark", "null": False},
    {"key": "value", "type": ft.STR, "name": "value", "null": False},
    {"key": "lock", "type": ft.BOOL, "name": "lock", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]


xtb_xtcs_detail_fields = [
    {"key": "key"},
    {"key": "md5"},
    {"key": "remark"},
    {"key": "value"},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]


xtb_xtcs_view_fields = [
    {"key": "key"},
    {"key": "md5"},
    {"key": "remark"},
    {"key": "value"},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True}
]

xtb_xtcs_download_fields =  [
    {"key": "key", "type": ft.STR, "name": "参数名称", "null": False},
    {"key": "remark", "type": ft.STR, "name": "参数说明", "null": False},
    {"key": "value", "type": ft.STR, "name": "参数值", "null": False},
    {"key": "lock", "type": ft.LOCK_TEXT, "name": "状态", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "更新人", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "更新时间", "null": True}
]