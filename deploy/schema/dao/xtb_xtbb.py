# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbXtbbModel             xtb_xtbb               系统表-系统报表

base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtbb.py

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


__all__ = ["XtbXtbbModel"]


class XtbXtbbModel(baseModel, IDField, Md5Field, CUDField, StatusField):
    __tablename__ = 'xtb_xtbb'
    __table_args__ = ({'comment': '系统表-系统报表'})

    name: Mapped[str] = mapped_column(name="name", type_=String(35), comment="报表名称")
    table: Mapped[str] = mapped_column(name="table", type_=String(35), comment="数据库表名")
    remark: Mapped[str] = mapped_column(name="remark", type_=String(100), comment="报表说明")
    mode: Mapped[bool] = mapped_column(name="mode", type_=Boolean(), default=False, comment="宽度模式：1百分比；0固定数值")

    def __str__(self):
        return f"XtbXtbbModel Class[DB table: {self.__tablename__}], name: {self.name}, table: {self.table}, remark: {self.remark}."

    def __repr__(self):
        return self.__str__()
