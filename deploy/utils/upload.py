# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    upload file utils

base_info:
    __author__ = PyGo
    __time__ = 2026/7/26 15:59
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
from pathlib import Path as pathlib_path

from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.utils import get_now, get_store_folder, default_file_suffix
from deploy.delib.store_lib import QiNiuStoreLib
from deploy.config import store_yun_access, store_yun_secret, store_yun_base, store_yun_space


class uploadUtils:
    def __init__(self):
        """
        uploadUtils class initialize
        """
        # 定义文件读取默认大小
        self.READ_SIZE = 1024 * 1024  # 1024 = 1KB  1024 * 1024 = 1MB
        # 云存储
        self.qn_store = QiNiuStoreLib(
            space_url=store_yun_base,
            space_name=store_yun_space,
            access_key=store_yun_access,
            secret_key=store_yun_secret
        )

    def __str__(self):
        return "uploadUtils class."

    def __repr__(self):
        return self.__str__()

    async def upload(
            self,
            rtx_id: str,
            upload_type: str,
            file_: UploadFile
    ) -> Status:
        # - - - - - - - - - - - - - 数据质量检查 - - - - - - - - - - - - -
        if not file_:
            return FailureStatus(code=status_code.CODE_450_REQUEST_FILE_NO_UPLOAD)
        file_name = getattr(file_, 'filename')  # use getattr method to get file name
        if not file_name:
            file_name = f"{rtx_id}-{get_now(format_="%Y-%m-%d-%H-%M-%S")}{default_file_suffix(upload_type)}"
        real_file = f"{get_store_folder(add_date=True)}/{file_name}"
        if pathlib_path(real_file).exists():
            # 文件已存在，重命名文件，同时保留多份文件
            __file_names = os.path.splitext(real_file)
            real_file = f"{__file_names[0]}-{get_now(format_='%Y-%m-%d-%H-%M-%S')}{__file_names[1]}"
        # - - - - - - - - - - - - - 本地缓存写入 - - - - - - - - - - - - -
        try:
            with open(real_file, "wb") as f:
                while content := await file_.read(self.READ_SIZE):
                    f.write(content)
        except Exception as e:
            return FailureStatus(
                code=status_code.CODE_456_REQUEST_FILE_LOCAL_STORE_FAILURE.value,
                message=f"文件本地存储失败：{str(e)}")
        # - - - - - - - - - - - - - 云存储 - - - - - - - - - - - - -
        _store_name: str = f"{get_now(format_='%Y%m%d')}/{file_name}"    # 加入上传日期
        qn_result = await self.qn_store.upload(store_name=_store_name, local_file=real_file)
        if qn_result.get("code") != 100:
            return FailureStatus(
                code=status_code.CODE_457_REQUEST_FILE_YUN_STORE_FAILURE.value,
                message=qn_result.get("message") or "文件云存储上传失败")
        __data: Dict = {
            "name": file_name,
            "local": real_file,
            "url": qn_result.get("data").get("url")
        }
        return SuccessStatus(data=__data)
