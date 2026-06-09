# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>ops>task service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/6/8 21:26
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = task.py

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
from deploy.curd.xtb_user_task import XtbUserTaskCurd
from deploy.schema.dao.xtb_user_task import XtbUserTaskModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_user_task import (
    xtb_user_task_detail_fields,
    xtb_user_task_list_fields,
    xtb_user_task_download_fields
)
from deploy.utils.utils import get_now, d2s, md5 as generator_md5
from deploy.config import server_role as SERVER_ROLE_ADMIN


class SystemOpsTaskService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemMainRoleService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_task_curd: XtbUserTaskCurd = XtbUserTaskCurd()

    def __str__(self):
        return "SystemMainRoleService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List[Dict] = xtb_user_task_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbUserTaskModel = await self.xtb_user_task_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbUserTaskModel] = await self.xtb_user_task_curd.get_pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            rtx_id=rtx_id
        )
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        id_value: int = params.get("offset") + 1
        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_user_task_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "total": await self.xtb_user_task_curd.get_count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_user_task_detail_fields
        )
        return SuccessStatus(data=data) if __flag else data
