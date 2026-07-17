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
from typing import List
from deploy.utils.enumeration import FieldTypeEnum as ft


profile_request_list_fields: List = [
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "ip", "type": ft.STR, "null": False},
    {"key": "method", "type": ft.STR, "null": False},
    {"key": "url", "type": ft.STR, "null": True},
    {"key": "cost", "type": ft.FLOAT, "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_request_list_fields: List = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId", "null": False},
    {"key": "md5", "type": ft.STR, "null": False},
    {"key": "ip", "type": ft.STR, "null": False},
    {"key": "method", "type": ft.STR, "null": False},
    {"key": "url", "type": ft.STR, "null": True},
    {"key": "cost", "type": ft.FLOAT, "null": False},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_request_detail_fields: List = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId", "null": False},
    {"key": "md5"},
    {"key": "ip"},
    {"key": "method"},
    {"key": "url"},
    {"key": "params", "null": True},
    {"key": "path"},
    {"key": "full_path"},
    {"key": "host_url"},
    {"key": "url"},
    {"key": "cost", "type": ft.FLOAT},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_request_download_fields: List = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True},
    {"key": "rtx_id", "type": ft.STR, "name": "系统用户", "null": True},
    {"key": "ip", "type": ft.STR, "name": "IP来源", "null": True},
    {"key": "method", "type": ft.STR, "name": "请求方式", "null": True},
    {"key": "url", "type": ft.STR, "name": "请求URL", "null": True},
    {"key": "path", "type": ft.STR, "name": "请求路径", "null": True},
    {"key": "params", "type": ft.STR, "name": "请求参数", "null": True},
    {"key": "cost", "type": ft.FLOAT, "name": "耗时（单位：s）", "null": True}
]
