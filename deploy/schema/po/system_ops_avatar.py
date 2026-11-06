# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    po model of system ops avatar

base_info:
    __author__ = PyGo
    __time__ = 2026/11/06 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = system_ops_avatar.py

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


__all__ = ["XtbAvatarAddModel", "XtbAvatarUpdateModel"]


class __XtbAvatarBaseModel(baseModel):
    name: str = Field(..., min_length=1, max_length=35, description="文件名称", alias="name")
    type: Optional[str] = Field(default=None, max_length=35, description="头像类别：枚举avatar-type", alias="type")
    summary: Optional[str] = Field(default=None, max_length=255, description="简要说明", alias="summary")
    tag: Optional[str] = Field(default=None, max_length=55, description="标签，用英文,分割", alias="tag")
    url: str = Field(..., min_length=1, max_length=120, description="存储地址", alias="url")
    or_url: str = Field(..., min_length=1, max_length=120, description="原始图片存储地址", alias="orUrl")
    format: Optional[str] = Field(default="PNG", max_length=16, description="格式", alias="format")
    width: int = Field(default=0, ge=0, description="宽(px)", alias="width")
    height: int = Field(default=0, ge=0, description="高(px)", alias="height")
    size: int = Field(default=0, ge=0, description="文件大小(字节)", alias="size")
    status: bool = Field(default=False, description="数据状态：False启用；True停用", alias="status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "用户默认头像-01",
                "type": "PORTRAIT",
                "summary": "系统默认男性头像",
                "tag": "默认,男性",
                "url": "https://cdn.example.com/avatar/01.png",
                "orUrl": "https://cdn.example.com/avatar/01.png",
                "format": "PNG",
                "width": 512,
                "height": 512,
                "size": 102400,
                "status": False
            }
        }
    }


class XtbAvatarAddModel(__XtbAvatarBaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "用户默认头像-01",
                "type": "PORTRAIT",
                "summary": "系统默认男性头像",
                "tag": "默认,男性",
                "url": "https://cdn.example.com/avatar/01.png",
                "orUrl": "https://cdn.example.com/avatar/01.png",
                "format": "PNG",
                "width": 512,
                "height": 512,
                "size": 102400,
                "status": False
            }
        }
    }


class XtbAvatarUpdateModel(__XtbAvatarBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "name": "用户默认头像-01",
                "type": "PORTRAIT",
                "summary": "系统默认男性头像",
                "tag": "默认,男性",
                "url": "https://cdn.example.com/avatar/01.png",
                "orUrl": "https://cdn.example.com/avatar/01.png",
                "format": "PNG",
                "width": 512,
                "height": 512,
                "size": 102400,
                "status": False
            }
        }
    }
