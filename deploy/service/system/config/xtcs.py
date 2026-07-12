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
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_xtcs import (xtb_xtcs_list_fields, xtb_xtcs_detail_fields,
                                        xtb_xtcs_view_fields, xtb_xtcs_download_fields)
from deploy.utils.utils import get_now, md5 as generator_md5, d2s


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

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbXtcsModel] = await self.xtb_xtcs_curd.get_pagination(
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
            fields=xtb_xtcs_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_xtcs_curd.get_count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_key(
            query_id=md5,
            status_check=False,
            response_type="dict",
            query_type="md5",
            fields=xtb_xtcs_detail_fields,
            lock_check=False
        )
        return SuccessStatus(data=data) if __flag else data

    async def status(self, rtx_id: str, params: Dict) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_key(
            query_id=params.get("md5"), status_check=True, response_type="model", query_type="md5", lock_check=False
        )
        if not __flag: return data

        setattr(data, "lock", params.get("value"))
        await self.xtb_xtcs_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def add(self, rtx_id: str, model: Dict) -> Status:
        db_model: XtbXtcsModel = await self.xtb_xtcs_curd.get_by_key(
            db=self.db,
            key=model.get("key"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="参数名称已存在，请更换")

        new_model: XtbXtcsModel = await self.xtb_xtcs_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('key')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.lock = False
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_xtcs_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5_or_key(
            query_id=_md5, status_check=True, response_type="model", query_type="md5", lock_check=True
        )
        if not __flag: return data

        del model["md5"]
        if model.get("key"): del model["key"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_xtcs_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_key(
            query_id=md5, status_check=True, response_type="model", query_type="md5", lock_check=False
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_xtcs_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.xtb_xtcs_curd.get_count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.xtb_xtcs_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def view(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_key(
            query_id=md5,
            status_check=False,
            response_type="dict",
            query_type="md5",
            fields=xtb_xtcs_view_fields,
            lock_check=False
        )
        return SuccessStatus(data=data) if __flag else data


    async def download(self, params: dict) -> List:
        models = await self.xtb_xtcs_curd.download(db=self.db, params=params)
        data: List = list()
        _id = 1
        for u in models:
            if not u: continue
            _d = await model_converter_dict(model=u, fields=xtb_xtcs_download_fields)
            _d["序号"] = _id
            _id +=  1
            data.append(_d)
        return data