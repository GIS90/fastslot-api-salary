# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table                     ZH DB table
    ------------------------------------------------------------------------
    SalaryEmailMessageModel  salary_email_message          邮件消息-信息表
    SalaryEmailRobotModel    salary_email_robot            邮件消息-邮件服务配置表

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = salary_email.py

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
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column

from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField


__all__ = ["SalaryEmailMessageModel", "SalaryEmailRobotModel"]


class SalaryEmailMessageModel(baseModel, IDField, Md5Field, CUDField, StatusField):
    __tablename__ = 'salary_email_message'
    __table_args__ = ({'comment': '邮件消息-信息表'})

    file_name: Mapped[str] = mapped_column(name="file_name", type_=String(80), comment="文件名称")
    file_local_url: Mapped[Optional[str]] = mapped_column(name="file_local_url", type_=String(150), comment="文件存储本地路径")
    file_store_url: Mapped[Optional[str]] = mapped_column(name="file_store_url", type_=String(150), comment="文件存储云对象存储位置")
    robot: Mapped[Optional[str]] = mapped_column(name="robot", type_=String(55), comment="邮件邮件服务配置MD5-ID")
    count: Mapped[Optional[int]] = mapped_column(name="count", type_=Integer, default=0, comment="消息文件发送的累积次数")
    number: Mapped[Optional[int]] = mapped_column(name="number", type_=Integer, default=0, comment="消息发送的累积条数")
    nsheet: Mapped[Optional[int]] = mapped_column(name="nsheet", type_=Integer, default=1, comment="sheet数")
    sheet_names: Mapped[Optional[str]] = mapped_column(name="sheet_names", type_=Text, comment="Sheets名称列表，JSON存储")
    sheet_columns: Mapped[Optional[str]] = mapped_column(name="sheet_columns", type_=Text, comment="Sheets列名集合，JSON存储")
    headers: Mapped[Optional[str]] = mapped_column(name="headers", type_=Text, comment="Excel的header信息，JSON存储")
    set_sheet: Mapped[Optional[str]] = mapped_column(name="set_sheet", type_=String(35), comment="当前设置的sheet选择索引，;分割")
    cur_sheet: Mapped[Optional[str]] = mapped_column(name="cur_sheet", type_=String(4), comment="当前设置的sheet索引")
    set_column: Mapped[Optional[str]] = mapped_column(name="set_column", type_=Text, comment="当前设置的sheet表头列表设置JSON")
    set_title: Mapped[Optional[str]] = mapped_column(name="set_title", type_=Text, comment="每个sheet的消息标题JSON")
    success: Mapped[Optional[str]] = mapped_column(name="success", type_=Text, comment="发送成功人员名单，JSON字符串")
    failure: Mapped[Optional[str]] = mapped_column(name="failure", type_=Text, comment="发送失败人员名单，JSON字符串")

    def __str__(self):
        return f"SalaryEmailMessageModel Class[DB table: {self.__tablename__}], id: {self.id}, md5: {self.md5}."

    def __repr__(self):
        return self.__str__()


class SalaryEmailRobotModel(baseModel, IDField, Md5Field, CUDField, StatusField):
    __tablename__ = 'salary_email_robot'
    __table_args__ = ({'comment': '邮件消息-邮件服务配置表'})

    name: Mapped[str] = mapped_column(name="name", type_=String(30), comment="邮件服务名称")
    key: Mapped[str] = mapped_column(name="key", type_=String(120), comment="SMTP服务器地址:端口")
    secret: Mapped[str] = mapped_column(name="secret", type_=String(120), comment="邮箱密码或授权码")
    agent_id: Mapped[Optional[str]] = mapped_column(name="agent_id", type_=String(120), comment="发件邮箱地址")
    select: Mapped[bool] = mapped_column(name="select", type_=Boolean, default=False, comment="是否当前默认：1是；0否（默认）")
    description: Mapped[Optional[str]] = mapped_column(name="description", type_=String(120), comment="描述")

    def __str__(self):
        return f"SalaryEmailRobotModel Class[DB table: {self.__tablename__}], id: {self.id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()
