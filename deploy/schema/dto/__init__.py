# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    schema -> dto[Modal数据传输API Route对象]：Data Transfer Object

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:44
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = __init__.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""

"""
字段含义：
- key: 模型中的属性名；
- type: 属性的数据类型（如"str", "int", "datetime"等），具体含义参考FieldTypeEnum
- name: 输出字典中对应的键名
- null: 是否允许为空，默认设置False，值为空自动会添加默认值
完全体：
[
    {"key": "id", "type": "int", "name": "id", null: False},
    {"key": "rtx_id", "type": ft.STRING, "name": "rtxId", null: False},
    {"key": "md5_id", "type": ft.STRING, "name": "md5Id", null: False},
]

简版本：
[
    {"key": "id"},
    {"key": "rtx_id"},
    {"key": "md5_id"},
]
"""