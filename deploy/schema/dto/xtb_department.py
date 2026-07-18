# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_department fields

base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:49
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_department.py

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


xtb_depart_tree_fields: List = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "name", "type": ft.STR, "name": "label", "null": False},
    {"key": "description", "type": ft.STR, "name": "description", "null": True},
    {"key": "pid", "type": ft.INT, "name": "pid", "null": False},
    {"key": "leaf", "type": ft.BOOL, "name": "leaf", "null": True},
    {"key": "lock", "type": ft.BOOL, "name": "disabled", "null": True},
    {"key": "level", "type": ft.INT, "name": "level", "null": True},
    {"key": "dept_path", "type": ft.STR, "name": "deptPath", "null": True},
    {"key": "manage_rtx", "type": ft.SPLITLIST, "name": "manageRtx", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
]


xtb_depart_download_fields: List = [
    {"key": "id", "type": ft.INT, "name": "部门ID", "null": True},
    {"key": "md5", "type": ft.STR, "name": "部门MD5", "null": True},
    {"key": "name", "type": ft.STR, "name": "部门名称", "null": True},
    {"key": "description", "type": ft.STR, "name": "部门描述", "null": True},
    {"key": "pid", "type": ft.INT, "name": "上级PID", "null": False},
    {"key": "leaf", "type": ft.BOOL_TEXT, "name": "是否叶子节点", "null": True},
    {"key": "lock", "type": ft.LOCK_TEXT, "name": "状态", "null": True},
    {"key": "level", "type": ft.INT, "name": "部门级别", "null": True},
    {"key": "dept_path", "type": ft.STR, "name": "部门路径", "null": True},
    {"key": "manage_rtx", "type": ft.SPLITLIST, "name": "管理员（RTX列表）", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "排序编号", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True},
]

