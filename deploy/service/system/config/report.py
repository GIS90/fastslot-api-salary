# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>report service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = report.py

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
from typing import Dict, List, Tuple, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_xtbb import XtbXtbbCurd
from deploy.curd.xtb_xtbb_field import XtbXtbbFieldCurd
from deploy.schema.dao.xtb_xtbb import XtbXtbbModel
from deploy.schema.dao.xtb_xtbb_field import XtbXtbbFieldModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_xtbb import (xtb_xtbb_list_fields, xtb_xtbb_detail_fields,
                                        xtb_xtbb_view_fields, xtb_xtbb_download_fields)
from deploy.schema.dto.xtb_xtbb_field import (xtb_xtbb_field_list_fields, xtb_xtbb_field_detail_fields,
                                             xtb_xtbb_field_view_fields)
from deploy.utils.utils import get_now, md5 as generator_md5, d2s


class SystemConfigReportService:

    def __init__(self, db_connection: AsyncSession):
        self.db: AsyncSession = db_connection
        self.xtb_xtbb_curd: XtbXtbbCurd = XtbXtbbCurd()
        self.xtb_xtbb_field_curd: XtbXtbbFieldCurd = XtbXtbbFieldCurd()

    def __str__(self):
        return "SystemConfigReportService class."

    def __repr__(self):
        return self.__str__()

    # ======================== xtb_xtbb ========================

    async def __valid_model_by_md5(
            self,
            md5: str,
            status_check: bool = True,
            response_type: str = "model",
            fields: Union[List, None] = xtb_xtbb_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少md5参数")

        model: XtbXtbbModel = await self.xtb_xtbb_curd.get_by_md5(db=self.db, md5=md5)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbXtbbModel] = await self.xtb_xtbb_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            content=params.get("content")
        )
        if not models:
            __data = {
                "list": [],
                "page": params.get("page"),
                "pageSize": params.get("limit"),
                "total": 0
            }
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA, data=__data)

        id_value: int = params.get("offset") + 1
        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_xtbb_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_xtbb_curd.count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_xtbb_detail_fields
        )
        return SuccessStatus(data=data) if __flag else data

    async def add(self, rtx_id: str, model: Dict) -> Status:
        db_model: XtbXtbbModel = await self.xtb_xtbb_curd.get_by_name(
            db=self.db,
            name=model.get("name"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="报表名称已存在，请更换")

        new_model: XtbXtbbModel = await self.xtb_xtbb_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('name')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_xtbb_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        # 不可用更新字段
        del model["md5"]
        del model["name"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_xtbb_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_xtbb_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.xtb_xtbb_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.xtb_xtbb_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def download(self, params: dict) -> List:
        models = await self.xtb_xtbb_curd.download(db=self.db, params=params)
        data: List = list()
        _id = 1
        for u in models:
            if not u: continue
            _d: Dict | None = await model_converter_dict(model=u, fields=xtb_xtbb_download_fields)
            if not _d: continue
            _d["序号"] = _id
            _id += 1
            data.append(_d)
        return data

    # ======================== xtb_xtbb_field ========================

    async def __valid_field_model_by_md5(
            self,
            md5: str,
            status_check: bool = True,
            response_type: str = "model",
            fields: Union[List, None] = xtb_xtbb_field_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少md5参数")

        model: XtbXtbbFieldModel = await self.xtb_xtbb_field_curd.get_by_md5(db=self.db, md5=md5)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def field_list_by_xtbb(self, rtx_id: str, xtbb: str) -> Status:
        models: List[XtbXtbbFieldModel] = await self.xtb_xtbb_field_curd.list_by_xtbb(
            db=self.db, xtbb=xtbb
        )
        if not models:
            return SuccessStatus(data=[])

        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_xtbb_field_list_fields
        )
        return SuccessStatus(data=data)

    async def field_column_by_xtbb(self, rtx_id: str, xtbb: str) -> Status:
        models: List[XtbXtbbFieldModel] = await self.xtb_xtbb_field_curd.list_by_xtbb(
            db=self.db, xtbb=xtbb
        )
        if not models:
            return SuccessStatus(data=[])

        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_xtbb_field_list_fields
        )
        return SuccessStatus(data=data)

    async def field_add(self, rtx_id: str, model: Dict) -> Status:
        if not model.get("xtbb"):
            return FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少xtbb参数")

        new_model: XtbXtbbFieldModel = await self.xtb_xtbb_field_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('field')}-{model.get('xtbb_md5')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_xtbb_field_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def field_update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_field_model_by_md5(
            md5=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_xtbb_field_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def field_delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_field_model_by_md5(
            md5=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_xtbb_field_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def field_batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.xtb_xtbb_field_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.xtb_xtbb_field_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")
