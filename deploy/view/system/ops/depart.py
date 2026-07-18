# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    system>ops>depart view

base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:50
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = depart.py

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
from deploy.service.system.ops.depart import SystemOpsDepartService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx
from deploy.schema.po.x import RequestMd5Models
from deploy.schema.po.system_ops_depart import XtbDepartmentAddModel, XtbDepartmentUpdateModel, XtbDepartmentDragModel


# router
router: APIRouter = APIRouter(prefix="/system/ops", tags=["系统维护-部门架构"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemOpsDepartService:
    return SystemOpsDepartService(db_connection=db)


@router.get("/depart.tree", summary="树结构数据")
async def tree(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.tree(rtx_id=token_rtx_id)


@router.get('/depart.addEnum', summary="新增枚举值")
async def add_enum(
    md5: str = Query(..., min_length=1, max_length=289, description="数据MD5"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.add_enum(token_rtx_id, md5)


@router.post('/depart', summary="新增")
async def add(
    params: Annotated[XtbDepartmentAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.add(rtx_id=token_rtx_id, params=params.model_dump())


@router.get('/depart', summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.one_by_md5(token_rtx_id, md5)


@router.put("/depart", summary="更新")
async def update(
    params: Annotated[XtbDepartmentUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, params=params.model_dump())


@router.delete('/depart.delete', summary="单条软删除")
async def delete_(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.delete_(rtx_id=token_rtx_id, md5=md5)


@router.put('/depart.batch.delete', summary="批量软删除")
async def batch_delete(
    params: RequestMd5Models,
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put('/depart.drag', summary="[DEPART]节点调整架构")
async def drag(
    params: Annotated[XtbDepartmentDragModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsDepartService = Depends(get_service)
) -> Status:
    return await service.drag(rtx_id=token_rtx_id, params=params.model_dump())

