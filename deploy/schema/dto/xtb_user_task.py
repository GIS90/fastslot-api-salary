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
from deploy.utils.enumeration import FieldTypeEnum as ft


xtb_user_task_list_fields = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "api", "type": ft.STR, "name": "api", "null": False},
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "data", "type": ft.STR, "name": "data", "null": False},
    {"key": "task", "type": ft.STR, "name": "task", "null": False},
    {"key": "cost", "type": ft.FLOAT, "name": "cost", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_user_task_detail_fields = [
    {"key": "rtx_id"},
    {"key": "md5"},
    {"key": "api"},
    {"key": "name"},
    {"key": "data"},
    {"key": "task"},
    {"key": "cost"},
    {"key": "create_time", "type": ft.DATETIME},
    {"key": "update_time", "type": ft.DATETIME},
    {"key": "status", "type": ft.BOOL},
]


xtb_user_task_download_fields = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "rtx_id", "type": ft.STR, "name": "用户账号", "null": True},
    {"key": "name", "type": ft.STR, "name": "用户昵称", "null": True},
    {"key": "phone", "type": ft.STR, "name": "电话", "null": True},
    {"key": "email", "type": ft.STR, "name": "邮箱", "null": True},
    {"key": "sex", "type": ft.STR, "name": "性别", "null": True},
    {"key": "avatar", "type": ft.STR, "name": "头像URL地址", "null": True},
    {"key": "department", "type": ft.STR, "name": "部门名称", "null": True},
    {"key": "introduction", "type": ft.STR, "name": "个性签名", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True},
    {"key": "status", "type": ft.USER_STATUS_TEXT, "name": "状态", "null": True},
]

