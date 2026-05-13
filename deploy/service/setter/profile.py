# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/5/11 22:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = profile.py

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
from deploy.curd.xtb_user import XtbUserCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_user import xtb_user_list_fields, xtb_user_detail_fields, xtb_user_login_fields
from deploy.utils.utils import get_now, random_string, md5 as generator_md5
from deploy.config import server_user as SERVER_USER_ADMIN


class SetterProfileService:

    def __init__(self, db_connection: AsyncSession):
        """
        SetterProfileService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_curd: XtbUserCurd = XtbUserCurd()

    def __str__(self):
        return "SetterProfileService class."

    def __repr__(self):
        return self.__str__()

    async def profile_detail(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=False, response_type="dict", query_type="md5", admin_check=False
        )
        return SuccessStatus(data=data) if __flag else data

    async def profile_update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=_md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        if model.get("rtx_id"):
            del model["rtx_id"]
        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()
