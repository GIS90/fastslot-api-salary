# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    service of system ops avatar

base_info:
    __author__ = PyGo
    __time__ = 2026/11/06 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = avatar.py

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

from deploy.curd.xtb_user_avatar import XtbUserAvatarCurd
from deploy.schema.dao.xtb_user_avatar import XtbUserAvatarModel
from deploy.schema.dto.xtb_user_avatar import xtb_user_avatar_detail_fields
from deploy.service.system.config.report import SystemConfigReportService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (
    StatusCode as status_code,
)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.utils.utils import get_now, d2s, md5 as generator_md5
from deploy.utils.enumeration import XtbReportKey
from deploy.config import table_default_null as TABLE_DEFAULT_NULL, table_default_db_id as TABLE_DEFAULT_DB_ID
from deploy.utils.exception import ReportNotColumnException
from deploy.utils.utils import xtbb_field_id_value


__all__ = ["SystemOpsAvatarService"]


class SystemOpsAvatarService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemOpsAvatarService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_avatar_curd: XtbUserAvatarCurd = XtbUserAvatarCurd()
        self.system_config_report_service: SystemConfigReportService = (
            SystemConfigReportService(db_connection=db_connection)
        )

    def __str__(self):
        return "SystemOpsAvatarService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List | None = xtb_user_avatar_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbUserAvatarModel = await self.xtb_user_avatar_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", True):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbUserAvatarModel] = await self.xtb_user_avatar_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            content=params.get("content")
        )
        _default_data = {
            "list": [],
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": 0
        }
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value, data=_default_data)

        fields: Dict = await self.system_config_report_service.report_column_by_xtbb(
            rtx_id=rtx_id,
            xtbb=XtbReportKey.SystemOpsAvatar.value,
            type_="list",
            is_md5=True,
        )
        if not fields:
            return FailureStatus(code=status_code.CODE_102_SUCCESS_NO_COLUMN.value, data=_default_data)

        data: List = await many_model_converter_dict(
            models=models,
            fields=fields.get("column"),
            default_value=TABLE_DEFAULT_NULL,
            auto_id=fields.get("id_auto"),
            auto_id_value=params.get("offset") + 1,
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_user_avatar_curd.count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=True,
            response_type="dict",
            fields=xtb_user_avatar_detail_fields
        )
        return SuccessStatus(data=data) if __flag else data

    async def add(self, rtx_id: str, model: Dict) -> Status:
        # 验证头像名称是否已存在
        db_model: XtbUserAvatarModel = await self.xtb_user_avatar_curd.get_by_name(
            db=self.db,
            name=model.get("name"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="图片名称已存在，请更换")

        # 新增头像
        new_model: XtbUserAvatarModel = await self.xtb_user_avatar_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('name')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.count = 0
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_user_avatar_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def lock(self, rtx_id: str, params: Dict) -> Status:
        """
        锁定管理（启用/停用），lock=True停用 False启用
        """
        __flag, data = await self.__valid_model_by_md5(
            md5_id=params.get("md5"), status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "lock", params.get("value"))
        setattr(data, "update_rtx", rtx_id)
        setattr(data, "update_time", get_now())
        await self.xtb_user_avatar_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5_id=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_user_avatar_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_hard(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        await self.xtb_user_avatar_curd.delete(db=self.db, model=data)
        return SuccessStatus()

    async def delete_soft(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_user_avatar_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def __verify_models(self, md5_list: List) -> List:
        return await self.xtb_user_avatar_curd.get_models_by_md5_list(db=self.db, md5_list=md5_list)

    async def batch_delete_hard(self, rtx_id: str, md5_list: List) -> Status:
        data: List = await self.__verify_models(md5_list)
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_user_avatar_curd.batch_delete(db=self.db, md5_list=md5_list)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count-query_count}")

    async def batch_delete_soft(self, rtx_id: str, md5_list: List) -> Status:
        data: List = await self.__verify_models(md5_list)
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_user_avatar_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def download(self, rtx_id: str, params: dict) -> List:
        models = await self.xtb_user_avatar_curd.download(db=self.db, params=params)
        fields: Dict = await self.system_config_report_service.report_column_by_xtbb(
            rtx_id=rtx_id,
            xtbb=XtbReportKey.SystemOpsAvatar.value,
            type_="export",
            is_md5=False,
        )
        if not fields:
            raise ReportNotColumnException(detail="[系统表-用户头像表]未配置导出表头")

        __auto_id_name: Any = xtbb_field_id_value(options=fields.get("column"))
        data: List = await many_model_converter_dict(
            models=models,
            fields=fields.get("column"),
            default_value=TABLE_DEFAULT_NULL,
            auto_id=fields.get("id_auto"),
            auto_id_name=__auto_id_name if __auto_id_name else TABLE_DEFAULT_DB_ID,
            auto_id_value=1,
        )
        return data
