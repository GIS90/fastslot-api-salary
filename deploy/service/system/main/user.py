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
import re
from datetime import datetime
from fastapi import UploadFile
from typing import Dict, List, Tuple, Literal, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.xtb_user import XtbUserCurd
from deploy.curd.xtb_xtcs import XtbXtcsCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.schema.dao.xtb_xtcs import XtbXtcsModel
from deploy.service.system.config.dict import SystemConfigDictService
from deploy.service.system.main.role import SystemMainRoleService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_user import (xtb_user_list_fields, xtb_user_detail_fields,
                                        xtb_user_login_fields, xtb_user_download_fields,
                                        xtb_user_import_fields)
from deploy.utils.utils import get_now, random_string, md5 as generator_md5, d2s
from deploy.config import server_user, server_password, server_avatar
from deploy.utils.enumeration import XtbXtcsKEY, CsbEnumKEY, FileTypeEnum
from deploy.utils.upload import uploadUtils
from deploy.delib.excel_lib import ExcelLib


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
        self.system_config_dict_service: SystemConfigDictService = SystemConfigDictService(db_connection=db_connection)
        self.system_main_role_service: SystemMainRoleService = SystemMainRoleService(db_connection=db_connection)
        self.upload_utils: uploadUtils = uploadUtils()
        self.excel_lib: ExcelLib = ExcelLib()

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
            fields: Union[List, None] = xtb_user_detail_fields,
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
        models: List = await self.xtb_user_curd.pagination(
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

        data: List = list()
        for model in models:
            if not model: continue
            _d = await model_converter_dict(model=model, fields=xtb_user_list_fields)
            if not _d: continue
            data.append(_d)
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_user_curd.count(self.db)
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
            "sexEnum": await self.system_config_dict_service.dict_value_by_name_money(
                name=CsbEnumKEY.SEX_TYPE.value, response_="option", filter_lock=True, key_trans_int=False
            ),
            "roleList": await self.system_main_role_service.role_select_option()
        }
        return SuccessStatus(data=_d)

    async def depend_by_rtx_id(self, rtx_id: str) -> Dict:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=rtx_id, status_check=False, response_type="model", query_type="rtx", admin_check=False
        )
        return data if __flag else {}

    async def status(self, rtx_id: str, params: Dict) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=params.get("md5"), status_check=False, response_type="model", admin_check=True
        )
        if not __flag: return data

        setattr(data, "status", params.get("value"))
        setattr(data, "delete_rtx", rtx_id)
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

    async def default_password(self, rtx_id: str) -> Status:
        return SuccessStatus(data={"password": await self.__generator_default_password(encrypt=False)})

    async def reset_password(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        setattr(data, "password", await self.__generator_default_password(encrypt=True))
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()
    
    async def add_enum(self, rtx_id: str) -> Status:
        _d = {
            "roleList": await self.system_main_role_service.role_select_option(),
            "sexEnum": await self.system_config_dict_service.dict_value_by_name_money(
                name=CsbEnumKEY.SEX_TYPE.value, response_="option", filter_lock=True, key_trans_int=False
            )
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

    async def option(self, status_view: bool = False) -> List:
        models = await self.xtb_user_curd.option(db=self.db, status=status_view)
        option_list: List = []
        for model in models:
            if not model: continue
            option_list.append({
                "label": getattr(model, "name"),
                "value": getattr(model, "rtx_id"),
                "disabled": getattr(model, "status", False)
            })
        else:
            return option_list

    @staticmethod
    async def validate_rtx_id(rtx_id: str) -> bool:
        """
        校验 rtxId 格式
        允许：大小写英文字母、数字、连字符(-)和点(.)
        不允许：空格、标点等特殊字符
        """
        pattern = r'^[a-zA-Z0-9\-\.]+$'
        return bool(re.match(pattern, rtx_id))


    async def preview(self, rtx_id: str, file_: UploadFile) -> Status:
        # 存储
        upload_result: Status = await self.upload_utils.upload(
            rtx_id=rtx_id,
            upload_type=FileTypeEnum.USER_IMPORT.value,
            file_=file_)
        if upload_result.dict().get("code") != 100:
            return upload_result
        # 读取数据
        file_local: str = upload_result.dict().get("data").get("local")
        excel_result: Dict = await self.excel_lib.read_by_cell(
            read_file=file_local,
            sheet=0,
            format_="only_new",
            request_title=True,
            response_title=False)
        if excel_result.get("code") != 100:
            return FailureStatus(
                code=excel_result.get("code"),
                message=excel_result.get("message"))
        excel_data: List = excel_result.get("data").get("data")
        if not excel_data:
            return FailureStatus(
                code=status_code.CODE_101_SUCCESS_NO_DATA,
                message="上传的模板文件不包含有效数据，请重新上传")
        if len(excel_data[0]) != 7:
            return FailureStatus(
                code=status_code.CODE_466_REQUEST_FILE_TEMPLATE_ERROR.value,
                message="上传的模板文件格式有误，请点击模板下载并重新上传")
        if len(excel_data) > 200:
            return SuccessStatus(code=status_code.CODE_453_REQUEST_FILE_EXCEED_MAX_ROW.value,
                                 message="单次导入最大数据量为200，请分批上传")
        # 格式化数据
        __data: List = []
        __upload_rtx_id_list: List = []
        index: int = 1
        for d in excel_data:
            if not d: continue
            __status: bool = False
            __message: str = ""
            # 校验一：字段不允许为空
            if not d[0]:
                __status: bool = True; __message: str = "账户不允许为空"
            if not d[1]:
                __status: bool = True; __message: str = "昵称不允许为空"
            if not d[2]:
                __status: bool = True; __message: str = "性别不允许为空"
            if not d[3]:
                __status: bool = True; __message: str = "邮箱不允许为空"
            if not d[4]:
                __status: bool = True; __message: str = "电话不允许为空"
            # 校验二：rtx-id表格人员重复
            if not __status and d[0] in __upload_rtx_id_list:
                __status: bool = True; __message: str = "用户在表格中重复"
            if d[0] not in __upload_rtx_id_list: __upload_rtx_id_list.append(d[0])
            # 校验三：rtx-id数据库人员重复
            if not __status and await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=d[0]):
                __status = True; __message="平台已存在用户账号"
            # 校验四：rtx-id规则校验
            if not __status and not await self.validate_rtx_id(rtx_id=d[0]):
                __status = True; __message: str = "账户格式不正确"
            # 校验五：长度校验
            if not __status:
                if len(d[0]) > 35: __status = True; __message: str = "账户长度必须在35个字符以内"
            if not __status:
                if len(d[1]) > 30: __status = True; __message: str = "昵称长度必须在30个字符以内"
            if not __status:
                if len(d[2]) > 2: __status = True; __message: str = "性别长度必须在2个字符以内"
            if not __status:
                if len(d[3]) > 80: __status = True; __message: str = "邮箱长度必须在80个字符以内"
            if not __status:
                if len(d[4]) != 11: __status = True; __message: str = "电话长度必须符合11位"
            if not __status and d[5]:
                if len(d[5]) > 255: __status = True; __message: str = "个性签名长度必须在255个字符以内"
            if not __status and d[6]:
                if len(d[6]) > 255: __status = True; __message: str = "角色长度必须在255个字符以内"

            __d: Dict = {
                "id": index,
                "rtxId": d[0],
                "name": d[1],
                "sex": d[2],
                "email": d[3],
                "phone": d[4],
                "introduction": d[5],
                "role": d[6],
                "status": __status,
                "message": __message
            }
            __data.append(__d)
            index += 1
        return SuccessStatus(data=__data)

    async def import_(self, rtx_id: str, data: List) -> Status:
        _success: int = 0
        for _d in data:
            if not _d or getattr(_d, "status"): continue
            result = await self.add(rtx_id=rtx_id, model=dict(_d))  # _d为XtbUserImportModel
            if result.dict().get("code") == 100: _success += 1
        _data: Dict = {
            "total": len(data),
            "success": _success,
            "failed": len(data) - _success
        }
        return SuccessStatus(data=_data)