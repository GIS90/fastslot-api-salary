# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    dao model of table xtb_redis_rule

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = xtb_redis_rule.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！！
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField, LockField


__all__ = ["XtbRedisRuleModel"]


class XtbRedisRuleModel(baseModel, IDField, Md5Field, CUDField, StatusField, LockField):
    __tablename__ = 'xtb_redis_rule'
    __table_args__ = ({'comment': '系统表-Redis缓存清理规则表'})

    name: Mapped[Optional[str]] = mapped_column(name="name", type_=String(55), nullable=False, comment="规则名称")
    redis_md5: Mapped[Optional[str]] = mapped_column(name="redis_md5", type_=String(64), nullable=False, comment="关联Redis连接配置MD5")
    match: Mapped[Optional[str]] = mapped_column(name="match", type_=String(20), default="prefix", comment="匹配方式：枚举redis-match，prefix/pattern/regex")
    pattern: Mapped[Optional[str]] = mapped_column(name="pattern", type_=String(255), nullable=False, comment="键匹配内容，由后端解析执行")
    max_keys: Mapped[Optional[int]] = mapped_column(name="max_keys", type_=Integer, default=1000, comment="单次清理最大键数量限制")
    order_id: Mapped[Optional[int]] = mapped_column(name="order_id", type_=Integer, default=1, comment="排序编码")
    summary: Mapped[Optional[str]] = mapped_column(name="summary", type_=String(255), comment="规则说明")
    last_clean_time: Mapped[Optional[datetime]] = mapped_column(name="last_clean_time", type_=DateTime(), comment="上次清理时间")
    last_clean_count: Mapped[Optional[int]] = mapped_column(name="last_clean_count", type_=Integer, default=0, comment="上次清理键数量")

    def __str__(self):
        return f"XtbRedisRuleModel Class[DB table: {self.__tablename__}], id: {self.id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()
