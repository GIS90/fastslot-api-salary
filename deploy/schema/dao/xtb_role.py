# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbRoleModel             xtb_role               系统表-角色表

base_info:
    __author__ = PyGo
    __time__ = 2026/4/2 23:18
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_role.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField
from typing import Optional


__all__ = ["XtbRoleModel"]


class XtbRoleModel(baseModel, IDField, Md5Field, CUDField, StatusField):
    __tablename__ = 'xtb_role'
    __table_args__ = ({'comment': '系统表-角色表'})

    engname : Mapped[Optional[str]] = mapped_column(name="engname", type_=String(35), comment="角色唯一标识，英文+数字组成")
    chnname : Mapped[Optional[str]] = mapped_column(name="chnname", type_=String(35), comment="角色中文名称")
    authority : Mapped[Optional[str]] = mapped_column(name="authority", type_=String(255), comment="角色权限ID集合，用英文,分割")
    introduction: Mapped[Optional[str]] = mapped_column(name="introduction", type_=Text, comment="描述")

    def __str__(self):
        return f"XtbRoleModel Class[DB table: {self.__tablename__}], id: {self.id}, engname: {self.engname}, chnname: {self.chnname}."

    def __repr__(self):
        return self.__str__()
