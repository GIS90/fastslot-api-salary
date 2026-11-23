# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    salary>notify>email

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = salary_notify_email.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Any, List, Optional
from pydantic import Field

from deploy.schema._po_base_model import baseModel


__all__ = [
    "SalaryEmailUpdateModel",
    "SalaryEmailRobotAddModel",
    "SalaryEmailRobotUpdateModel",
    "SalaryEmailRobotSelectModel",
    "SalaryEmailSendModel",
    "SalaryEmailResendModel",
]


class SalaryEmailUpdateModel(baseModel):
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
                "name": "邮件通知模板V1.0.xls",
                "setSheet": ["0", "1"],
                "sheet": "0",
                "title": "2026-11绩效明细",
                "column": ["0", "1", "2"]
            }
        }
    }


class SalaryEmailRobotAddModel(baseModel):
    name: str = Field(..., min_length=1, max_length=30, description="邮件服务名称")
    key: str = Field(..., min_length=1, max_length=120, description="SMTP服务器地址:端口")
    secret: str = Field(..., min_length=1, max_length=120, description="邮箱密码或授权码")
    agent_id: str = Field(..., min_length=1, max_length=120, alias="agentId", description="发件邮箱地址")
    description: Optional[str] = Field(default="", max_length=120, description="描述")
    select: bool = Field(default=False, description="是否设置为默认邮件服务")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "薪资邮件服务",
                "key": "smtp.qq.com:465",
                "secret": "邮箱授权码",
                "agentId": "sender@qq.com",
                "description": "用于发送工资邮件",
                "select": True
            }
        }
    }


class SalaryEmailRobotUpdateModel(SalaryEmailRobotAddModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "name": "薪资邮件服务",
                "key": "smtp.qq.com:465",
                "secret": "邮箱授权码",
                "agentId": "sender@qq.com",
                "description": "用于发送工资邮件",
                "select": True
            }
        }
    }


class SalaryEmailRobotSelectModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id")
    select: bool = Field(..., description="是否为默认邮件服务")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "select": True
            }
        }
    }


class SalaryEmailSendModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="邮件消息数据Md5-Id")
    robot: str = Field(..., min_length=1, max_length=64, description="邮件服务配置Md5-Id")
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


class SalaryEmailResendModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="邮件消息数据Md5-Id")
    robot: str = Field(..., min_length=1, max_length=64, description="邮件服务配置Md5-Id")
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
