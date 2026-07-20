# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    CsbEnumKeyModel          csb_enum_key           参数表-枚举Key表

base_info:
    __author__ = PyGo
    __time__ = 2026/5/28 22:48
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = csb_enum_key.py

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
from .common_field import IDField, Md5Field, CUDField, LockField, StatusField, OrderIdFiled


__all__ = ["CsbEnumKeyModel"]


class CsbEnumKeyModel(baseModel, IDField, Md5Field, CUDField, LockField, StatusField, OrderIdFiled):
    __tablename__ = 'csb_enum_key'
    __table_args__ = ({'comment': '参数表-枚举Key表'})

    key: Mapped[str] = mapped_column(name="key", type_=String(35), comment="字典分类KEY值RTX-ID")
    remark: Mapped[str] = mapped_column(name="remark", type_=String(35), comment="字典分类说明")

    def __str__(self):
        return f"CsbEnumKeyModel Class[DB table: {self.__tablename__}], key: {self.key}, remark: {self.remark}."

    def __repr__(self):
        return self.__str__()
