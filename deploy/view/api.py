# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    api view

base_info:
    __author__ = PyGo
    __time__ = 2025/11/30 14:35
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = api.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.api.api import ApiOpenService
from deploy.service.api.user import ApiUserService
from deploy.service.api.download import ApiDownloadService
from deploy.service.system.config.xtcs import SystemConfigXtcsService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx
from deploy.utils.decorator import watch_except
from deploy.utils.depend import download_params, pageable_params


# router
router: APIRouter = APIRouter(prefix="/api", tags=["系统正常运行相关APIs集合"])
# service
api_service: ApiOpenService = ApiOpenService()
def get_user_service(db: AsyncSession = Depends(get_session)) -> ApiUserService:
    return ApiUserService(db_connection=db)
def get_download_service(db: AsyncSession = Depends(get_session)) -> ApiDownloadService:
    return ApiDownloadService(db_connection=db)
def get_xtcs_service(db: AsyncSession = Depends(get_session)) -> SystemConfigXtcsService:
    return SystemConfigXtcsService(db_connection=db)


# - - - - - - - - - - - - - - - - - - - - Open Api - - - - - - - - - - - - - - - - - - - -
@router.get('/open/m1.case',
            summary="[M1模块]CASE",
            description="[M1模块]测试用例")
@watch_except
async def m1_case() -> Status:
    """
    [M1模块]CASE
    :return: json
    """
    return await api_service.m1_case()


@router.get('/open/system.info', summary="[系统]基础信息")
@watch_except
async def system_info(
    name: str = Query(..., description="数据KEY"),
    xtcs_service: SystemConfigXtcsService = Depends(get_xtcs_service)
) -> Status:
    return await xtcs_service.system_info_openapi(system_name=name)


# - - - - - - - - - - - - - - - - - - - - 文件下载 - - - - - - - - - - - - - - - - - - - -
@router.get('/download.enum', summary="[下载]枚举")
async def download_enum(
    token_rtx_id: str = Depends(depend_token_rtx),
    download_service: ApiDownloadService = Depends(get_download_service)
) -> Status:
    return await download_service.download_enum(token_rtx_id)


@router.post('/download', summary="[下载]下载")
async def download(
    params: dict = Depends(download_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    download_service: ApiDownloadService = Depends(get_download_service)
) -> Status:
    return await download_service.download(rtx_id=token_rtx_id, params=params)


# - - - - - - - - - - - - - - - - - - - - 用户系统权限 - - - - - - - - - - - - - - - - - - - -
@router.get("/auth", summary="用户菜单权限，用于系统登录后获取用户权限菜单树")
async def auth(
    token_rtx_id: str = Depends(depend_token_rtx),
    user_service: ApiUserService = Depends(get_user_service)
) -> Status:
    return await user_service.auth(token_rtx_id)


@router.get('/dashboard', summary="[USER]用户Dashboard")
async def dashboard(
    token_rtx_id: str = Depends(depend_token_rtx),
    user_service: ApiUserService = Depends(get_user_service)
) -> Status:
    return await user_service.dashboard(token_rtx_id)


@router.get('/task', summary="[USER]用户Task列表")
async def task(
    params: dict = Depends(pageable_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    user_service: ApiUserService = Depends(get_user_service)
) -> Status:
    return await user_service.task(rtx_id=token_rtx_id, params=params)
