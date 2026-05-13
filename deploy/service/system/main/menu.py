# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_menu service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:06
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_menu.py

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
from deploy.curd.xtb_role import XtbRoleCurd
from deploy.schema.dao.xtb_menu import XtbMenuModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_role import xtb_role_list_fields, xtb_role_detail_fields, xtb_role_authority_fields
from deploy.utils.utils import get_now, d2s, md5 as generator_md5
from deploy.config import server_role as SERVER_ROLE_ADMIN


class XtbMenuService:

    def __init__(self, db_connection: AsyncSession):
        """
        XtbMenuService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_role_curd: XtbRoleCurd = XtbRoleCurd()

    def __str__(self):
        return "XtbMenuService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List[Dict] = xtb_role_detail_fields,
            root_check: bool = False
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbMenuModel = await self.xtb_role_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if root_check and getattr(model, "name") == SERVER_ROLE_ADMIN:
            return False, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbMenuModel] = await self.xtb_role_curd.get_pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit")
        )
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        id_value: int = params.get("offset") * params.get("limit") + 1
        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_role_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "total": await self.xtb_role_curd.get_count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_role_detail_fields,
            admin_check=False
        )
        return SuccessStatus(data=data) if __flag else data

    async def add(self, rtx_id: str, model: Dict) -> Status:
        # 验证角色名称是否已存在
        db_model: XtbMenuModel = await self.xtb_role_curd.get_by_engname(
            db=self.db,
            engname=model.get("engname"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="角色ID已存在，请更换")

        # 新增角色
        new_model: XtbMenuModel = await self.xtb_role_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('engname')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_role_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5_id=_md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_role_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_hard(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        await self.xtb_role_curd.delete(db=self.db, model=data)
        return SuccessStatus()


    async def delete_soft(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_role_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def __verify_contain_admin_role(self, md5_list: List) -> Tuple[bool, Any]:
        db_model: List = await self.xtb_role_curd.get_engname_by_md5_list(db=self.db, md5_list=md5_list)
        if db_model and SERVER_ROLE_ADMIN in db_model:
            return True, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="管理员角色不允许删除")
        else:
            return False, db_model

    async def batch_delete_hard(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_role(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_role_curd.batch_delete(db=self.db, md5_list=md5_list)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count-query_count}")


    async def batch_delete_soft(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_role(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_role_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")
