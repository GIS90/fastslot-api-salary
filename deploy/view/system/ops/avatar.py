# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    view of system ops avatar

base_info:
    __author__ = PyGo
    __time__ = 2026/11/06 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = avatar.py

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
from deploy.service.system.ops.avatar import SystemOpsAvatarService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_like_params, depend_token_rtx
from deploy.schema.po.system_ops_avatar import XtbAvatarAddModel, XtbAvatarUpdateModel
from deploy.schema.po.x import RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/ops", tags=["系统->系统维护->头像管理"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemOpsAvatarService:
    return SystemOpsAvatarService(db_connection=db)


@router.get("/avatar.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_like_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/avatar", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.post("/avatar", summary="新增")
async def add(
    params: Annotated[XtbAvatarAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/avatar", summary="更新")
async def update(
    params: Annotated[XtbAvatarUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/avatar.hard", summary="单条硬删除")
async def delete_hard(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.delete_hard(rtx_id=token_rtx_id, md5=md5)


@router.delete("/avatar.soft", summary="单条软删除")
async def delete_soft(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.delete_soft(rtx_id=token_rtx_id, md5=md5)


@router.put("/avatar.batch.hard", summary="批量硬删除")
async def batch_delete_hard(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.batch_delete_hard(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put("/avatar.batch.soft", summary="批量软删除")
async def batch_delete_soft(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsAvatarService = Depends(get_service)
) -> Status:
    return await service.batch_delete_soft(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))
