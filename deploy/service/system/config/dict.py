# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>dict service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/7/19 16:03
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = dict.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import json
from typing import Dict, List, Tuple, Literal, Any, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.csb_enum_key import CsbEnumKeyCurd
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.service.system.config.xtcs import SystemConfigXtcsService
from deploy.schema.dao.csb_enum_key import CsbEnumKeyModel
from deploy.schema.dao.csb_enum_value import CsbEnumValueModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, option_converter_dict, many_model_converter_dict
from deploy.schema.dto.csb_enum_key import csb_ek_list_fields, csb_ek_detail_fields
from deploy.schema.dto.csb_enum_value import csb_ev_list_fields, csb_ev_detail_fields
from deploy.config import (redis_host, redis_port, redis_password, redis_db)
from deploy.delib.redis_lib import RedisClientLib
from deploy.utils.utils import format_redis_key, get_now, md5 as generator_md5


class SystemConfigDictService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemConfigDictService class initialize
        """
        self.db: AsyncSession = db_connection
        self.redis_cli = RedisClientLib(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        self.csb_ek_curd: CsbEnumKeyCurd = CsbEnumKeyCurd()
        self.csb_ev_curd: CsbEnumValueCurd = CsbEnumValueCurd()
        self.system_config_xtcs_service: SystemConfigXtcsService = SystemConfigXtcsService(db_connection=db_connection)

    def __str__(self):
        return "SystemConfigDictService class."

    def __repr__(self):
        return self.__str__()

    async def __dk_valid_model_by_md5_or_key(
            self,
            query_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            query_type: Literal["md5", "key"] = "md5",
            fields: Union[List, None] = csb_ek_detail_fields,
            lock_check: bool = False
    ) -> Tuple[bool, Any]:
        if not query_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数" if query_type == "md5" else "缺少key参数")

        model: CsbEnumKeyModel = await self.csb_ek_curd.get_by_md5(db=self.db, md5=query_id, filter_lock=False) if query_type == "md5" \
            else await self.csb_ek_curd.get_by_key(db=self.db, key=query_id, filter_lock=False)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if lock_check and getattr(model, "lock", None):
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def __de_valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: Union[List, None] = csb_ev_detail_fields,
            lock_check: bool = False
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: CsbEnumValueModel = await self.csb_ev_curd.get_by_md5(db=self.db, md5=md5_id, filter_lock=False)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if lock_check and getattr(model, "lock", None):
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def dict_value_by_name_money(
            self,
            name: str,
            response_: Literal["option", "dict"] = "dict",
            filter_lock: bool = True,
            key_trans_int: bool = False,
        ) -> Union[List, Dict, None]:
        """
        枚举值
        获取机制：Redis -> 数据库
        :param name: 枚举值名称
        :param response_: 枚举值返回类型 option|dict
        :param filter_lock: 是否过滤锁
        :param key_trans_int: 是否将key转为int

        更新的时候删除 "option", "dict 缓存
        """
        if response_ not in ["option", "dict"]:
            return None
        # redis 缓存
        __ev_redis_key = format_redis_key(key=name, type_="ev", ev_response=response_, ev_filter_lock=filter_lock)
        if self.redis_cli.connection:
            ev_redis_value = self.redis_cli.get_key(key=__ev_redis_key)
            if ev_redis_value and ev_redis_value != "null": return json.loads(ev_redis_value)

        # 数据库
        models = await self.csb_ev_curd.get_list_by_name(db=self.db, name=name, filter_lock=filter_lock)
        if not models: return None
        if response_ == "dict":
            __ev_value: Dict = {}
            for model in models:
                if not model or not getattr(model, "key") or not getattr(model, "value"): continue
                __key = int(getattr(model, "key")) if key_trans_int else getattr(model, "key")
                __ev_value[__key] = getattr(model, "value")
        else:
            __ev_value: List = await option_converter_dict(models=models, key_trans_int=key_trans_int, lock_view=True)
        if __ev_value and self.redis_cli.connection:
            self.redis_cli.set_key(
                key=__ev_redis_key,
                value=json.dumps(__ev_value),
                ex=await self.system_config_xtcs_service.get_xtcs_redis_expire()        # 默认是秒
            )
        return __ev_value

    async def dk_pagination(self, rtx_id: str) -> Status:
        models: List[Dict] = await self.csb_ek_curd.all_(db=self.db, filter_lock=False)
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)
        __data: List[Dict] = []
        __data.extend(filter(
            lambda model: model is not None and model != {},
            [await model_converter_dict(model=model, fields=csb_ek_list_fields) for model in models]
        ))
        return SuccessStatus(data=__data)

    async def dk_one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__dk_valid_model_by_md5_or_key(
            query_id=md5,
            status_check=False,
            response_type="dict",
            query_type="md5",
            fields=csb_ek_detail_fields,
            lock_check=False
        )
        return SuccessStatus(data=data) if __flag else data

    async def dk_status(self, rtx_id: str, params: Dict) -> Status:
        __flag, data = await self.__dk_valid_model_by_md5_or_key(
            query_id=params.get("md5"), status_check=True, response_type="model", query_type="md5", lock_check=False
        )
        if not __flag: return data

        setattr(data, "lock", params.get("value"))
        await self.csb_ek_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def dk_add(self, rtx_id: str, model: Dict) -> Status:
        db_model: CsbEnumKeyModel = await self.csb_ek_curd.get_by_key(
            db=self.db,
            key=model.get("key"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="数据字典分类标识已存在，请更换")

        new_model: CsbEnumKeyModel = await self.csb_ek_curd.new_model()
        __now = get_now()
        new_model.md5 = generator_md5(v=f"{model.get('key')}-{__now}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.lock = False
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.csb_ek_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def dk_update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__dk_valid_model_by_md5_or_key(
            query_id=_md5, status_check=True, response_type="model", query_type="md5", lock_check=True
        )
        if not __flag: return data

        del model["md5"]
        if model.get("key"): del model["key"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.csb_ek_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def dk_delete(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__dk_valid_model_by_md5_or_key(
            query_id=md5, status_check=True, response_type="model", query_type="md5", lock_check=False
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.csb_ek_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def de_pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[CsbEnumValueModel] = await self.csb_ev_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            name=params.get("content"),
            filter_lock=False
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
            fields=csb_ev_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.csb_ev_curd.count(db=self.db, name=params.get("content"), filter_lock=False)
        }
        return SuccessStatus(data=result)

    async def de_one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__de_valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields=csb_ev_detail_fields,
            lock_check=False
        )
        return SuccessStatus(data=data) if __flag else data

    async def de_status(self, rtx_id: str, params: Dict) -> Status:
        __flag, data = await self.__de_valid_model_by_md5(
            md5_id=params.get("md5"), status_check=True, response_type="model", lock_check=False
        )
        if not __flag: return data

        setattr(data, "lock", params.get("value"))
        await self.csb_ev_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def de_add_init(self, rtx_id: str,) -> Status:
        models: List[Dict] = await self.csb_ek_curd.all_(db=self.db, filter_lock=False)
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)
        __data: List[Dict] = await option_converter_dict(models=models, lock_view=False)
        return SuccessStatus(data=__data)

    async def de_add(self, rtx_id: str, model: Dict) -> Status:
        db_model: CsbEnumValueModel = await self.csb_ev_curd.get_by_key_name(
            db=self.db,
            key=model.get("key"),
            name=model.get("name"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="数据字典枚举标识已存在，请更换")

        new_model: CsbEnumValueModel = await self.csb_ev_curd.new_model()
        __now = get_now()
        new_model.md5 = generator_md5(v=f"{model.get('key')}-{__now}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.lock = False
        new_model.status = False
        print("*" * 100)
        print(model)
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.csb_ev_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def de_update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__de_valid_model_by_md5(
            md5_id=_md5, status_check=True, response_type="model", lock_check=True
        )
        if not __flag: return data

        del model["md5"]
        if model.get("key"): del model["key"]
        if model.get("name"): del model["name"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.csb_ev_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def de_delete(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__de_valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", lock_check=False
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.csb_ev_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def de_batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.csb_ev_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.csb_ev_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")
