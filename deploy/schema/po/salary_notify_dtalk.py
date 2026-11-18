# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    salary>notify>dtalk

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = salary_notify_dtalk.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import List, Optional
from pydantic import Field

from deploy.schema._po_base_model import baseModel


__all__ = [
    "SalaryDtalkUpdateModel",
    "SalaryDtalkRobotAddModel",
    "SalaryDtalkRobotUpdateModel",
    "SalaryDtalkRobotSelectModel",
    "SalaryDtalkSendModel",
]


class SalaryDtalkUpdateModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id")
    name: str = Field(..., min_length=1, max_length=80, description="文件名称")
    set_sheet: List[str] = Field(..., alias="setSheet", description="消息Sheet索引列表")
    sheet: str = Field(..., min_length=1, max_length=4, description="当前设置的Sheet索引")
    title: str = Field(default="", max_length=50, description="当前Sheet的消息标题")
    column: List[str] = Field(default=[], description="当前Sheet的消息列头索引列表")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "name": "钉钉消息通知模板V1.0.xls",
                "setSheet": ["0", "1"],
                "sheet": "0",
                "title": "2026-11绩效明细",
                "column": ["0", "1", "2"]
            }
        }
    }


class SalaryDtalkRobotAddModel(baseModel):
    name: str = Field(..., min_length=1, max_length=30, description="机器人名称")
    key: str = Field(..., min_length=1, max_length=30, description="机器人APP-KEY")
    secret: str = Field(..., min_length=1, max_length=70, description="机器人APP-SECRET")
    description: Optional[str] = Field(default="", max_length=120, description="描述")
    select: bool = Field(default=False, description="是否设置为默认机器人")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "薪资机器人",
                "key": "dingxxxxxxxx",
                "secret": "SECxxxxxxxx",
                "description": "用于发送绩效消息",
                "select": True
            }
        }
    }


class SalaryDtalkRobotUpdateModel(SalaryDtalkRobotAddModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "name": "薪资机器人",
                "key": "dingxxxxxxxx",
                "secret": "SECxxxxxxxx",
                "description": "用于发送绩效消息",
                "select": True
            }
        }
    }


class SalaryDtalkRobotSelectModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id")
    select: bool = Field(..., description="是否为默认机器人")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "select": True
            }
        }
    }


class SalaryDtalkSendModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="钉钉消息数据Md5-Id")
    robot: str = Field(..., min_length=1, max_length=64, description="机器人配置Md5-Id")
    sheet: List[str] = Field(..., description="发送的Sheet索引列表")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "robot": "BBBBBBBBBB",
                "sheet": ["0"]
            }
        }
    }
