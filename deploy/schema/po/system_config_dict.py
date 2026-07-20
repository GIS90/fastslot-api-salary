# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    csb_enum_key
    csb_enum_value

base_info:
    __author__ = PyGo
    __time__ = 2026/7/19 22:31
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = system_config_dict.py

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
from deploy.utils.utils import alphanumeric_only
from pydantic import Field, field_validator


__all__ = [
    "CsbEnumKeyAddModel",
    "CsbEnumKeyUpdateModel",
    "CsbEnumValueAddModel",
    "CsbEnumValueUpdateModel"
]


class __CsbEnumKeyBaseModel(baseModel):
    remark: str = Field(..., min_length=1, max_length=35, description="字典分类说明", alias="remark")
    order_id: int = Field(..., description="排序编号", alias="orderId")

    model_config = {
        "json_schema_extra": {
            "example": {
                "remark": "哈哈哈哈哈",
                "order_id": 1
            }
        }
    }


class CsbEnumKeyAddModel(__CsbEnumKeyBaseModel):
    key: str = Field(..., min_length=1, max_length=35, description="字典分类KEY值（允许字母、数字、连字符(-)和点(.)的组合）", alias="key")

    model_config = {
        "json_schema_extra": {
            "example": {
                "key": "ABCD-EFG",
                "remark": "说明",
                "order_id": 1
            }
        }
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("key")
    def field_is_key(cls, value: str) -> str:
        return alphanumeric_only(value=value, field="字典分类KEY值")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class CsbEnumKeyUpdateModel(__CsbEnumKeyBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
            "json_schema_extra": {
                "example": {
                    "md5": "AAAAAAAAAA",
                    "remark": "哈哈哈哈哈",
                    "order_id": 1
                }
            }
        }


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class __CsbEnumValueBaseModel(baseModel):
    value: str = Field(..., min_length=1, max_length=35, description="字典枚举值", alias="value")
    remark: str = Field(..., max_length=255, description="字典枚举描述")
    order_id: int = Field(..., description="排序编号", alias="orderId")

    model_config = {
        "json_schema_extra": {
            "example": {
                "value": "哈哈哈哈哈",
                "remark": "哈哈哈哈哈",
                "order_id": 1
            }
        }
    }


class CsbEnumValueAddModel(__CsbEnumValueBaseModel):
    name: str = Field(..., min_length=1, max_length=35, description="字典分类KEY值（允许字母、数字、连字符(-)和点(.)的组合）", alias="key")
    key: str = Field(..., min_length=1, max_length=35, description="字典枚举KEY值（允许字母、数字、连字符(-)和点(.)的组合）", alias="key")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "ABCD-EFG-UU",
                "key": "ABCD-EFG",
                "value": "ABCD-EFG",
                "remark": "说明",
                "order_id": 1
            }
        }
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("key")
    def field_is_key(cls, value: str) -> str:
        return alphanumeric_only(value=value, field="字典枚举KEY值")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class CsbEnumValueUpdateModel(__CsbEnumValueBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
            "json_schema_extra": {
                "example": {
                    "md5": "AAAAAAAAAA",
                    "value": "哈哈哈哈哈",
                    "remark": "哈哈哈哈哈",
                    "order_id": 1
                }
            }
        }