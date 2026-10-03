# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_xtbb / xtb_xtbb_field

base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = system_config_report.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.schema._po_base_model import baseModel
from pydantic import Field


__all__ = [
    "XtbXtbbAddModel", "XtbXtbbUpdateModel",
    "XtbXtbbFieldAddModel", "XtbXtbbFieldUpdateModel"
]


class __XtbXtbbBaseModel(baseModel):
    name: str = Field(..., min_length=1, max_length=35, description="报表名称", alias="name")
    table: str = Field(..., min_length=1, max_length=35, description="数据库表名", alias="table")
    remark: str | None = Field(default=None, max_length=100, description="报表说明", alias="remark")
    mode: bool = Field(default=False, description="宽度模式：1百分比；0固定数值", alias="mode")


class XtbXtbbAddModel(__XtbXtbbBaseModel):
    ...


class XtbXtbbUpdateModel(__XtbXtbbBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")


class __XtbXtbbFieldBaseModel(baseModel):
    field: str = Field(..., min_length=1, max_length=35, description="数据库字段名称", alias="field")
    name_zh: str = Field(..., min_length=1, max_length=35, description="字段英文名称", alias="nameZh")
    name_ch: str = Field(..., min_length=1, max_length=35, description="字段中文名称", alias="nameCh")
    xtbb_md5: str = Field(..., min_length=1, max_length=64, description="系统报表MD5-ID", alias="xtbbMd5")
    remark: str | None = Field(default=None, max_length=100, description="字段说明", alias="remark")
    width: float = Field(default=0, description="宽度", alias="width")
    fixed: str = Field(default="", max_length=35, description="锁定：left right", alias="fixed")
    list: bool = Field(default=True, description="列表：1支持；0不支持", alias="list")
    list_type: str = Field(default="", max_length=35, description="List字段类型", alias="listType")
    export: bool = Field(default=True, description="导出：1支持；0不支持", alias="export")
    export_type: str = Field(default="", max_length=35, description="Export字段类型", alias="exportType")
    null: bool = Field(default=True, description="空值：1允许；0不允许", alias="null")
    id_auto: bool = Field(default=True, description="ID自增：1自增；0非自增", alias="idAuto")
    extend: bool = Field(default=False, description="扩展字段：1扩展字段；0非扩展字段", alias="extend")
    filter: str | None = Field(default=None, description="字段筛选字段内容", alias="filter")
    order_id: int | None = Field(default=None, description="排序ID", alias="orderId")


class XtbXtbbFieldAddModel(__XtbXtbbFieldBaseModel):
    ...


class XtbXtbbFieldUpdateModel(__XtbXtbbFieldBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")
