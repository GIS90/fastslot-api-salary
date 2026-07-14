# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>xtcs view

base_info:
    __author__ = PyGo
    __time__ = 2026/6/6 22:07
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtcs.py

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
from deploy.service.system.config.xtcs import SystemConfigXtcsService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_like_params, depend_token_rtx
from deploy.schema.po.system_config_xtcs import XtbXtcsAddModel, XtbXtcsUpdateModel
from deploy.schema.po.x import RequestMd5StatusModel, RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/config", tags=["系统配置-参数配置"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemConfigXtcsService:
    return SystemConfigXtcsService(db_connection=db)


@router.get("/xtcs.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_like_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/xtcs", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)

@router.put('/xtcs.status', summary="状态")
async def status(
    params: Annotated[RequestMd5StatusModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.status(token_rtx_id, params=params.model_dump())


@router.post("/xtcs", summary="新增")
async def add(
    params: Annotated[XtbXtcsAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/xtcs", summary="更新")
async def update(
    params: Annotated[XtbXtcsUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/xtcs.delete", summary="单条软删除")
async def delete_(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.delete_(rtx_id=token_rtx_id, md5=md5)


@router.put("/xtcs.batch.delete", summary="批量软删除")
async def batch_delete(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.get("/xtcs.view", summary="视图")
async def view(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigXtcsService = Depends(get_service)
) -> Status:
    return await service.view(rtx_id=token_rtx_id, md5=md5)