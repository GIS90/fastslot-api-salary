# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>menu view

base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:06
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = menu.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.system.main.menu import SystemMainMenuService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_params, depend_token_rtx
from deploy.schema.po.system_main_menu import XtbMenuBaseModel, XtbMenuUpdateModel


# router
router: APIRouter = APIRouter(prefix="/system/main", tags=["系统管理-菜单管理"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemMainMenuService:
    return SystemMainMenuService(db_connection=db)


@router.get("/menu.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.delete("/menu.delete", summary="单条软删除")
async def delete_soft(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.delete(rtx_id=token_rtx_id, md5=md5)


@router.delete('/menu.status', summary="启用/注销")
async def status(
    md5: str = Query(..., description="数据Md5-Id"),
    value: bool = Query(..., description="状态"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.status(token_rtx_id, md5, value)


@router.get("/menu", summary="通过Md5-Id获取单条数据")
async def one_by_md5(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.put("/menu", summary="更新")
async def update(
    params: Annotated[XtbMenuUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, model=params.model_dump())


@router.get("/menu.addEnum", summary="新增枚举")
async def add(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.add_enum(rtx_id=token_rtx_id)


@router.post("/menu", summary="新增")
async def add(
    params: Annotated[XtbMenuBaseModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainMenuService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, model=params.model_dump())