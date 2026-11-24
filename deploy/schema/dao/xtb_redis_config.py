# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    dao model of table xtb_redis_config

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = xtb_redis_config.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！！
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField, LockField


__all__ = ["XtbRedisConfigModel"]


class XtbRedisConfigModel(baseModel, IDField, Md5Field, CUDField, StatusField, LockField):
    __tablename__ = 'xtb_redis_config'
    __table_args__ = ({'comment': '系统表-Redis连接配置表'})

    name: Mapped[Optional[str]] = mapped_column(name="name", type_=String(55), nullable=False, comment="配置名称")
    host: Mapped[Optional[str]] = mapped_column(name="host", type_=String(120), default="127.0.0.1", comment="Redis主机地址")
    port: Mapped[Optional[int]] = mapped_column(name="port", type_=Integer, default=6379, comment="Redis端口")
    db: Mapped[Optional[int]] = mapped_column(name="db", type_=Integer, default=0, comment="Redis数据库编号")
    password: Mapped[Optional[str]] = mapped_column(name="password", type_=String(120), comment="Redis密码，可为空")
    order_id: Mapped[Optional[int]] = mapped_column(name="order_id", type_=Integer, default=1, comment="排序编码")
    summary: Mapped[Optional[str]] = mapped_column(name="summary", type_=String(255), comment="配置说明")

    def __str__(self):
        return f"XtbRedisConfigModel Class[DB table: {self.__tablename__}], id: {self.id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()
