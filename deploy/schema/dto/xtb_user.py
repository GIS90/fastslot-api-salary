# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user fields

base_info:
    __author__ = PyGo
    __time__ = 2025/12/17 22:37
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user.py

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


xtb_user_list_fields: List = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "sex", "type": ft.STR, "name": "sex", "null": False},
    {"key": "email", "type": ft.STR, "name": "email", "null": False},
    {"key": "phone", "type": ft.STR, "name": "phone", "null": False},
    {"key": "avatar", "type": ft.STR, "name": "avatar", "null": False},
    {"key": "introduction", "type": ft.STR, "name": "introduction", "null": True},
    {"key": "department", "type": ft.STR, "name": "department", "null": False},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "status", "type": ft.BOOL, "name": "status", "null": False}
]


xtb_user_detail_fields: List = [
    {"key": "id", "type": ft.INT},
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId"},
    {"key": "name"},
    {"key": "md5"},
    {"key": "sex"},
    {"key": "email"},
    {"key": "phone"},
    {"key": "avatar"},
    {"key": "introduction"},
    {"key": "role", "type": ft.SPLITLIST, "name": "role", "null": True},
    # {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    # {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    # {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    # {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True}
]


xtb_user_login_fields: List = [
    {"key": "rtx_id", "type": ft.STR, "name": "rtxId"},
    {"key": "password"},
    {"key": "name"},
    {"key": "sex"},
    {"key": "email"},
    {"key": "phone"},
    {"key": "avatar"},
    {"key": "introduction"},
    {"key": "role", "type": ft.SPLITLIST, "null": True},
    {"key": "status", "type": ft.BOOL},
]


xtb_user_download_fields: List = [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "rtx_id", "type": ft.STR, "name": "账号", "null": True},
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

