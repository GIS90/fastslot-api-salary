# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbApiModel             xtb_api               API接口说明表

base_info:
    __author__ = PyGo
    __time__ = 2026/7/20 00:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_api.py

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
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField, OrderIdFiled
from typing import Optional


__all__ = ["XtbApiModel"]


class XtbApiModel(baseModel, IDField, Md5Field, CUDField, StatusField, OrderIdFiled):
    __tablename__ = 'xtb_api'
    __table_args__ = ({'comment': 'API接口说明表'})

    blueprint: Mapped[str] = mapped_column(name="blueprint", type_=String(25), nullable=False, comment="API接口blueprint")
    apiname: Mapped[str] = mapped_column(name="apiname", type_=String(35), nullable=False, comment="API接口View方法名称")
    endpoint: Mapped[str] = mapped_column(name="endpoint", type_=String(65), nullable=False, comment="API接口endpoint")
    path: Mapped[str] = mapped_column(name="path", type_=String(65), nullable=False, comment="API接口path，与request表关联")
    method: Mapped[str] = mapped_column(name="method", type_=String(35), nullable=False, default="GET", comment="API接口请求方式：GET/POST/PUT/PATCH/DELETE")
    short: Mapped[Optional[str]] = mapped_column(name="short", type_=String(35), comment="API接口简述")
    long: Mapped[Optional[str]] = mapped_column(name="long", type_=String(255), comment="API接口详细描述")

    def __str__(self):
        return f"XtbApiModel Class[DB table: {self.__tablename__}], id: {self.id}, blueprint: {self.blueprint}, apiname: {self.apiname}, endpoint: {self.endpoint}, path: {self.path}, method: {self.method}."

    def __repr__(self):
        return self.__str__()
