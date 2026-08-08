# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>ops>task view

base_info:
    __author__ = PyGo
    __time__ = 2026/7/12 15:06
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = task.py

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
from deploy.service.system.ops.task import SystemOpsTaskService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx
from deploy.schema.po.x import PageFilterModel, RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/ops", tags=["系统->系统维护->任务中心"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemOpsTaskService:
    return SystemOpsTaskService(db_connection=db)


@router.post("/task.list", summary="数据列表")
async def pagination(
    params: Annotated[PageFilterModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsTaskService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params.model_dump(), _all=True)


@router.get("/task.filter", summary="过滤条件")
async def filter_(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsTaskService = Depends(get_service)
) -> Status:
    return await service.filter_(rtx_id=token_rtx_id)


@router.get("/task", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsTaskService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.delete("/task.delete", summary="单条软删除")
async def delete_(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsTaskService = Depends(get_service)
) -> Status:
    return await service.delete_(rtx_id=token_rtx_id, md5=md5)


@router.put("/task.batch.delete", summary="批量软删除")
async def batch_delete(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsTaskService = Depends(get_service)
) -> Status:
    return await service.batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))
