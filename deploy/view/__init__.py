# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    MVS：view layer

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:44
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = __init__.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from deploy.view.root import router as root_router
from deploy.view.access import router as access_router
from deploy.view.api import router as api_router
from deploy.view.upload import router as upload_router

from deploy.view.system.xtb_user import router as xtb_user_router
from deploy.view.system.xtb_role import router as xtb_role_router


"""
View根据系统设计的api进行模块划分，其中有3个比较特殊（不为系统模块设计API）
- root：路径为/，系统首页
- access：JWT Token系统验证 [不走token验证]
- api：为对外开发的API集合 [不走token验证]
- upload：文件上传模块 [File UploadFile]

功能模块
  系统管理
    - xtb_user：用户管理
    - xtb_role：角色管理
"""
__all__ = ["add_routers"]


add_routers = [
    root_router,
    access_router,
    api_router,
    upload_router,
    xtb_user_router,
    xtb_role_router,
]
