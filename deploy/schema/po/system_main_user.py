# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user

base_info:
    __author__ = PyGo
    __time__ = 2025/12/25 22:51
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user.py

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


__all__ = ["XtbUserAddModel", "XtbUserUpdateModel"]


class __XtbUserBaseModel(baseModel):
    name: str = Field(..., min_length=1, max_length=30, description="昵称")
    sex: str = Field(..., min_length=1, max_length=2, description="性别")
    email: str = Field(..., min_length=1, max_length=80, description="邮箱")
    phone: str = Field(..., min_length=11, max_length=11, description="电话")
    introduction: Optional[str] = Field(..., max_length=255, description="个性签名")
    # department: Optional[str] = Field(..., max_length=64, description="用户部门")
    role: Optional[list] = Field(..., description="用户权限")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "abcd木头人",
                "sex": "M",
                "email": "gaoming971366@163.com",
                "phone": "13051355646",
                "introduction": "哈哈哈哈哈",
                "department": "研发部",
                "role": ["admin", "hr"]
            }
        }
    }


class XtbUserAddModel(__XtbUserBaseModel):
    rtx_id: str = Field(...,
                        min_length=1,
                        max_length=35,
                        description="用户RTX-ID（唯一标识）",
                        alias="rtxId",
                        validate_default=True)

    model_config = {
        "json_schema_extra": {
            "example": {
                "rtxId": "ADC",
                "name": "abcd木头人",
                "sex": "M",
                "email": "gaoming971366@163.com",
                "phone": "13051355646",
                "introduction": "哈哈哈哈哈",
                "department": "研发部",
                "role": ["admin", "hr"]
            }
        }
    }

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("rtx_id")
    def field_is_alnum(cls, value: str) -> str:
        return alphanumeric_only(value=value, field="用户账户")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class XtbUserUpdateModel(__XtbUserBaseModel):
    md5: str = Field(..., min_length=1, max_length=64, description="数据Md5-Id", alias="md5")

    model_config = {
        "json_schema_extra": {
            "example": {
                "md5": "AAAAAAAAAA",
                "name": "adc",
                "sex": "M",
                "email": "gaoming971366@163.com",
                "phone": "13051355646",
                "introduction": "哈哈哈哈哈",
                "department": "研发部",
                "role": ["admin", "hr"]
            }
        }
    }
