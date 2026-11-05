# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_api

base_info:
    __author__ = PyGo
    __time__ = 2026/7/20 00:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = system_config_api.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.schema._po_base_model import baseModel
from pydantic import Field
from typing import Optional


__all__ = ["XtbApiAddModel", "XtbApiUpdateModel"]


class __XtbApiBaseModel(baseModel):
    blueprint: str = Field(..., min_length=1, max_length=25, description="API接口blueprint", alias="blueprint")
    apiname: str = Field(..., min_length=1, max_length=35, description="API接口View方法名称", alias="apiname")
    endpoint: str = Field(..., min_length=1, max_length=65, description="API接口endpoint", alias="endpoint")
    path: str = Field(..., min_length=1, max_length=65, description="API接口path，与request表关联", alias="path")
    method: str = Field(..., min_length=1, max_length=35, description="API接口请求方式", alias="method")
    short: Optional[str] = Field(default=None, max_length=35, description="API接口简述", alias="short")
    long: Optional[str] = Field(default=None, max_length=255, description="API接口详细描述", alias="long")
    order_id: int = Field(default=0, description="排序ID", alias="orderId")

    model_config = {
        "json_schema_extra": {
            "example": {
                "blueprint": "system",
                "apiname": "role_list",
                "endpoint": "/system/main/role.list",
                "path": "/system/main/role.list",
                "method": "GET",
                "short": "角色列表",
                "long": "获取角色列表数据",
                "orderId": 0
            }
        }
    }


class XtbApiAddModel(__XtbApiBaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "blueprint": "system",
                "apiname": "role_list",
                "endpoint": "/system/main/role.list",
                "path": "/system/main/role.list",
                "method": "GET",
                "short": "角色列表",
                "long": "获取角色列表数据",
                "orderId": 0
            }
        }
    }


class XtbApiUpdateModel(__XtbApiBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "blueprint": "system",
                "apiname": "role_list",
                "endpoint": "/system/main/role.list",
                "path": "/system/main/role.list",
                "method": "GET",
                "short": "角色列表",
                "long": "获取角色列表数据",
                "orderId": 0
            }
        }
    }
