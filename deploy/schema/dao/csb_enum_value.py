# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    CsbEnumValueModel        csb_enum_value         参数表-枚举Value表
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/28 22:48
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = csb_enum_value.py

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


__all__ = ["CsbEnumValueModel"]


class CsbEnumValueModel(baseModel, IDField, Md5Field, CUDField, LockField, StatusField, OrderIdFiled):
    __tablename__ = 'csb_enum_value'
    __table_args__ = ({'comment': '参数表-枚举Value表'})

    name: Mapped[str] = mapped_column(name="name", type_=String(35), comment="字典枚举子集对应的key（csb_enum_key）")
    key: Mapped[str] = mapped_column(name="key", type_=String(35), comment="字典枚举VALUE值RTX-ID")
    value: Mapped[str] = mapped_column(name="value", type_=String(35), comment="字典枚举子集对应的value")
    remark: Mapped[str] = mapped_column(name="remark", type_=Text, comment="字典枚举子集对应的value说明")

    def __str__(self):
        return f"CsbEnumValueModel Class[DB table: {self.__tablename__}], key: {self.key}, name: {self.name}, value: {self.value}."

    def __repr__(self):
        return self.__str__()
