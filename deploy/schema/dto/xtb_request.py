# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_request fields

base_info:
    __author__ = PyGo
    __time__ = 2026/5/20 21:52
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_request.py

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


profile_request_list_fields = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "ip", "type": ft.STR, "null": False},
    {"key": "method", "type": ft.STR, "null": False},
    {"key": "url", "type": ft.STR, "null": True},
    {"key": "cost", "type": ft.FLOAT, "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_request_list_fields = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId", "null": False},
    {"key": "md5", "type": ft.STR, "null": False},
    {"key": "ip", "type": ft.STR, "null": False},
    {"key": "method", "type": ft.STR, "null": False},
    {"key": "url", "type": ft.STR, "null": True},
    {"key": "cost", "type": ft.FLOAT, "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_request_detail_fields = [
    {"key": "md5"},
    {"key": "ip"},
    {"key": "method"},
    {"key": "url"},
    {"key": "params"},
    {"key": "path"},
    {"key": "full_path"},
    {"key": "host_url"},
    {"key": "url"},
    {"key": "cost", "type": ft.FLOAT},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_request_download_fields = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "engname", "type": ft.STR, "name": "角色ID", "null": False},
    {"key": "chnname", "type": ft.STR, "name": "角色名称", "null": False},
    {"key": "introduction", "type": ft.STR, "name": "角色介绍", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True}
]
