# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/6/6 22:27
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = system_config_xtcs.py

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
from deploy.utils.utils import capital_letter_only
from pydantic import Field, field_validator


__all__ = ["XtbXtcsAddModel", "XtbXtcsUpdateModel"]


class __XtbXtcsBaseModel(baseModel):
    remark: str = Field(..., min_length=1, max_length=35, description="参数说明", alias="remark")
    value: str = Field(..., min_length=1, max_length=255, description="参数值", alias="value")
    order_id: int = Field(..., description="排序编号", alias="orderId")

    model_config = {
        "json_schema_extra": {
            "example": {
                "remark": "系统参数说明",
                "value": "参数值",
                "order_id": 1
            }
        }
    }


class XtbXtcsAddModel(__XtbXtcsBaseModel):
    key: str = Field(..., min_length=1, max_length=35, description="参数名称（大写字母、数字和中划线（-））", alias="key")

    model_config = {
        "json_schema_extra": {
            "example": {
                "key": "ABCD-EFG",
                "remark": "系统参数说明",
                "value": "参数值",
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
        return capital_letter_only(value=value, field="参数名称")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class XtbXtcsUpdateModel(__XtbXtcsBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
            "json_schema_extra": {
                "example": {
                    "md5": "AAAAAAAAAA",
                    "remark": "系统参数说明",
                    "value": "参数值",
                    "order_id": 1
                }
            }
        }
