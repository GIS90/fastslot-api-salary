# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/8/8 12:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = pdf2word.py

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
from typing import Dict, List, Tuple, Literal, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.tool_office_pdf import ToolOfficePdfCurd
from deploy.schema.dao.tool_office_pdf import ToolOfficePdfModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.tool_office_pdf2word import (
    tool_office_pdf2word_detail_fields,
    tool_office_pdf2word_download_fields,
    tool_office_pdf2word_list_fields
)
from deploy.utils.utils import get_now, md5 as generator_md5, d2s, format_redis_key
from deploy.utils.enumeration import XtbXtcsKEY



class ToolOfficePdf2WordService:

    def __init__(self, db_connection: AsyncSession):
        """
        ToolOfficePdf2WordService class initialize
        """
        self.db: AsyncSession = db_connection
        self.tool_office_pdf_curd: ToolOfficePdfCurd = ToolOfficePdfCurd()

    def __str__(self):
        return "ToolOfficePdf2WordService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            rtx_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: Union[List, None] = tool_office_pdf2word_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: ToolOfficePdfModel = await self.tool_office_pdf_curd.get_by_md5(db=self.db, md5=query_id, filter_lock=False)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[ToolOfficePdfModel] = await self.tool_office_pdf_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            rtx_id=rtx_id,
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
            fields=tool_office_pdf2word_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.tool_office_pdf_curd.count(self.db)
        }
        return SuccessStatus(data=result)
    #
    # async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
    #     __flag, data = await self.__valid_model_by_md5_or_key(
    #         query_id=md5,
    #         status_check=False,
    #         response_type="dict",
    #         query_type="md5",
    #         fields=xtb_xtcs_detail_fields,
    #         lock_check=False
    #     )
    #     return SuccessStatus(data=data) if __flag else data
    #
    # async def status(self, rtx_id: str, params: Dict) -> Status:
    #     __flag, data = await self.__valid_model_by_md5_or_key(
    #         query_id=params.get("md5"), status_check=True, response_type="model", query_type="md5", lock_check=False
    #     )
    #     if not __flag: return data
    #
    #     setattr(data, "lock", params.get("value"))
    #     await self.tool_office_pdf_curd.update(db=self.db, model=data)
    #     return SuccessStatus()
    #
    # async def __redis_key(self, key: str) -> str:
    #     xtcs_response: str = "int" if key in self.XTCS_INT_LIST else "str"
    #     return format_redis_key(
    #         key=key,
    #         type_="xtcs",
    #         xtcs_response=xtcs_response
    #     )
    #
    # async def get_xtcs_redis_expire(self):
    #     """获取系统参数设置的Rides缓存有效期"""
    #     # redis
    #     redis_key = await self.__redis_key(key=XtbXtcsKEY.REDIS_CACHE_EXPIRE.value)
    #     if self.redis_cli.connection:
    #         redis_value = self.redis_cli.get_key(key=redis_key)
    #         if redis_value: return int(redis_value)
    #     # 数据库
    #     model = await self.tool_office_pdf_curd.get_by_key(db=self.db, key=XtbXtcsKEY.REDIS_CACHE_EXPIRE.value, filter_lock=True)
    #     if model and getattr(model, "value", None):
    #         if self.redis_cli.connection:
    #             self.redis_cli.set_key(key=redis_key, value=getattr(model, "value"))
    #         return getattr(model, "value")
    #     # 默认
    #     __rv_expire: int = _REDIS_EXPIRE_DEFAULT * 60
    #     if self.redis_cli.connection:
    #         self.redis_cli.set_key(key=redis_key, value=__rv_expire)
    #     return __rv_expire
    #
    # async def add(self, rtx_id: str, model: Dict) -> Status:
    #     db_model: XtbXtcsModel = await self.tool_office_pdf_curd.get_by_key(
    #         db=self.db,
    #         key=model.get("key"))
    #     if db_model:
    #         return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
    #                              message="参数名称已存在，请更换")
    #
    #     new_model: XtbXtcsModel = await self.tool_office_pdf_curd.new_model()
    #     __now = datetime.now()
    #     new_model.md5 = generator_md5(v=f"{model.get('key')}-{d2s(__now)}-{rtx_id}")
    #     new_model.create_time = __now
    #     new_model.create_rtx = rtx_id
    #     new_model.lock = False
    #     new_model.status = False
    #     for k, v in model.items():
    #         setattr(new_model, k, v)
    #     await self.tool_office_pdf_curd.add(db=self.db, model=new_model)
    #     return SuccessStatus()
    #
    # async def update(self, rtx_id: str, model: Dict) -> Status:
    #     _md5: str = model.get("md5")
    #     __flag, data = await self.__valid_model_by_md5_or_key(
    #         query_id=_md5, status_check=True, response_type="model", query_type="md5", lock_check=True
    #     )
    #     if not __flag: return data
    #
    #     del model["md5"]
    #     if model.get("key"): del model["key"]
    #     model["update_rtx"] = rtx_id
    #     model["update_time"] = get_now()
    #     for k, v in model.items():
    #         setattr(data, k, v)
    #     await self.tool_office_pdf_curd.update(db=self.db, model=data)
    #     return SuccessStatus()
    #
    # async def delete_(self, rtx_id: str, md5: str) -> Status:
    #     __flag, data = await self.__valid_model_by_md5_or_key(
    #         query_id=md5, status_check=True, response_type="model", query_type="md5", lock_check=False
    #     )
    #     if not __flag: return data
    #
    #     setattr(data, "status", True)
    #     setattr(data, "delete_rtx", rtx_id)
    #     setattr(data, "delete_time", get_now())
    #     await self.tool_office_pdf_curd.update(db=self.db, model=data)
    #     return SuccessStatus()
    #
    # async def batch_delete(self, rtx_id: str, md5_list: List) -> Status:
    #     query_count: int = await self.tool_office_pdf_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
    #     if not query_count:
    #         return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
    #     request_count: int = len(md5_list)
    #     await self.tool_office_pdf_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
    #     return SuccessStatus() if query_count == request_count \
    #         else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
    #                            message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")
    #
    # async def view(self, rtx_id: str, md5: str) -> Status:
    #     __flag, data = await self.__valid_model_by_md5_or_key(
    #         query_id=md5,
    #         status_check=False,
    #         response_type="dict",
    #         query_type="md5",
    #         fields=xtb_xtcs_view_fields,
    #         lock_check=False
    #     )
    #     return SuccessStatus(data=data) if __flag else data
    #
    # async def download(self, params: dict) -> List:
    #     models = await self.tool_office_pdf_curd.download(db=self.db, params=params)
    #     data: List = list()
    #     _id = 1
    #     for u in models:
    #         if not u: continue
    #         _d = await model_converter_dict(model=u, fields=xtb_xtcs_download_fields)
    #         _d["序号"] = _id
    #         _id +=  1
    #         data.append(_d)
    #     return data