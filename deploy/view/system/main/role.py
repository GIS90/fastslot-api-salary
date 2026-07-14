# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>role view

base_info:
    __author__ = PyGo
    __time__ = 2026/4/2 23:29
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = role.py

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
from deploy.service.system.main.role import SystemMainRoleService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_like_params, depend_token_rtx
from deploy.schema.po.system_main_role import XtbRoleAddModel, XtbRoleUpdateModel, XtbRoleAuthModel
from deploy.schema.po.x import RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/main", tags=["系统管理-角色管理"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemMainRoleService:
    return SystemMainRoleService(db_connection=db)


@router.get("/role.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_like_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/role", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.post("/role", summary="新增")
async def add(
    params: Annotated[XtbRoleAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/role", summary="更新")
async def update(
    params: Annotated[XtbRoleUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/role.hard", summary="单条硬删除")
async def delete_hard(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.delete_hard(rtx_id=token_rtx_id, md5=md5)


@router.delete("/role.soft", summary="单条软删除")
async def delete_soft(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.delete_soft(rtx_id=token_rtx_id, md5=md5)


@router.put("/role.batch.hard", summary="批量硬删除")
async def batch_delete_hard(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.batch_delete_hard(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put("/role.batch.soft", summary="批量软删除")
async def batch_delete_soft(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.batch_delete_soft(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.get("/role.auth", summary="权限菜单")
async def auth(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.auth(rtx_id=token_rtx_id, md5=md5)


@router.put("/role.auth", summary="权限菜单")
async def auth_update(
    params: Annotated[XtbRoleAuthModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainRoleService = Depends(get_service)
) -> Status:
    return await service.auth_update(rtx_id=token_rtx_id, model=params.model_dump())