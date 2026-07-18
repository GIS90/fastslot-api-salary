# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_department

base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:50
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = system_ops_depart.py

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
from typing import Optional, List


__all__ = ["XtbDepartmentAddModel", "XtbDepartmentUpdateModel", "XtbDepartmentDragModel"]


class __XtbDepartmentBaseModel(baseModel):
    name: str = Field(..., min_length=1, max_length=30, description="部门名称", alias="label")
    description: Optional[str] = Field(..., max_length=255, description="description")
    pid: Optional[int] = Field(..., description="上级部门ID")
    manage_rtx: List[str] = Field(..., description="部门主管rtx-id，多用户，用英文,分割", alias="manageRtx")
    order_id: Optional[int] = Field(..., description="序号", alias="orderId")
    lock: bool = Field(..., description="锁定状态", alias="disabled")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "基础研发部",
                "introduction": "哈哈哈哈哈",
                "pid": 1,
                "manage_rtx": ["a1", "b2"],
                "order_id": 1,
                "lock": False
            }
        }
    }


class XtbDepartmentAddModel(__XtbDepartmentBaseModel):
    ...


class XtbDepartmentUpdateModel(__XtbDepartmentBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "基础研发部",
                "md5": "md5",
                "introduction": "哈哈哈哈哈",
                "pid": 1,
                "manage_rtx": ["a1", "b2"],
                "order_d": 1,
                "lock": False
            }
        }
    }


class XtbDepartmentDragModel(baseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")
    pid: int = Field(..., description="父节点ID")

    class Config:
        json_schema_extra = {
            "example": {
                "md5": 1,
                "pid": 1
            }
        }