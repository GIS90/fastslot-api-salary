# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    xtb_menu

base_info:
    __author__ = PyGo
    __time__ = 2025/12/6 16:01
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = menu.py

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
from pydantic import Field, field_validator
from typing import Optional
from deploy.utils.utils import letters_only


class XtbMenuBaseModel(baseModel):
    pid: int = Field(..., description="菜单父ID")
    name: str = Field(..., min_length=1, max_length=55, description="名称")
    path: str = Field(..., min_length=1, max_length=255, description="路由地址")
    title: str = Field(..., min_length=1, max_length=35, description="菜单标题")
    level: int = Field(..., description="级别")
    type: str = Field(..., min_length=1, max_length=35, description="类型")
    component: str = Field(..., min_length=1, max_length=255, description="组件路径")
    redirect: Optional[str] = Field(..., max_length=255, description="重定向地址")
    icon: Optional[str] = Field(..., max_length=35, description="图标")
    isHide: bool = Field(..., description="隐藏")
    isKeepAlive: bool = Field(..., description="缓存")
    isAffix: bool = Field(..., description="固定标签")
    isFull: bool = Field(..., description="全屏")
    isBreadcrumb: bool = Field(..., description="面包屑菜单")
    tag: str = Field(..., max_length=10, description="TAG")
    order_id: int = Field(..., description="排序编号")


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("name")
    def field_is_name(cls, value: str) -> str:
        return letters_only(value=value, field="菜单名称")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class XtbMenuUpdateModel(XtbMenuBaseModel):
    id: int = Field(..., description="菜单ID")
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")