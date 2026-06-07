# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_menu fields

base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:10
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_menu.py

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


xtb_menu_list_fields = [
    {"key": "id", "type": ft.INT, "name": "id", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "path", "type": ft.STR, "name": "path", "null": False},
    {"key": "title", "type": ft.STR, "name": "title", "null": False},
    {"key": "pid", "type": ft.INT, "name": "pid", "null": False},
    {"key": "level", "type": ft.INT, "name": "pid", "null": False},
    {"key": "component", "type": ft.STR, "name": "component", "null": False},
    {"key": "hidden", "type": ft.BOOL_TEXT, "name": "hidden", "null": True},
    {"key": "redirect", "type": ft.STR, "name": "redirect", "null": True},
    {"key": "icon", "type": ft.STR, "name": "icon", "null": True},
    {"key": "cache", "type": ft.BOOL_TEXT, "name": "cache", "null": True},
    {"key": "affix", "type": ft.BOOL_TEXT, "name": "affix", "null": True},
    {"key": "full", "type": ft.BOOL_TEXT, "name": "full", "null": True},
    {"key": "breadcrumb", "type": ft.BOOL_TEXT, "name": "breadcrumb", "null": True},
    {"key": "shortcut", "type": ft.BOOL_TEXT, "name": "shortcut", "null": True},
    {"key": "tag", "type": ft.STR, "name": "tag", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


xtb_tree_detail_fields = [
    {"key": "id", "type": ft.INT},
    {"key": "md5"},
    {"key": "name"},
    {"key": "path"},
    {"key": "title"},
    {"key": "pid", "type": ft.INT},
    {"key": "level", "type": ft.INT},
    {"key": "component"},
    {"key": "hidden", "type": ft.BOOL},
    {"key": "redirect", "null": True},
    {"key": "icon", "null": True},
    {"key": "cache", "type": ft.BOOL},
    {"key": "affix", "type": ft.BOOL},
    {"key": "full", "type": ft.BOOL},
    {"key": "breadcrumb", "type": ft.BOOL},
    {"key": "shortcut", "type": ft.BOOL, "null": True},
    {"key": "tag", "null": True},
    {"key": "order_id", "type": ft.INT}
]


xtb_menu_detail_fields = [
    {"key": "id", "type": ft.INT},
    {"key": "md5"},
    {"key": "name"},
    {"key": "path"},
    {"key": "title"},
    {"key": "pid", "type": ft.INT},
    {"key": "level", "type": ft.INT},
    {"key": "component"},
    {"key": "hidden", "type": ft.BOOL},
    {"key": "redirect", "null": True},
    {"key": "icon", "null": True},
    {"key": "cache", "type": ft.BOOL},
    {"key": "affix", "type": ft.BOOL},
    {"key": "full", "type": ft.BOOL},
    {"key": "breadcrumb", "type": ft.BOOL},
    {"key": "shortcut", "type": ft.BOOL, "null": True},
    {"key": "tag", "null": True},
    {"key": "order_id", "type": ft.INT, "name": "orderId"},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True},
    {"key": "update_rtx", "type": ft.STR, "name": "updateRtx", "null": True},
    {"key": "update_time", "type": ft.DATETIME, "name": "updateTime", "null": True}
]
