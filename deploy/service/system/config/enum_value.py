# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/6/6 22:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = enum_value.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.schema.dao.csb_enum_value import CsbEnumValueModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, option_converter_dict
from deploy.schema.dto.xtb_xtcs import xtb_xtcs_list_fields, xtb_xtcs_detail_fields
from deploy.config import server_user, server_password, server_avatar


_SERVER_USER_ADMIN: str = server_user
_SERVER_USER_DEFAULT_PASSWORD: str = server_password
_SERVER_USER_DEFAULT_AVATAR: str = server_avatar


class SystemConfigEnumVService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemConfigEnumVService class initialize
        """
        self.db: AsyncSession = db_connection
        self.csb_enum_v_curd: CsbEnumValueCurd = CsbEnumValueCurd()

    def __str__(self):
        return "SystemConfigEnumVService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List[Dict] = xtb_xtcs_detail_fields,
            lock_check: bool = False
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: CsbEnumValueModel = await self.csb_enum_v_curd.get_by_md5(db=self.db, md5=md5_id, filter_lock=False)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if lock_check and getattr(model, "lock", None):
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def get_select_option_data(self, name: str, lock_view: bool = False) -> List:
        if not name: return []

        enum_v_model = await self.csb_enum_v_curd.get_list_by_name(db=self.db, name=name)
        return [] if not enum_v_model else await option_converter_dict(enum_v_model, lock_view=lock_view)