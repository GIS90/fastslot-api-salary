# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    ToolOfficePdfModel       tool_office_pdf        工具表-PDF转WORD

base_info:
    __author__ = PyGo
    __time__ = 2026/8/8 11:37
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = tool_office_pdf.py

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
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, RcUDField, StatusField


__all__ = ["ToolOfficePdfModel"]


class ToolOfficePdfModel(baseModel, IDField, Md5Field, RcUDField, StatusField):
    __tablename__ = 'tool_office_pdf'
    __table_args__ = ({'comment': '工具表-PDF转WORD'})

    name: Mapped[str] = mapped_column(name="name", type_=String(100), comment="文件名称")
    store_name: Mapped[str] = mapped_column(name="store_name", type_=String(100), comment="文件存储名称")
    transfer_name: Mapped[str] = mapped_column(name="transfer_name", type_=String(100), comment="文件转换store存储名称")
    transfer: Mapped[bool] = mapped_column(name="transfer", type_=Boolean(), default=False, comment="转换状态")
    transfer_time: Mapped[Optional[datetime]] = mapped_column(name="transfer_time", type_=DateTime(), comment="转换时间")
    local_url: Mapped[str] = mapped_column(name="local_url", type_=String(130), comment="文件本地资源路径（绝对路径）")
    store_url: Mapped[str] = mapped_column(name="store_url", type_=String(130), comment="原始文件store对象存储资源路径（相对路径）")
    transfer_url: Mapped[str] = mapped_column(name="transfer_url", type_=String(130), comment="转换文件store对象存储资源路径（相对路径）")
    mode: Mapped[bool] = mapped_column(name="mode", type_=Boolean(), default=True, comment="转换模式：True页码，False指定页码")
    start: Mapped[int] = mapped_column(name="start", type_=Integer, comment="转换开始页")
    end: Mapped[int] = mapped_column(name="end", type_=Integer, comment="转换结束页")
    pages: Mapped[str] = mapped_column(name="pages", type_=String(120), comment="指定的转换页码，用英文,分割")

    def __str__(self):
        return f"ToolOfficePdfModel Class[DB table: {self.__tablename__}], id: {self.id}, name: {self.name}."

    def __repr__(self):
        return self.__str__()

