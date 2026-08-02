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
from typing import List, Dict
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.upload import uploadUtils
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

    async def uploads(self, rtx_id: str, upload_type: str, files_: List[UploadFile]) -> Status:
        __request_len: int = len(files_)
        __success_list: int = 0
        for f in files_:
            if not f: continue
            result = await self.upload_utils.upload(rtx_id=rtx_id, upload_type=upload_type, file_=f)
            if result.dict().get("code") == 100: __success_list += 1
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