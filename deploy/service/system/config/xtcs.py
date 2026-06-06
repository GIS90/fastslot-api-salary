# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>xtcs service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/6/6 21:46
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtcs.py

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
from deploy.curd.xtb_xtcs import XtbXtcsCurd
from deploy.schema.dao.xtb_xtcs import XtbXtcsModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_xtcs import xtb_xtcs_list_fields, xtb_xtcs_detail_fields
from deploy.config import server_user, server_password, server_avatar


_SERVER_USER_ADMIN: str = server_user
_SERVER_USER_DEFAULT_PASSWORD: str = server_password
_SERVER_USER_DEFAULT_AVATAR: str = server_avatar


class SystemConfigXtcsService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemConfigXtcsService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_xtcs_curd: XtbXtcsCurd = XtbXtcsCurd()

    def __str__(self):
        return "SystemConfigXtcsService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5_or_key(
            self,
            query_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            query_type: Literal["md5", "key"] = "md5",
            fields: List[Dict] = xtb_xtcs_detail_fields,
            lock_check: bool = False
    ) -> Tuple[bool, Any]:
        if not query_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数" if query_type == "md5" else "缺少key参数")

        model: XtbXtcsModel = await self.xtb_xtcs_curd.get_by_md5(db=self.db, md5=query_id, filter_lock=False) if query_type == "md5" \
            else await self.xtb_xtcs_curd.get_by_key(db=self.db, key=query_id, filter_lock=False)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if lock_check and getattr(model, "lock", None):
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))
