# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    common field of base model

base_info:
    __author__ = PyGo
    __time__ = 2025/12/28 14:57
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = common_field.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text
)


class IDField:
    id: Mapped[int] = mapped_column(name="id", type_=Integer, autoincrement="auto", primary_key=True, comment="主键，自增ID")


class RtxIdField:
    rtx_id: Mapped[str] = mapped_column(name="rtx_id", type_=String(35), nullable=False, comment="RTX-ID唯一标识，有英文+数字组成")


class Md5Field:
    md5: Mapped[str] = mapped_column(name="md5", type_=String(64), unique=True, nullable=False, comment="数据唯一标识：MD5-ID")


class CUDField:
    create_rtx: Mapped[Optional[str]] = mapped_column(name="create_rtx", type_=String(35), comment="创建用户RTX-ID")
    create_time: Mapped[datetime] = mapped_column(name="create_time", type_=DateTime(), comment="创建时间")
    update_rtx: Mapped[Optional[str]] = mapped_column(name="update_rtx", type_=String(35), comment="更新用户RTX-ID")
    update_time: Mapped[Optional[datetime]] = mapped_column(name="update_time", type_=DateTime(), comment="更新时间")
    delete_rtx: Mapped[Optional[str]] = mapped_column(name="delete_rtx", type_=String(35), comment="删除用户RTX-ID")
    delete_time: Mapped[Optional[datetime]] = mapped_column(name="delete_time", type_=DateTime(), comment="删除时间")


class RcUDField:
    rtx_id: Mapped[str] = mapped_column(name="rtx_id", type_=String(35), nullable=False, comment="RTX-ID唯一标识，有英文+数字组成")
    create_time: Mapped[datetime] = mapped_column(name="create_time", type_=DateTime(), comment="创建时间")
    update_rtx: Mapped[Optional[str]] = mapped_column(name="update_rtx", type_=String(35), comment="更新用户RTX-ID")
    update_time: Mapped[Optional[datetime]] = mapped_column(name="update_time", type_=DateTime(), comment="更新时间")
    delete_rtx: Mapped[Optional[str]] = mapped_column(name="delete_rtx", type_=String(35), comment="删除用户RTX-ID")
    delete_time: Mapped[Optional[datetime]] = mapped_column(name="delete_time", type_=DateTime(), comment="删除时间")


class LockField:
    lock: Mapped[bool] = mapped_column(name="lock", type_=Boolean(), default=False, comment="锁定状态：1锁定；0非锁定")

class StatusField:
    status: Mapped[bool] = mapped_column(name="status", type_=Boolean(), default=False, comment="数据状态：1注销/删除；0启用/正常（默认）")


class OrderIdFiled:
    order_id: Mapped[int] = mapped_column(name="order_id", type_=Integer, comment="数据排序ID")