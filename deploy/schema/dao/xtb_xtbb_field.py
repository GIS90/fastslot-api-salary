# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbXtbbFieldModel        xtb_xtbb_field         系统表-系统报表字段

base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtbb_field.py

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
    Boolean,
    DateTime,
    Text,
    Numeric
)
from sqlalchemy.orm import Mapped, mapped_column
from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField, OrderIdFiled


__all__ = ["XtbXtbbFieldModel"]


class XtbXtbbFieldModel(baseModel, IDField, Md5Field, CUDField, StatusField, OrderIdFiled):
    __tablename__ = 'xtb_xtbb_field'
    __table_args__ = ({'comment': '系统表-系统报表字段'})

    field: Mapped[str] = mapped_column(name="field", type_=String(35), comment="数据库字段名称")
    name_zh: Mapped[str] = mapped_column(name="name_zh", type_=String(35), comment="字段英文名称")
    name_ch: Mapped[str] = mapped_column(name="name_ch", type_=String(35), comment="字段中文名称")
    xtbb_md5: Mapped[str] = mapped_column(name="xtbb_md5", type_=String(64), comment="系统报表MD5-ID，关联xtb_xtbb表")
    remark: Mapped[str | None] = mapped_column(name="remark", type_=String(100), comment="字段说明")
    width: Mapped[float] = mapped_column(name="width", type_=Numeric(10, 4), default=0, comment="宽度")
    fixed: Mapped[str] = mapped_column(name="fixed", type_=String(35), default="", comment="锁定：left right")
    list: Mapped[bool] = mapped_column(name="list", type_=Boolean(), default=True, comment="列表：1支持；0不支持")
    list_type: Mapped[str] = mapped_column(name="list_type", type_=String(35), default="", comment="List字段类型")
    export: Mapped[bool] = mapped_column(name="export", type_=Boolean(), default=True, comment="导出：1支持；0不支持")
    export_type: Mapped[str] = mapped_column(name="export_type", type_=String(35), default="", comment="Export字段类型")
    null: Mapped[bool] = mapped_column(name="null", type_=Boolean(), default=True, comment="空值：1允许；0不允许")
    id_auto: Mapped[bool] = mapped_column(name="id_auto", type_=Boolean(), default=True, comment="ID自增：1自增；0非自增")
    extend: Mapped[bool] = mapped_column(name="extend", type_=Boolean(), default=False, comment="扩展字段：1扩展字段；0非扩展字段")
    filter: Mapped[str | None] = mapped_column(name="filter", type_=Text, comment="字段筛选字段内容")

    def __str__(self):
        return f"XtbXtbbFieldModel Class[DB table: {self.__tablename__}], field: {self.field}, name_ch: {self.name_ch}."

    def __repr__(self):
        return self.__str__()
