# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/5/18 23:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = setter_profile.py

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


__all__ = ["ProfileUserBaseModel", "ProfileUserPasswordModel"]


class ProfileUserBaseModel(baseModel):
    userId: str = Field(..., min_length=1, max_length=35, description="用户RTX-ID（唯一标识）", validate_default=True)
    userName: str = Field(..., min_length=1, max_length=30, description="昵称")
    sex: str = Field(..., min_length=1, max_length=2, description="性别")
    email: str = Field(..., min_length=1, max_length=80, description="邮箱")
    phone: str = Field(..., min_length=11, max_length=11, description="电话")
    introduction: Optional[str] = Field(..., max_length=255, description="个性签名")

    model_config = {
        "json_schema_extra": {
            "example": {
                "userId": "adc",
                "userName": "abcd木头人",
                "sex": "M",
                "email": "gaoming971366@163.com",
                "phone": "13051355646",
                "introduction": "哈哈哈哈哈"
            }
        }
    }


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    """
    字段特殊验证：字母+数字
    """
    @field_validator("userId")
    def field_is_alnum(cls, value: str) -> str:
        return alphanumeric_only(value=value, field="rtx_id")
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ProfileUserPasswordModel(baseModel):
    """
    url: [put]/set/password
    """
    userPassword: str = Field(..., min_length=1, max_length=120, description="旧密码")
    newPassword: str = Field(..., min_length=8, max_length=120, description="新密码")
    confirmNewPassword: str = Field(..., min_length=8, max_length=120, description="新密码")

    class Config:
        json_schema_extra = {
            "example": {
                "userPassword": "abcd1234",
                "newPassword": "abcd1234",
                "confirmNewPassword": "abcd1234"
            }
        }
