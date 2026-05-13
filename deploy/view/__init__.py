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
from deploy.view.x import router as x_router
from deploy.view.api import router as api_router
from deploy.view.upload import router as upload_router

from deploy.view.system.main.user import router as system_main_user_router
from deploy.view.system.main.role import router as system_mian_role_router


"""
View根据系统设计的api进行模块划分，其中有3个比较特殊（不为系统模块设计API）
- root：路径为/，系统首页
- access：系统登录、退出API，采用JWT Token系统验证 [不走token验证]
- x：系统正常运行的API集合
- api：对外开发的API集合 [不走token验证]
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
    x_router,
    api_router,
    upload_router,
    system_main_user_router,
    system_mian_role_router,
]
