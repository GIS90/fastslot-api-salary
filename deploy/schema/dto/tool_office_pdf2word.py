# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    tool_office_pdf2word fields

base_info:
    __author__ = PyGo
    __time__ = 2026/8/8 17:17
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = tool_office_pdf2word.py

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


tool_office_pdf2word_list_fields: List = [
    {"key": "name", "type": ft.STR, "name": "name", "null": False},
    {"key": "store_name", "type": ft.STR, "name": "storeName", "null": False},
    {"key": "transfer_name", "type": ft.STR, "name": "transferName", "null": False},
    {"key": "md5", "type": ft.STR, "name": "md5", "null": False},
    {"key": "transfer", "type": ft.BOOL_TEXT, "null": False},
    {"key": "transfer_time", "type": ft.STR, "name": "transferTime", "null": True},
    {"key": "transfer_url", "type": ft.STR, "name": "transferUrl", "null": True},
    {"key": "mode", "type": ft.BOOL, "name": "mode", "null": True},
    {"key": "start", "type": ft.INT, "name": "start", "null": True},
    {"key": "end", "type": ft.INT, "name": "end", "null": True},
    {"key": "pages", "type": ft.STR, "name": "pages", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "createRtx", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "createTime", "null": True}
]


tool_office_pdf2word_detail_fields: List = [
    {"key": "md5"},
    {"key": "mode", "type": ft.BOOL},
    {"key": "start", "type": ft.INT},
    {"key": "end", "type": ft.INT},
    {"key": "pages", "type": ft.STR}
]


tool_office_pdf2word_download_fields: List =  [
    {"key": "id", "type": ft.INT, "name": "序号", "null": True},
    {"key": "name", "type": ft.STR, "name": "文件名", "null": False},
    {"key": "store_name", "type": ft.STR, "name": "文件存储名称", "null": False},
    {"key": "transfer_name", "type": ft.STR, "name": "文件转换名称", "null": False},
    {"key": "transfer", "type": ft.BOOL_TEXT, "转换状态": False},
    {"key": "transfer_time", "type": ft.STR, "name": "转换时间", "null": True},
    {"key": "transfer_url", "type": ft.STR, "name": "转换文件下载地址", "null": True},
    {"key": "mode", "type": ft.BOOL, "name": "转换模式", "null": True},
    {"key": "start", "type": ft.INT, "name": "起始页码", "null": True},
    {"key": "end", "type": ft.INT, "name": "结束页码", "null": True},
    {"key": "pages", "type": ft.STR, "name": "转换页码", "null": True},
    {"key": "create_rtx", "type": ft.STR, "name": "创建人", "null": True},
    {"key": "create_time", "type": ft.DATETIME, "name": "创建时间", "null": True}
]