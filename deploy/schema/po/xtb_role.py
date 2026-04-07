# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_role

base_info:
    __author__ = PyGo
    __time__ = 2026/4/7 21:16
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_role.py

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
from typing import Optional


__all__ = ["XtbRoleAddModel", "XtbRoleUpdateModel"]


class __XtbRoleBaseModel(baseModel):
    chnname: str = Field(..., min_length=1, max_length=30, description="角色中文名称", alias="chnname")
    introduction: Optional[str] = Field(..., max_length=255, description="角色描述")

    model_config = {
        "json_schema_extra": {
            "example": {
                "chnname": "abcd木头人",
                "introduction": "哈哈哈哈哈"
            }
        }
    }


class XtbRoleAddModel(__XtbRoleBaseModel):
    engname: str = Field(...,
                         min_length=1,
                         max_length=35,
                         description="角色唯一标识，英文+数字组成",
                         alias="engname",
                         validate_default=True)

    model_config = {
        "json_schema_extra": {
            "example": {
                "engname": "ADC",
                "chnname": "abcd木头人",
                "introduction": "哈哈哈哈哈"
            }
        }
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("engname")
    def field_is_alnum(cls, value: str) -> str:
        return alphanumeric_only(value=value, field="engname")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class XtbRoleUpdateModel(__XtbRoleBaseModel):
    md5_id: str = Field(..., min_length=1, max_length=64, description="数据MD5", alias="md5_id")

    model_config = {
            "json_schema_extra": {
                "example": {
                    "md5_id": "AAAAAAAAAA",
                    "chnname": "abcd木头人",
                    "introduction": "哈哈哈哈哈"
                }
            }
        }
