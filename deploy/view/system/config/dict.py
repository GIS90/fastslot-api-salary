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
from deploy.utils.depend import pageable_like_params, depend_token_rtx
from deploy.schema.po.system_config_dict import CsbEnumKeyAddModel, CsbEnumKeyUpdateModel
from deploy.schema.po.x import RequestMd5StatusModel, RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/system/config", tags=["系统配置-数据字典"])
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






#
# @ops.get('/dict/enum/list', summary="[DICT]Enum.列表")
# async def dict_enum_list(
#         params: dict = Depends(pageable_query_params),
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_list(token_rtx_id, params)
#
#
# @ops.delete('/dict/enum/delete', summary="[DICT]Enum.单条删除")
# async def dict_enum_delete(
#         md5: str = Query(..., min_length=1, max_length=289, description="数据MD5"),
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_delete(token_rtx_id, md5)
#
#
# @ops.put('/dict/enum/delete', summary="[DICT]Enum.批量删除")
# async def dict_enums_delete(
#         params: RequestMd5Models,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enums_delete(token_rtx_id, params.model_dump().get("md5"))
#
#
# @ops.delete('/dict/enum/status', summary="[DICT]Enum.启用/注销")
# async def dict_enum_status(
#         md5: str = Query(..., min_length=1, max_length=289, description="数据MD5"),
#         value: bool = Query(..., description="状态"),
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_status(token_rtx_id, md5, value)
#
#
# @ops.get('/dict/enum/init', summary="[DICT]Enum.新增枚举")
# async def dict_enum_add_init(
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_add_init(token_rtx_id)
#
#
# @ops.post('/dict/enum', summary="[DICT]Enum.新增")
# async def dict_enum_add(
#         data: DictEnumBaseModel,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_add(token_rtx_id, data.model_dump())
#
#
# @ops.get('/dict/enum', summary="[DICT]Enum.详情")
# async def dict_enum_detail(
#         md5: str = Query(..., min_length=1, max_length=289, description="数据MD5"),
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_detail(token_rtx_id, md5)
#
#
# @ops.put('/dict/enum', summary="[DICT]Enum.更新")
# async def dict_enum_update(
#         data: DictEnumUpdateModel,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.dict_enum_update(token_rtx_id, data.model_dump())
