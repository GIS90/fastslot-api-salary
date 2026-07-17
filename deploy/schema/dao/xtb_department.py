# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbDepartmentModel       xtb_department         系统表-部门表

base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_department.py

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
from typing import Optional


__all__ = ["XtbDepartmentModel"]


class XtbDepartmentModel(baseModel, IDField, Md5Field, CUDField, StatusField, OrderIdFiled):
    __tablename__ = 'xtb_department'
    __table_args__ = ({'comment': '系统表-部门表'})

    name : Mapped[Optional[str]] = mapped_column(name="name", type_=String(30), comment="部门名称")
    description: Mapped[Optional[str]] = mapped_column(name="description", type_=Text, comment="部门描述")
    pid: Mapped[int] = mapped_column(name="pid", type_=Integer, comment="父ID")
    leaf: Mapped[bool] = mapped_column(name="leaf", type_=Boolean(), default=False, comment="是否为叶子节点，如果为True不允许有子节点，默认为False")
    lock: Mapped[bool] = mapped_column(name="lock", type_=Boolean(), default=False, comment="是否锁定，如果为True为锁定，默认为False")
    level: Mapped[int] = mapped_column(name="level", type_=Integer, default=1, comment="部门层级，默认为1级")
    dept_path: Mapped[Optional[str]] = mapped_column(name="dept_path", type_=String(254), comment="部门名称全路径，用>进行分割")
    manage_rtx: Mapped[Optional[str]] = mapped_column(name="manage_rtx", type_=String(254), comment="部门主管rtx-id，多用户，用英文,分割")

    def __str__(self):
        return f"XtbDepartmentModel Class[DB table: {self.__tablename__}], id: {self.id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()
