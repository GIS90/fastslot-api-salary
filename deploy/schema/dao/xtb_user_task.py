# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbUserTaskModel         xtb_user_task          系统表-用户任务表

base_info:
    __author__ = PyGo
    __time__ = 2026/6/7 16:20
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user_task.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text,
    DECIMAL
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, StatusField, RtxIdField
from typing import Optional


__all__ = ["XtbUserTaskModel"]


class XtbUserTaskModel(baseModel, IDField, RtxIdField, Md5Field, StatusField):
    __tablename__ = 'xtb_user_task'
    __table_args__ = ({'comment': '系统表-用户任务表'})

    api : Mapped[Optional[str]] = mapped_column(name="api", type_=String(55), comment="API接口名称")
    name : Mapped[Optional[str]] = mapped_column(name="name", type_=String(55), comment="文件名称")
    data : Mapped[Optional[str]] = mapped_column(name="data", type_=String(35), comment="数据下载类型")
    task : Mapped[Optional[str]] = mapped_column(name="task", type_=String(35), comment="任务状态：success failure working")
    cost: Mapped[float] = mapped_column(name="cost", type_=DECIMAL(10, 4), comment="运行时间")
    create_time: Mapped[datetime] = mapped_column(name="create_time", type_=DateTime(), comment="创建时间")
    update_time: Mapped[Optional[datetime]] = mapped_column(name="update_time", type_=DateTime(), comment="更新时间")
    delete_rtx: Mapped[Optional[str]] = mapped_column(name="delete_rtx", type_=String(35), comment="删除用户RTX-ID")
    delete_time: Mapped[Optional[datetime]] = mapped_column(name="delete_time", type_=DateTime(), comment="删除时间")

    def __str__(self):
        return f"XtbUserTaskModel Class[DB table: {self.__tablename__}], id: {self.id}, api: {self.api}, name: {self.name}."

    def __repr__(self):
        return self.__str__()

