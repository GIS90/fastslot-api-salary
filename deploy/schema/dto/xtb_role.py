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
from deploy.utils.enumeration import FieldTypeEnum as ft


xtb_role_list_fields = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "engname", "type": ft.STR, "name": "engname", "null": False},
    {"key": "chnname", "type": ft.STR, "name": "chnname", "null": False},
    {"key": "introduction", "type": ft.STR, "name": "introduction", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_role_detail_fields = [
    {"key": "md5"},
    {"key": "engname"},
    {"key": "chnname"},
    {"key": "introduction"},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True}
]


xtb_role_authority_fields = [
    {"key": "md5"},
    {"key": "authority", "type": ft.SPLITLIST, "name": "authority", "null": True},
]


xtb_role_download_fields = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "engname", "type": ft.STR, "name": "角色ID", "null": False},
    {"key": "chnname", "type": ft.STR, "name": "角色名称", "null": False},
    {"key": "introduction", "type": ft.STR, "name": "角色介绍", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True}
]

