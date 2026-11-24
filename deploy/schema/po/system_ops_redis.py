# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    po model of system ops redis

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = system_ops_redis.py

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

from pydantic import Field

from deploy.schema._po_base_model import baseModel


__all__ = [
    "XtbRedisConfigAddModel", "XtbRedisConfigUpdateModel",
    "XtbRedisRuleAddModel", "XtbRedisRuleUpdateModel",
]


class __XtbRedisConfigBaseModel(baseModel):
    name: str = Field(..., min_length=1, max_length=55, description="配置名称", alias="name")
    host: str = Field(..., min_length=1, max_length=120, description="Redis主机地址", alias="host")
    port: int = Field(default=6379, ge=1, le=65535, description="Redis端口", alias="port")
    db: int = Field(default=0, ge=0, le=15, description="Redis数据库编号", alias="db")
    password: Optional[str] = Field(default=None, max_length=120, description="Redis密码", alias="password")
    order_id: int = Field(default=1, ge=0, description="排序编码", alias="orderId")
    summary: Optional[str] = Field(default=None, max_length=255, description="配置说明", alias="summary")
    lock: bool = Field(default=False, description="True停用；False启用", alias="lock")


class XtbRedisConfigAddModel(__XtbRedisConfigBaseModel):
    pass


class XtbRedisConfigUpdateModel(__XtbRedisConfigBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")


class __XtbRedisRuleBaseModel(baseModel):
    name: str = Field(..., min_length=1, max_length=55, description="规则名称", alias="name")
    redis_md5: str = Field(..., min_length=1, max_length=64, description="Redis配置Md5-Id", alias="redisMd5")
    match: str = Field(default="prefix", max_length=20, description="匹配方式：枚举redis-match", alias="match")
    pattern: str = Field(..., min_length=1, max_length=255, description="键匹配内容", alias="pattern")
    max_keys: int = Field(default=1000, ge=1, le=100000, description="单次清理最大键数量", alias="maxKeys")
    order_id: int = Field(default=1, ge=0, description="排序编码", alias="orderId")
    summary: Optional[str] = Field(default=None, max_length=255, description="规则说明", alias="summary")
    lock: bool = Field(default=False, description="True停用；False启用", alias="lock")


class XtbRedisRuleAddModel(__XtbRedisRuleBaseModel):
    pass


class XtbRedisRuleUpdateModel(__XtbRedisRuleBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")
