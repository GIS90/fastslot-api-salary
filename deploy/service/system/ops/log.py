# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>ops>log service

base_info:
    __author__ = PyGo
    __time__ = 2026/7/15 22:59
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = log.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Dict, List, Tuple, Literal, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_request import XtbRequestCurd
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.schema.dao.xtb_request import XtbRequestModel
from deploy.service.system.config.enum_value import SystemConfigEnumVService
from deploy.service.system.main.user import SystemMainUserService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_request import (
    xtb_request_list_fields,
    xtb_request_detail_fields,
    xtb_request_download_fields
)
from deploy.utils.utils import get_now
from deploy.utils.enumeration import CsbEnumKEY, API_TYPE_DICT


class SystemOpsLogService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemOpsLogService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_request_curd: XtbRequestCurd = XtbRequestCurd()
        self.csb_ev_curd: CsbEnumValueCurd = CsbEnumValueCurd()
        self.system_main_user_service: SystemMainUserService = SystemMainUserService(db_connection=self.db)
        self.system_config_ev_service: SystemConfigEnumVService = SystemConfigEnumVService(db_connection=self.db)

    def __str__(self):
        return "SystemOpsLogService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: Union[List, None] = xtb_request_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbRequestModel = await self.xtb_request_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def __get_tag(self, type_: Literal["option", "dict"] = "dict") -> Union[List, Dict]:
        """
        因为枚举值的tag在数据库中存储key-value反的，所以需要反转
        """
        enum_v_model = await self.csb_ev_curd.get_list_by_name(
            db=self.db,
            name=CsbEnumKEY.API_TYPE,
            filter_lock=False)
        __default: Dict = API_TYPE_DICT
        if type_ == "dict":
            __tag: Dict = {}
            if not enum_v_model: return __default
            for model in enum_v_model:
                if not model or not getattr(model, "key") or not getattr(model, "value"): continue
                __tag[str(model.value).upper()] = str(model.key).lower() if getattr(model, "value") else "info"
            else:
                return __tag
        else:
            __tag: List = []
            if not enum_v_model:
                for k in __default.keys():
                    if not k: continue
                    __tag.append({"label": k, "value": k})
            for model in enum_v_model:
                if not model or not getattr(model, "value"): continue
                __tag.append({"label": str(model.value).upper(), "value": str(model.value).upper()})
            else:
                return __tag

    async def pagination(self, rtx_id: str, params: Dict, _all: bool = False) -> Status:
        if _all:
            __rtx_id = None
            pagination_offset = (params.get("page") - 1) * params.get("pageSize")
        else:
            __rtx_id = rtx_id
            pagination_offset = params.get("offset")
            params["filter"]: Dict = {}
        models: List[XtbRequestModel] = await self.xtb_request_curd.pagination(
            db=self.db,
            offset=pagination_offset,
            limit=params.get("pageSize"),
            rtx_id=__rtx_id,
            filter_=params.get("filter")
        )
        if not models:
            __data = {
                "list": [],
                "page": params.get("page"),
                "pageSize": params.get("pageSize"),
                "total": 0
            }
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA, data=__data)

        id_value: int = pagination_offset + 1
        data: List = []
        tag: Dict = await self.__get_tag(type_="dict")
        for model in models:
            _d = await model_converter_dict(model=model, fields=xtb_request_list_fields)
            if not _d: continue
            _d["id"] = id_value
            id_value += 1
            _d["tag"] = tag.get(_d.get("method").upper()) if _d.get("method") else "info"
            data.append(_d)

        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("pageSize"),
            "total": await self.xtb_request_curd.count(self.db, rtx_id=__rtx_id, filter_=params.get("filter"))
        }
        return SuccessStatus(data=result)

    async def filter_(self, rtx_id: str) -> Status:
        data = {
            "api": await self.__get_tag(type_="option"),
            "user": await self.system_main_user_service.option(status_view=True)
        }
        return SuccessStatus(data=data)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_request_detail_fields
        )
        return SuccessStatus(data=data) if __flag else data

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5_id=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        del model["md5"]
        if model.get("key"): del model["key"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_request_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_request_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.xtb_request_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.xtb_request_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def download(self, params: dict) -> List:
        models = await self.xtb_request_curd.download(db=self.db, params=params)
        data: List = list()
        _id = 1
        for u in models:
            if not u: continue
            _d = await model_converter_dict(model=u, fields=xtb_request_download_fields)
            _d["序号"] = _id
            _id +=  1
            data.append(_d)
        return data