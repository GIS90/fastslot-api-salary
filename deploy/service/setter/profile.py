# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/5/11 22:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = profile.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_user import XtbUserCurd
from deploy.curd.xtb_request import XtbRequestCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_user import xtb_user_detail_fields
from deploy.schema.dto.xtb_request import profile_request_list_fields
from deploy.utils.utils import get_now, md5 as generator_md5
from deploy.config import server_user as SERVER_USER_ADMIN


class SetterProfileService:

    def __init__(self, db_connection: AsyncSession):
        """
        SetterProfileService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_curd: XtbUserCurd = XtbUserCurd()
        self.xtb_request_curd: XtbRequestCurd = XtbRequestCurd()

    def __str__(self):
        return "SetterProfileService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_rtx(
            self,
            rtx_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List[Dict] = xtb_user_detail_fields,
            admin_check: bool = False
    ) -> Tuple[bool, Any]:
        if not rtx_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少rtx-id参数")

        model: XtbUserModel = await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=rtx_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if admin_check and getattr(model, "rtx_id") ==  SERVER_USER_ADMIN:
            return False, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def profile_detail(self, rtx_id: str) -> Status:
        __flag, data = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=False, response_type="model", admin_check=False
        )
        if not __flag: return data

        user = {
            "userId": getattr(data, "rtx_id"),
            "userName": getattr(data, "name"),
            "sex": getattr(data, "sex") or "NO",
            "email": getattr(data, "email"),
            "phone": getattr(data, "phone"),
            "introduction": getattr(data, "introduction"),
        }
        # sex_enum_model = self.csb_enum_value_bo.get_model_by_name(name=CsbEnum.SEX_TYPE.value)
        # data = {
        #     "user": user,
        #     "sexEnum": csb_enum_value_to_option(sex_enum_model) if sex_enum_model else []
        # }
        _d = {
            "user": user,
            "sexEnum": [
                {"label": "男", "value": "M", "disabled": False},
                {"label": "女", "value": "F", "disabled": False},
                {"label": "未知", "value": "NO", "disabled": True},
            ]
        }
        return SuccessStatus(data=_d)

    async def profile_update(self, rtx_id: str, model: Dict) -> Status:
        __flag, data = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=False, response_type="model", admin_check=False
        )
        if not __flag: return data

        setattr(data, "name", model.get("userName"))
        setattr(data, "sex", model.get("sex"))
        setattr(data, "email", model.get("email"))
        setattr(data, "phone", model.get("phone"))
        setattr(data, "introduction", model.get("introduction"))
        setattr(data, "update_rtx", rtx_id)
        setattr(data, "update_time", get_now())
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def profile_password(self, rtx_id: str, model: dict) -> Status:
        __flag, data = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=False, response_type="model", admin_check=False
        )
        if not __flag: return data

        # 原密码不匹配
        user_model_password = getattr(data, "password")   # 加密后
        userPassword = model.get("userPassword")  # 未加密
        userPassword_md5 = generator_md5(v=userPassword)
        if userPassword_md5 != user_model_password:
            return FailureStatus(
                code=status_code.CODE_205_USER_OLD_PASSWORD_ERROR.value)
        # 新密码与确认密码不匹配
        newPassword = model.get("newPassword")
        confirmPassword = model.get("confirmNewPassword")
        if newPassword != confirmPassword:
            return FailureStatus(
                code=status_code.CODE_206_USER_NEW_PASSWORD_NOT_MATCH.value)

        setattr(data, "password", generator_md5(v=newPassword))
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def profile_log(self, rtx_id: str, params: dict) -> Status:
        models: List = await self.xtb_request_curd.get_pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            rtx_id=rtx_id
        )
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        data: List = list()
        id_value: int = params.get("offset") + 1
        __tag = {
            "GET": "primary",
            "POST": "success",
            "PUT": "warning",
            "DELETE": "danger",
        }
        for model in models:
            _d = await model_converter_dict(model=model, fields=profile_request_list_fields)
            if not _d: continue
            _d["id"] = id_value
            id_value += 1
            # TODO tag去系统表维护的数据，目前暂时写死
            _d["tag"] = __tag.get(_d.get("method")) if _d.get("method") else "info"
            data.append(_d)
        result: Dict = {
            "list": data,
            "total": await self.xtb_request_curd.get_count(self.db, rtx_id),
            "page": params.get("page"),
            "pageSize": params.get("limit")
        }
        return SuccessStatus(data=result)

    # async def profile_avatar(self, token_rtx_id: str, image_file: UploadFile) -> Status:
    #     # ============= 1、image format check =============
    #     image_name = image_file.filename
    #     if not self.image_lib.legal(image_name):
    #         return FailureStatus(
    #             status_id=Status_code.CODE_454_REQUEST_FILE_NOT_SUPPORT.value,
    #             message="图片格式不支持")
    #     # ============= 2、local store =============
    #     local_res = await self.image_lib.save(image_file, compress=False, _type="uf")
    #     if local_res.get('status_id') != 100:
    #         return FailureStatus(
    #             status_id=Status_code.CODE_456_REQUEST_FILE_LOCAL_STORE_FAILURE.value,
    #             message=local_res.get('message') or '服务器本地存储失败')
    #
    #     local_image_file = local_res.get('data').get('file')
    #     # local_image_file_info = self.image_lib.scan(local_image_file)     # 图片信息
    #     # ============= 3、cloud store =============
    #     cloud_image_name = '%s/%s' % (get_now(format="%Y%m%d"), local_res.get('data').get('name'))
    #     cloud_res = self.cloud_lib.upload(store_name=cloud_image_name, local_file=local_image_file)
    #     if cloud_res.get('status_id') != 100:
    #         return FailureStatus(
    #             status_id=Status_code.CODE_457_REQUEST_FILE_YUN_STORE_FAILURE.value,
    #             message=local_res.get('message') or '服务器云存储失败')
    #     # ============= 4、更新数据 =============
    #     new_image_url = cloud_res.get('data').get('url')
    #     try:
    #         user_model = self._get_valid_user(rtx_id=token_rtx_id, format_dict=False)
    #         setattr(user_model, "avatar", new_image_url)
    #         self.xtb_sysuser_bo.merge_model(user_model)
    #     except:
    #         return FailureStatus(
    #             status_id=Status_code.CODE_603_DB_UPDATE_FAILURE.value)
    #
    #     return SuccessStatus(data={"url": new_image_url})
    #
