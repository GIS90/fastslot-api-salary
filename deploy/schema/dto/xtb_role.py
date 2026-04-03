# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

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
from deploy.utils.enumeration import FieldTypeEnum as ft


xtb_role_list_fields = [
    {"key": "md5_id", "type": ft.STR, "name": "md5Id", "null": False},
    {"key": "engname", "type": ft.STR, "name": "engname", "null": False},
    {"key": "chnname", "type": ft.STR, "name": "chnname", "null": False},
    {"key": "authority", "type": ft.SPLITLIST, "name": "authority", "null": True},
    {"key": "introduction", "type": ft.STR, "name": "introduction", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True},
    {"key": "status", "type": ft.BOOLTEXT, "name": "status", "null": False},
]


xtb_role_detail_fields = [
    {"key": "md5_id"},
    {"key": "engname"},
    {"key": "chnname"},
    {"key": "introduction"},
]


xtb_role_authority_fields = [
    {"key": "md5_id"},
    {"key": "authority", "type": ft.SPLITLIST, "name": "authority", "null": True},
]
