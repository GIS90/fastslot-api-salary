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


xtb_user_task_list_fields: List = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "api", "type": ft.STR, "name": "api", "null": False},
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "data", "type": ft.STR, "name": "data", "null": False},
    {"key": "data_value", "type": ft.STR, "name": "dataText", "null": False},
    {"key": "task", "type": ft.STR, "name": "task", "null": False},
    {"key": "task_value", "type": ft.STR, "name": "taskText", "null": False},
    {"key": "cost", "type": ft.FLOAT, "name": "cost", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


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


xtb_user_task_download_fields: List = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "create_time", "type": ft.STR, "name": "创建时间"},
    {"key": "rtx_id", "type": ft.STR, "name": "系统用户"},
    {"key": "name", "type": ft.STR, "name": "文件名称"},
    {"key": "md5", "type": ft.STR, "name": "MD5值"},
    {"key": "api", "type": ft.STR, "name": "接口名称"},
    {"key": "data_value", "type": ft.STR, "name": "下载类型"},
    {"key": "task_value", "type": ft.STR, "name": "任务状态"},
    {"key": "cost", "type": ft.FLOAT, "name": "耗时（单位：s）"},
]

