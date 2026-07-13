# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>user view

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 21:58
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = user.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.system.main.user import SystemMainUserService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_like_params, depend_token_rtx, md5_params, md5_list_params
from deploy.schema.po.system_main_user import XtbUserAddModel, XtbUserUpdateModel
from deploy.schema.po.x import RequestMd5Models, RequestMd5StatusModel


# router
router: APIRouter = APIRouter(prefix="/system/main", tags=["系统管理-用户管理"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemMainUserService:
    return SystemMainUserService(db_connection=db)


@router.get("/user.list", summary="数据列表")
async def pagination(
    params: Dict = Depends(pageable_like_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.put('/user.status', summary="启用/注销")
async def status(
    params: Annotated[RequestMd5StatusModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.status(token_rtx_id, params=params.model_dump())


@router.get('/user.defaultPwd', summary="默认密码")
async def default_pwd(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.default_pwd(rtx_id=token_rtx_id)


@router.put('/user.resetPwd', summary="重置密码")
async def reset_pwd(
    md5: str = Body(..., embed=True),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.reset_pwd(rtx_id=token_rtx_id, md5=md5)


@router.get("/user", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.get("/user.addEnum", summary="新增枚举值")
async def one_by_md5(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.add_enum(rtx_id=token_rtx_id)


@router.post("/user", summary="新增")
async def add(
    params: Annotated[XtbUserAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/user", summary="更新")
async def update(
    params: Annotated[XtbUserUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/user.hard", summary="单条硬删除")
async def delete_hard(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.delete_hard(rtx_id=token_rtx_id, md5=md5)


@router.delete("/user.soft", summary="单条软删除")
async def delete_soft(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.delete_soft(rtx_id=token_rtx_id, md5=md5)


@router.put("/user.batch.hard", summary="批量硬删除")
async def batch_delete_hard(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.batch_delete_hard(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put("/user.batch.soft", summary="批量软删除")
async def batch_delete_soft(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemMainUserService = Depends(get_service)
) -> Status:
    return await service.batch_delete_soft(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))

