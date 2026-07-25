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
from pathlib import Path as pathlib_path
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.utils import get_now, remove_file, get_static_folder


class ApiUploadService:
    """
    ApiUploadService Service
    """
    def __init__(self, db_connection: AsyncSession):
        """
        ApiUploadService class initialize
        """
        self.db: AsyncSession = db_connection
        # 定义文件读取默认大小
        self.READ_SIZE = 1024 * 1024  # 1024 = 1KB

    def __str__(self):
        return "ApiUploadService class."

    def __repr__(self):
        return self.__str__()

    async def upload(self, rtx_id: str, upload_type: str, file_) -> Status:
        if not file_:
            return FailureStatus(code=status_code.CODE_450_REQUEST_FILE_NO_UPLOAD)

        file_name = getattr(file_, 'filename')  # use getattr method to get file name
        if not file_name:
            file_name = get_now()
        real_file = pathlib_path.joinpath(get_static_folder(), file_name)
        if pathlib_path.exists(real_file):
            remove_file(file_=real_file)
        # - - - - - - - - - - - - - write file - - - - - - - - - - - - -
        with open(real_file, "wb") as f:
            while content := await file_.read(self.READ_SIZE):
                f.write(content)
        return SuccessStatus()

    async def uploads(self, rtx_id: str, upload_type: str, files_) -> Status:
        print('*' * 100)
        for f in files_:
            if not f: continue
            print(getattr(f, 'filename'))
            await self.upload(rtx_id=rtx_id, upload_type=upload_type, file_=f)
        return SuccessStatus()