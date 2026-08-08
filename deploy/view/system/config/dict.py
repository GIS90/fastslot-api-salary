# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>dict view

base_info:
    __author__ = PyGo
    __time__ = 2026/7/19 15:54
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = dict.py

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
from deploy.service.system.config.dict import SystemConfigDictService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_query_params, depend_token_rtx
from deploy.schema.po.system_config_dict import (CsbEnumKeyAddModel, CsbEnumKeyUpdateModel,
                                                 CsbEnumValueAddModel, CsbEnumValueUpdateModel)
from deploy.schema.po.x import RequestMd5StatusModel, RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/config", tags=["系统->系统配置->数据字典"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemConfigDictService:
    return SystemConfigDictService(db_connection=db)


@router.get("/dict/dk.list", summary="DK>数据列表")
async def dk_pagination(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.dk_pagination(rtx_id=token_rtx_id)


@router.delete("/dict/dk.delete", summary="DK>单条软删除")
async def dk_delete(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.dk_delete(rtx_id=token_rtx_id, md5=md5)


@router.put('/dict/dk.status', summary="DK>锁定/解锁")
async def dk_status(
    params: Annotated[RequestMd5StatusModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.dk_status(token_rtx_id, params=params.model_dump())


@router.post("/dict/dk", summary="DK>新增")
async def dk_add(
    params: Annotated[CsbEnumKeyAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.dk_add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/dict/dk", summary="DK>更新")
async def dk_update(
    params: Annotated[CsbEnumKeyUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.dk_update(rtx_id=token_rtx_id, model=params.model_dump())


@router.get('/dict/dk', summary="DK>通过Md5-Id获取单条数据")
async def dk_one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.dk_one_by_md5(token_rtx_id, md5)


@router.get("/dict/de.list", summary="DE>数据列表")
async def de_pagination(
    params: dict = Depends(pageable_query_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_pagination(rtx_id=token_rtx_id, params=params)


@router.delete("/dict/de.delete", summary="DE>单条软删除")
async def de_delete(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_delete(rtx_id=token_rtx_id, md5=md5)


@router.put("/dict/de.batch.delete", summary="批量软删除")
async def de_batch_delete(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put('/dict/de.status', summary="DE>锁定/解锁")
async def de_status(
    params: Annotated[RequestMd5StatusModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_status(token_rtx_id, params=params.model_dump())


@router.get("/dict/de.addInit", summary="DE>新增初始化")
async def de_add_init(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_add_init(rtx_id=token_rtx_id)


@router.post("/dict/de", summary="DE>新增")
async def de_add(
    params: Annotated[CsbEnumValueAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/dict/de", summary="DE>更新")
async def de_update(
    params: Annotated[CsbEnumValueUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_update(rtx_id=token_rtx_id, model=params.model_dump())


@router.get('/dict/de', summary="DE>通过Md5-Id获取单条数据")
async def de_one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemConfigDictService = Depends(get_service)
) -> Status:
    return await service.de_one_by_md5(token_rtx_id, md5)
