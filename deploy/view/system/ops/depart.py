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
from deploy.schema.po.x import PageFilterModel, RequestMd5Models


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




# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#
#
# @ops.post('/depart', summary="[DEPART]新增")
# async def depart_add(
#         data: DepartBaseModel,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.depart_add(token_rtx_id, data.model_dump())
#
#
# @ops.delete('/depart/delete', summary="[DEPART]单条删除")
# async def depart_delete(
#         md5: str = Query(..., min_length=1, max_length=289, description="数据MD5"),
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.depart_delete(token_rtx_id, md5)
#
#
# @ops.put('/depart/delete', summary="[DEPART]批量删除")
# async def departs_delete(
#         params: RequestMd5Models,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.departs_delete(token_rtx_id, params.model_dump().get("md5"))
#
#
# @ops.get('/depart', summary="[DEPART]详情")
# async def depart_detail(
#         md5: str = Query(..., min_length=1, max_length=289, description="数据MD5"),
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.depart_detail(token_rtx_id, md5)
#
#
# @ops.put('/depart', summary="[DEPART]更新")
# async def depart_update(
#         data: DepartUpdateModel,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.depart_update(token_rtx_id, data.model_dump())
#
#
# @ops.put('/depart/drag', summary="[DEPART]节点调整架构")
# async def depart_drag(
#         data: DepartDragModel,
#         token_rtx_id: str = Depends(depend_token_rtx)
# ) -> Status:
#     return await ops_service.depart_drag(token_rtx_id, data.model_dump())
