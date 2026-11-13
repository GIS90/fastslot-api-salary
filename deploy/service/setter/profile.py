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
from fastapi import UploadFile
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_user import XtbUserCurd
from deploy.curd.xtb_request import XtbRequestCurd
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.curd.xtb_user_avatar import XtbUserAvatarCurd
from deploy.curd.xtb_user_avatar_favorite import XtbUserAvatarFavoriteCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.service.system.config.dict import SystemConfigDictService
from deploy.service.system.ops.log import SystemOpsLogService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_user import xtb_user_detail_fields
from deploy.schema.dto.xtb_request import profile_request_list_fields
from deploy.utils.utils import get_now, md5 as generator_md5
from deploy.config import server_user as SERVER_USER_ADMIN
from deploy.delib.image_lib import ImageLib
from deploy.delib.store_lib import QiNiuStoreLib
from deploy.config import store_yun_access, store_yun_secret, store_yun_base, store_yun_space
from deploy.utils.enumeration import CsbEnumKEY


class SetterProfileService:

    def __init__(self, db_connection: AsyncSession):
        """
        SetterProfileService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_curd: XtbUserCurd = XtbUserCurd()
        self.xtb_request_curd: XtbRequestCurd = XtbRequestCurd()
        self.csb_enum_v_curd: CsbEnumValueCurd = CsbEnumValueCurd()
        self.xtb_user_avatar_curd: XtbUserAvatarCurd = XtbUserAvatarCurd()
        self.xtb_user_avatar_favorite_curd: XtbUserAvatarFavoriteCurd = XtbUserAvatarFavoriteCurd()
        self.csb_enum_v_service: SystemConfigDictService = SystemConfigDictService(db_connection=db_connection)
        self.system_ops_log_service: SystemOpsLogService = SystemOpsLogService(db_connection=db_connection)
        self.image_lib: ImageLib = ImageLib()
        self.qiniu_store_lib: QiNiuStoreLib = QiNiuStoreLib(
            space_url=store_yun_base,
            space_name=store_yun_space,
            access_key=store_yun_access,
            secret_key=store_yun_secret
        )

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
        data = {
            "user": user,
            "sexEnum": await self.csb_enum_v_service.dict_value_by_name_money(
                name=CsbEnumKEY.SEX_TYPE.value, response_="option", filter_lock=True, key_trans_int=False)
        }
        return SuccessStatus(data=data)

    async def profile_update(self, rtx_id: str, model: Dict) -> Status:
        __flag, data = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=True, response_type="model", admin_check=False
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
            rtx_id=rtx_id, status_check=True, response_type="model", admin_check=False
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
        return await self.system_ops_log_service.pagination(rtx_id=rtx_id, params=params, _all=False)

    async def __valid_avatar_by_md5(self, md5: str) -> Tuple[bool, Any]:
        avatar = await self.xtb_user_avatar_curd.get_by_md5(db=self.db, md5=md5)
        if not avatar:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST, message="头像不存在或已删除")
        if getattr(avatar, "lock", False):
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT, message="头像已禁用，无法使用")
        return True, avatar

    async def profile_avatar_market(
            self, rtx_id: str, params: Dict, type_: str = None, favorite_status: int = None,
            sort_: str = None, content: str = None
    ) -> Status:
        __flag, data = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=True, response_type="model", admin_check=False
        )
        if not __flag: return data

        models = await self.xtb_user_avatar_favorite_curd.market_pagination(
            db=self.db,
            rtx_id=rtx_id,
            offset=params.get("offset"),
            limit=params.get("limit"),
            type_=type_,
            favorite_status=favorite_status,
            sort_=sort_,
            content=content,
        )
        avatar_list = []
        for row in models:
            item = dict(row)
            item["favorite"] = bool(item.get("favorite"))
            item["favoriteCount"] = item.pop("favorite_count", 0) or 0
            avatar_list.append(item)

        result = {
            "list": avatar_list,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_user_avatar_favorite_curd.market_count(
                db=self.db, rtx_id=rtx_id, type_=type_, favorite_status=favorite_status, content=content
            ),
        }
        return SuccessStatus(data=result)

    async def profile_avatar_favorite(self, rtx_id: str, model: Dict) -> Status:
        __flag, user = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=True, response_type="model", admin_check=False
        )
        if not __flag: return user
        __flag, avatar = await self.__valid_avatar_by_md5(md5=model.get("md5"))
        if not __flag: return avatar

        value = model.get("value")
        favorite = await self.xtb_user_avatar_favorite_curd.get_by_user_avatar(
            db=self.db, rtx_id=rtx_id, avatar_md5=avatar.md5
        )
        result = {"md5": avatar.md5, "favorite": value, "favoriteCount": avatar.favorite or 0}

        __now: str = get_now()
        if not favorite:
            if not value:
                return SuccessStatus(data=result)
            favorite = await self.xtb_user_avatar_favorite_curd.new_model()
            favorite.md5 = generator_md5(v=f"{rtx_id}-{avatar.md5}-{__now}")
            favorite.rtx_id = rtx_id
            favorite.avatar_md5 = avatar.md5
            favorite.create_rtx = rtx_id
            favorite.create_time = __now
            favorite.status = False
            await self.xtb_user_avatar_favorite_curd.add(db=self.db, model=favorite)
            # 同步头像表收藏次数
            avatar.favorite = (avatar.favorite or 0) + 1
            avatar.update_rtx = rtx_id
            avatar.update_time = __now
            await self.xtb_user_avatar_curd.update(db=self.db, model=avatar)
            result["favoriteCount"] = avatar.favorite
            return SuccessStatus(data=result)

        target_status = not value
        if favorite.status != target_status:
            favorite.status = target_status
            favorite.update_rtx = rtx_id
            favorite.update_time = __now
            favorite.delete_rtx = None if value else rtx_id
            favorite.delete_time = None if value else __now
            await self.xtb_user_avatar_favorite_curd.update(db=self.db, model=favorite)
            # 同步头像表收藏次数（收藏+1，取消收藏-1，最小为0）
            avatar.favorite = max(0, (avatar.favorite or 0) + (1 if value else -1))
            avatar.update_rtx = rtx_id
            avatar.update_time = __now
            await self.xtb_user_avatar_curd.update(db=self.db, model=avatar)
            result["favoriteCount"] = avatar.favorite
        return SuccessStatus(data=result)

    async def profile_avatar_set(self, rtx_id: str, md5: str) -> Status:
        __flag, user = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=True, response_type="model", admin_check=False
        )
        if not __flag: return user
        __flag, avatar = await self.__valid_avatar_by_md5(md5=md5)
        if not __flag: return avatar

        if user.avatar != avatar.url:
            _now = get_now()
            # 用户表
            user.avatar = avatar.url
            user.update_rtx = rtx_id
            user.update_time = _now
            # 头像表
            avatar.count = (avatar.count or 0) + 1
            avatar.update_rtx = rtx_id
            avatar.update_time = _now
            await self.xtb_user_curd.update(db=self.db, model=user)
            await self.xtb_user_avatar_curd.update(db=self.db, model=avatar)
        return SuccessStatus(data={"url": avatar.url, "count": avatar.count})

    async def profile_avatar(self, rtx_id: str, image_file: UploadFile) -> Status:
        # ======================= 1、data legal check =======================
        __flag, data = await self.__valid_model_by_rtx(
            rtx_id=rtx_id, status_check=True, response_type="model", admin_check=False
        )
        if not __flag: return data
        # ============= 2、image format check =============
        image_name = image_file.filename
        if not await self.image_lib.allow_format_img(image_name):
            return FailureStatus(
                code=status_code.CODE_454_REQUEST_FILE_NOT_SUPPORT.value,
                message="图片格式不支持")
        # ============= 3、local store =============
        local_res = await self.image_lib.store_local(image_file, compress=False, _type="uf")
        if local_res.get('code') != 100:
            return FailureStatus(
                code=status_code.CODE_456_REQUEST_FILE_LOCAL_STORE_FAILURE.value,
                message=local_res.get('message') or '服务器本地存储失败')
        local_image_file = local_res.get('data').get('file')
        # ============= 4、cloud store =============
        cloud_image_name = '%s/%s' % (get_now(format_="%Y%m%d"), local_res.get('data').get('name'))
        cloud_res = await self.qiniu_store_lib.upload(store_name=cloud_image_name, local_file=local_image_file)
        if cloud_res.get('code') != 100:
            return FailureStatus(
                code=status_code.CODE_457_REQUEST_FILE_YUN_STORE_FAILURE.value,
                message=local_res.get('message') or '服务器云存储失败')
        # ============= 5、data update =============
        new_image_url = cloud_res.get('data').get('url')
        setattr(data, "avatar", new_image_url)
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus(data={"url": new_image_url})

