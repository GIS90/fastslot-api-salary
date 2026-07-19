# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>enum_value service

base_info:
    __author__ = PyGo
    __time__ = 2026/6/6 22:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = enum_value.py

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
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.service.system.config.xtcs import SystemConfigXtcsService
from deploy.schema.dao.csb_enum_value import CsbEnumValueModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, option_converter_dict
from deploy.config import (redis_host, redis_port, redis_password, redis_db)
from deploy.delib.redis_lib import RedisClientLib
from deploy.utils.utils import format_redis_key


class SystemConfigEnumVService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemConfigEnumVService class initialize
        """
        self.db: AsyncSession = db_connection
        self.redis_cli = RedisClientLib(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        self.csb_ev_curd: CsbEnumValueCurd = CsbEnumValueCurd()
        self.system_config_xtcs_service: SystemConfigXtcsService = SystemConfigXtcsService(db_connection=db_connection)

    def __str__(self):
        return "SystemConfigEnumVService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List[Dict] = '',
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

    async def get_select_option_data(self, name: str, lock_view: bool = False) -> List:
        if not name: return []
        enum_v_model = await self.csb_ev_curd.get_list_by_name(db=self.db, name=name)
        return [] if not enum_v_model else await option_converter_dict(enum_v_model, lock_view=lock_view)

    async def enum_by_name_money(
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


    # 更新的时候删除 "option", "dict 缓存