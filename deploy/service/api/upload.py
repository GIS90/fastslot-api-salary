# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/7/26 01:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = upload.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import os
from datetime import datetime
from typing import List, Dict
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.upload import uploadUtils
from deploy.utils.enumeration import FileTypeEnum
from deploy.utils.utils import get_now, d2s, md5 as generator_md5
from deploy.curd.xtb_user_avatar import XtbUserAvatarCurd
from deploy.schema.dao.xtb_user_avatar import XtbUserAvatarModel
from deploy.delib.store_lib import QiNiuStoreLib
from deploy.config import store_yun_access, store_yun_secret, store_yun_base, store_yun_space


class ApiUploadService:
    """
    ApiUploadService Service
    """
    def __init__(self, db_connection: AsyncSession):
        """
        ApiUploadService class initialize
        """
        self.db: AsyncSession = db_connection
        self.upload_utils: uploadUtils = uploadUtils()
        self.xtb_user_avatar_curd: XtbUserAvatarCurd = XtbUserAvatarCurd()
        # 定义文件读取默认大小
        self.READ_SIZE: int = 1024 * 1024  # 1024 = 1KB  1024 * 1024 = 1MB
        # 云存储
        self.qn_store: QiNiuStoreLib = QiNiuStoreLib(
            space_url=store_yun_base,
            space_name=store_yun_space,
            access_key=store_yun_access,
            secret_key=store_yun_secret
        )

    def __str__(self):
        return "ApiUploadService class."

    def __repr__(self):
        return self.__str__()

    async def upload(
            self,
            rtx_id: str,
            upload_type: str,
            file_: UploadFile
            # response_type: Literal["status", "dict"] = "status",
    ) -> Status:
        return await self.upload_utils.upload(rtx_id=rtx_id, upload_type=upload_type, file_=file_)

    async def uploads(self, rtx_id: str, upload_type: str, files_: List[UploadFile],
                      avatar_params: Dict | None = None) -> Status:
        __request_len: int = len(files_)
        __success_list: int = 0
        for f in files_:
            if not f: continue
            # 头像批量上传需在文件上传前缓存文件信息（upload后流已被读取）
            __file_name: str = getattr(f, 'filename', '') or ''
            __file_size: int = getattr(f, 'size', 0) or 0
            result = await self.upload_utils.upload(rtx_id=rtx_id, upload_type=upload_type, file_=f)
            if result.dict().get("code") == 100:
                __success_list += 1
                # 头像类型：上传成功后自动写入头像库记录
                if upload_type == str(FileTypeEnum.AVATAR.value):
                    await self.__create_avatar_record(
                        rtx_id=rtx_id,
                        file_name=__file_name,
                        file_size=__file_size,
                        url=result.dict().get("data", {}).get("url"),
                        avatar_params=avatar_params or {}
                    )
        __data: Dict = {
            "total": __request_len,
            "success": __success_list,
            "failed": __request_len - __success_list
        }
        if __success_list == __request_len:
            return SuccessStatus(data=__data)
        elif __success_list == 0:
            return FailureStatus(code=status_code.CODE_460_REQUEST_FILES_UPLOAD_ALL_FAILURE.value)
        else:
            return FailureStatus(
                code=status_code.CODE_461_REQUEST_FILES_UPLOAD_PART_FAILRE.value,
                data=__data)

    async def __create_avatar_record(self, rtx_id: str, file_name: str, file_size: int, url: str,
                                      avatar_params: Dict | None = None) -> None:
        """
        批量上传头像文件成功后，自动写入xtb_user_avatar头像库记录
        """
        if not url: return
        __base_name: str = os.path.splitext(file_name)[0][:35] or "头像"
        __format: str = os.path.splitext(file_name)[1].lstrip('.').upper() or 'PNG'
        # 名称重复时追加时间戳区分
        if await self.xtb_user_avatar_curd.get_by_name(db=self.db, name=__base_name):
            __base_name = f"{__base_name[:28]}-{get_now(format_='%H%M%S')}"[:35]

        avatar_params = avatar_params or {}
        __now = datetime.now()
        model: XtbUserAvatarModel = await self.xtb_user_avatar_curd.new_model()
        model.md5 = generator_md5(v=f"{__base_name}-{d2s(__now)}-{rtx_id}")
        model.name = __base_name
        model.url = url
        model.or_url = url
        model.format = __format
        model.size = file_size
        model.width = 0
        model.height = 0
        model.count = 0
        # 公共属性（类型/标签/备注/锁定）
        model.type = avatar_params.get("type") or ""
        model.tag = avatar_params.get("tag") or ""
        model.summary = avatar_params.get("summary") or ""
        model.lock = bool(avatar_params.get("lock", False))
        model.status = False
        model.create_rtx = rtx_id
        model.create_time = __now
        await self.xtb_user_avatar_curd.add(db=self.db, model=model)