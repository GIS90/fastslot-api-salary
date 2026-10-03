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


xtb_xtbb_list_fields: List = [
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "table", "type": ft.STR, "name": "table", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "remark", "type": ft.STR, "name": "remark", "null": False},
    {"key": "mode", "type": ft.BOOL, "name": "mode", "null": True}
]


xtb_xtbb_detail_fields: List = [
    {"key": "name"},
    {"key": "table"},
    {"key": "md5"},
    {"key": "remark"},
    {"key": "mode", "type": ft.BOOL, "name": "mode", "null": True}
]


xtb_xtbb_view_fields: List = [
    {"key": "name"},
    {"key": "table"},
    {"key": "md5"},
    {"key": "remark"},
    {"key": "mode", "type": ft.BOOL, "name": "mode", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True}
]

xtb_xtbb_download_fields: List = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "name", "type": ft.STR, "name": "报表名称", "null": False},
    {"key": "table", "type": ft.STR, "name": "数据库表名", "null": False},
    {"key": "remark", "type": ft.STR, "name": "报表说明", "null": False},
    {"key": "mode", "type": ft.BOOL, "name": "宽度模式", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "更新人", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "更新时间", "null": True}
]
