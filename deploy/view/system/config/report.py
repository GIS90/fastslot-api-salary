# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>report view

base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = report.py

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
from deploy.service.system.config.report import SystemConfigReportService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_like_params, depend_token_rtx
from deploy.schema.po.system_config_report import (
    XtbXtbbAddModel, XtbXtbbUpdateModel,
    XtbXtbbFieldAddModel, XtbXtbbFieldUpdateModel
)
from deploy.schema.po.x import RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/config", tags=["系统->系统配置->报表配置"])


def get_service(db: AsyncSession = Depends(get_session)) -> SystemConfigReportService:
    return SystemConfigReportService(db_connection=db)


@router.get("/report.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_like_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/report", summary="通过Md5-Id获取单条数据")
async def one_by_md5(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.post("/report", summary="新增")
async def add(
    params: Annotated[XtbXtbbAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/report", summary="更新")
async def update(
    params: Annotated[XtbXtbbUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/report.delete", summary="单条软删除")
async def delete_(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.delete_(rtx_id=token_rtx_id, md5=md5)


@router.put("/report.batch.delete", summary="批量软删除")
async def batch_delete(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.get("/report.view", summary="视图")
async def view(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.view(rtx_id=token_rtx_id, md5=md5)


# ======================== report field ========================

@router.get("/report.field.list", summary="字段列表-按报表Md5")
async def field_list_by_xtbb_md5(
    xtbbMd5: str = Query(..., description="报表Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.field_list_by_xtbb_md5(rtx_id=token_rtx_id, xtbb_md5=xtbbMd5)


@router.post("/report.field", summary="新增字段")
async def field_add(
    params: Annotated[XtbXtbbFieldAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.field_add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/report.field", summary="更新字段")
async def field_update(
    params: Annotated[XtbXtbbFieldUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.field_update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/report.field.delete", summary="单条删除字段")
async def field_delete_(
    md5: str = Query(..., description="字段Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.field_delete_(rtx_id=token_rtx_id, md5=md5)


@router.put("/report.field.batch.delete", summary="批量删除字段")
async def field_batch_delete(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigReportService = Depends(get_service)
) -> Status:
    return await service.field_batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))
