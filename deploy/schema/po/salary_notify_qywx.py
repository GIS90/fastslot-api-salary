# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    salary>notify>qywx

base_info:
    __author__ = PyGo
    __time__ = 2026/11/19 10:00
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = salary_notify_qywx.py

python version:
    python3

------------------------------------------------
"""
from typing import Any, List, Optional
from pydantic import Field

from deploy.schema._po_base_model import baseModel


__all__ = [
    "SalaryQywxUpdateModel",
    "SalaryQywxRobotAddModel",
    "SalaryQywxRobotUpdateModel",
    "SalaryQywxRobotSelectModel",
    "SalaryQywxSendModel",
    "SalaryQywxResendModel",
]


class SalaryQywxUpdateModel(baseModel):
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
                "name": "企微消息通知模板V1.0.xlsx",
                "setSheet": ["0", "1"],
                "sheet": "0",
                "title": "2026-11绩效明细",
                "column": ["0", "1", "2"]
            }
        }
    }


class SalaryQywxRobotAddModel(baseModel):
    name: str = Field(..., min_length=1, max_length=30, description="机器人名称")
    key: str = Field(..., min_length=1, max_length=30, description="企业ID（CorpID）")
    secret: str = Field(..., min_length=1, max_length=80, description="应用凭证密钥（Secret）")
    agent_id: str = Field(..., alias="agentId", min_length=1, max_length=30, description="企业应用ID（AgentId）")
    description: Optional[str] = Field(default="", max_length=120, description="描述")
    select: bool = Field(default=False, description="是否设置为默认机器人")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "薪资通知应用",
                "key": "wwxxxxxxxxxxxxxxxx",
                "secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "agentId": "1000002",
                "description": "用于发送绩效消息",
                "select": True
            }
        }
    }


class SalaryQywxRobotUpdateModel(SalaryQywxRobotAddModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "name": "薪资通知应用",
                "key": "wwxxxxxxxxxxxxxxxx",
                "secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "agentId": "1000002",
                "description": "用于发送绩效消息",
                "select": True
            }
        }
    }


class SalaryQywxRobotSelectModel(baseModel):
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


class SalaryQywxSendModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="企微消息数据Md5-Id")
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


class SalaryQywxResendModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="企微消息数据Md5-Id")
    robot: str = Field(..., min_length=1, max_length=64, description="机器人配置Md5-Id")
    users: Any = Field(default_factory=list, description="按Sheet分组的重发人员，支持 [{sheet, users}] 或 {sheet: [users]}，为空则重发全部失败人员")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "robot": "BBBBBBBBBB",
                "users": [
                    {"sheet": "0", "users": ["user001"]},
                    {"sheet": "1", "users": ["user002"]}
                ]
            }
        }
    }
