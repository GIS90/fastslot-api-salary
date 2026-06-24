# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>user service

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:22
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = user.py

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
from deploy.curd.xtb_user import XtbUserCurd
from deploy.curd.xtb_xtcs import XtbXtcsCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.schema.dao.xtb_xtcs import XtbXtcsModel
from deploy.service.system.config.enum_value import SystemConfigEnumVService
from deploy.service.system.main.role import SystemMainRoleService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_user import (xtb_user_list_fields, xtb_user_detail_fields,
                                        xtb_user_login_fields, xtb_user_download_fields)
from deploy.utils.utils import get_now, random_string, md5 as generator_md5, d2s
from deploy.config import server_user, server_password, server_avatar
from deploy.utils.enumeration import XtbXtcsKEY, CsbEnumKEY


_SERVER_USER_ADMIN: str = server_user
_SERVER_USER_DEFAULT_PASSWORD: str = server_password
_SERVER_USER_DEFAULT_AVATAR: str = server_avatar


class SystemMainUserService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemMainUserService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_curd: XtbUserCurd = XtbUserCurd()
        self.xtb_xtcs_curd: XtbXtcsCurd = XtbXtcsCurd()
        self.csb_enum_v_service: SystemConfigEnumVService = SystemConfigEnumVService(db_connection=db_connection)
        self.role_service: SystemMainRoleService = SystemMainRoleService(db_connection=db_connection)

    def __str__(self):
        return "SystemMainUserService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5_or_rtx(
            self,
            query_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            query_type: Literal["md5", "rtx"] = "md5",
            fields: List[Dict] = xtb_user_detail_fields,
            admin_check: bool = False
    ) -> Tuple[bool, Any]:
        if not query_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数" if query_type == "md5" else "缺少rtx-id参数")

        model: XtbUserModel = await self.xtb_user_curd.get_by_md5(db=self.db, md5=query_id) if query_type == "md5" \
            else await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=query_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT,
                                        message="用户已注销，不允许操作")
        if admin_check and getattr(model, "rtx_id") ==  _SERVER_USER_ADMIN:
            return False, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List = await self.xtb_user_curd.get_pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            content=params.get("content")
        )
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        data: List = list()
        for model in models:
            if not model: continue
            _d = await model_converter_dict(model=model, fields=xtb_user_list_fields)
            if not _d: continue
            data.append(_d)
        result: Dict = {
            "list": data,
            "total": await self.xtb_user_curd.get_count(self.db)
        }
        return SuccessStatus(data=result)

    async def login_by_rtx_id(self, rtx_id: str) -> Dict:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=rtx_id,
            status_check=False,
            response_type="dict",
            query_type="rtx",
            fields=xtb_user_login_fields,
            admin_check=False
        )
        return data if __flag else None

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=False, response_type="dict", query_type="md5", admin_check=False
        )
        if not __flag: return data

        _d = {
            "user": data,
            "sexEnum": await self.csb_enum_v_service.get_select_option_data(name=CsbEnumKEY.SEX_TYPE.value, lock_view=False),
            "roleList": await self.role_service.role_select_option()
        }
        return SuccessStatus(data=_d)

    async def depend_by_rtx_id(self, rtx_id: str) -> Dict:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=rtx_id, status_check=False, response_type="model", query_type="rtx", admin_check=False
        )
        return data if __flag else {}

    async def status(self, token_rtx_id: str, md5: str, value: bool) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=False, response_type="model", admin_check=True
        )
        if not __flag: return data

        setattr(data, "status", value)
        setattr(data, "delete_rtx", token_rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def __generator_default_password(
            self,
            password: str=_SERVER_USER_DEFAULT_PASSWORD,
            encrypt: bool=False
    ) -> str:
        """生成用户密码"""
        default_password: XtbXtcsModel = await self.xtb_xtcs_curd.get_by_key(
            db=self.db,
            key=XtbXtcsKEY.USER_DEFAULT_PASSWORD.value,
            filter_lock=True
        )
        __value: str = getattr(default_password, "value") if default_password else password
        return generator_md5(v=__value) if encrypt else __value

    async def default_pwd(self, rtx_id: str) -> Status:
        return SuccessStatus(data={"password": await self.__generator_default_password(encrypt=False)})

    async def reset_pwd(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        setattr(data, "password", await self.__generator_default_password(encrypt=True))
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()
    
    async def add_enum(self, rtx_id: str) -> Status:
        _d = {
            "sexEnum": await self.csb_enum_v_service.get_select_option_data(name=CsbEnumKEY.SEX_TYPE.value, lock_view=False),
            "roleList": await self.role_service.role_select_option()
        }
        return SuccessStatus(data=_d)
    
    async def __default_avatar(self, avatar: str=_SERVER_USER_DEFAULT_AVATAR) -> str:
        """用户默认头像"""
        default_avatar: XtbXtcsModel = await self.xtb_xtcs_curd.get_by_key(
            db=self.db,
            key=XtbXtcsKEY.USER_DEFAULT_AVATAR.value,
            filter_lock=True
        )
        __value: str = getattr(default_avatar, "value") if default_avatar else avatar
        return __value
    
    async def add(self, rtx_id: str, model: Dict) -> Status:
        db_model: XtbUserModel = await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=model.get("rtx_id"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="用户账号已存在，请更换")

        new_model: XtbUserModel = await self.xtb_user_curd.new_model()
        __salt: str = random_string(length=16)
        new_model.md5 = generator_md5(v=f"{model.get('rtx_id')}-{get_now()}-{__salt}")
        new_model.avatar = await self.__default_avatar()
        new_model.status = False
        new_model.salt = __salt
        new_model.create_time = datetime.now()
        new_model.create_rtx = rtx_id
        new_model.password = await self.__generator_default_password(encrypt=True)

        model["role"] = ','.join(model.get("role")) if model.get("role") else ""
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_user_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        del model["md5"]
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=_md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        if model.get("rtx_id"):
            del model["rtx_id"]
        model["role"] = ','.join(model.get("role")) if model.get("role") else ""
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_hard(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=True, response_type="model", query_type="md5", admin_check=True
        )
        if not __flag: return data

        await self.xtb_user_curd.delete(db=self.db, model=data)
        return SuccessStatus()


    async def delete_soft(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=True, response_type="model", query_type="md5", admin_check=True
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def __verify_contain_admin_user(self, md5_list: List) -> Tuple[bool, Any]:
        db_model: List = await self.xtb_user_curd.get_rtx_by_md5_list(db=self.db, md5_list=md5_list)
        if db_model and _SERVER_USER_ADMIN in db_model:
            return True, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="管理员用户不允许删除")
        else:
            return False, db_model

    async def batch_delete_hard(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_user(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_user_curd.batch_delete(db=self.db, md5_list=md5_list)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def batch_delete_soft(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_user(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_user_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def download(self, params: dict) -> List:
        models = await self.xtb_user_curd.download(db=self.db, params=params)
        data: List = list()
        data.extend(
            filter(
                lambda x: x is not None and x is not {},
                [await model_converter_dict(model=u, fields=xtb_user_download_fields) for u in models if u]
            )
        )
        return data
