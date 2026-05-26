# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbXtcsModel             xtb_xtcs               系统表-系统参数

base_info:
    __author__ = PyGo
    __time__ = 2026/5/26 22:25
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtcs.py

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
from .common_field import IDField, Md5Field, CUDField, StatusField, OrderIdFiled


__all__ = ["XtbXtcsModel"]


class XtbXtcsModel(baseModel, IDField, Md5Field, CUDField, StatusField, OrderIdFiled):
    __tablename__ = 'xtb_xtcs'
    __table_args__ = ({'comment': '系统表-系统参数'})

    key: Mapped[str] = mapped_column(name="key", type_=String(35), nullable=False, comment="参数KEY")
    remark: Mapped[str] = mapped_column(name="remark", type_=String(35), nullable=False, comment="参数说明")
    value: Mapped[str] = mapped_column(name="value", type_=String(255), nullable=False, comment="参数值")

    def __str__(self):
        return f"XtbXtcsModel Class[DB table: {self.__tablename__}], key: {self.key}, value: {self.value}, remark: {self.remark}."

    def __repr__(self):
        return self.__str__()
