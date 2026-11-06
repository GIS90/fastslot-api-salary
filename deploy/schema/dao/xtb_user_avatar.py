# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    dao model of table xtb_user_avatar

base_info:
    __author__ = PyGo
    __time__ = 2026/11/06 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user_avatar.py

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
    BigInteger,
    Boolean,
    DateTime,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField
from typing import Optional


__all__ = ["XtbUserAvatarModel"]


class XtbUserAvatarModel(baseModel, IDField, Md5Field, CUDField, StatusField):
    __tablename__ = 'xtb_user_avatar'
    __table_args__ = ({'comment': '系统表-用户头像表'})

    name: Mapped[Optional[str]] = mapped_column(name="name", type_=String(35), comment="文件名称")
    format: Mapped[Optional[str]] = mapped_column(name="format", type_=String(16), default="PNG", comment="格式")
    width: Mapped[Optional[int]] = mapped_column(name="width", type_=Integer, default=0, comment="宽(px)")
    height: Mapped[Optional[int]] = mapped_column(name="height", type_=Integer, default=0, comment="高(px)")
    size: Mapped[Optional[int]] = mapped_column(name="size", type_=BigInteger, default=0, comment="文件大小(字节)")
    type: Mapped[Optional[str]] = mapped_column(name="type", type_=String(35), comment="头像类别：枚举avatar-type")
    summary: Mapped[Optional[str]] = mapped_column(name="summary", type_=String(255), comment="简要")
    tag: Mapped[Optional[str]] = mapped_column(name="tag", type_=String(55), comment="标签，用英文,分割")
    url: Mapped[Optional[str]] = mapped_column(name="url", type_=String(120), comment="存储地址")
    or_url: Mapped[Optional[str]] = mapped_column(name="or_url", type_=String(120), comment="原始图片存储地址")
    count: Mapped[Optional[int]] = mapped_column(name="count", type_=Integer, default=0, comment="设置次数")

    def __str__(self):
        return f"XtbUserAvatarModel Class[DB table: {self.__tablename__}], id: {self.id}, name: {self.name}, md5: {self.md5}."

    def __repr__(self):
        return self.__str__()
