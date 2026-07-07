# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>menu view

base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:06
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = menu.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.system.main.menu import SystemMainMenuService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_params, depend_token_rtx
from deploy.schema.po.system_main_menu import XtbMenuBaseModel, XtbMenuUpdateModel


# router
router: APIRouter = APIRouter(prefix="/system/main", tags=["系统管理-菜单管理"])
# service
def get_menu_service(db: AsyncSession = Depends(get_session)) -> SystemMainMenuService:
    return SystemMainMenuService(db_connection=db)


@router.get("/menu.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    menu_service: SystemMainMenuService = Depends(get_menu_service)
) -> Status:
    return await menu_service.pagination(rtx_id=token_rtx_id, params=params)

@router.delete("/menu.delete", summary="软删除")
async def delete_soft(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    menu_service: SystemMainMenuService = Depends(get_menu_service)
) -> Status:
    return await menu_service.delete_soft(rtx_id=token_rtx_id, md5=md5)


@router.delete('/menu.status', summary="启用/注销")
async def status(
    md5: str = Query(..., description="数据Md5-Id"),
    value: bool = Query(..., description="状态"),
    token_rtx_id: str = Depends(depend_token_rtx),
    menu_service: SystemMainMenuService = Depends(get_menu_service)
) -> Status:
    return await menu_service.status(token_rtx_id, md5, value)


@router.get("/menu", summary="通过Md5-Id获取单条数据")
async def one_by_md5(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    menu_service: SystemMainMenuService = Depends(get_menu_service)
) -> Status:
    return await menu_service.one_by_md5(rtx_id=token_rtx_id, md5=md5)


@router.put("/menu", summary="更新")
async def update(
    params: Annotated[XtbMenuUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    menu_service: SystemMainMenuService = Depends(get_menu_service)
) -> Status:
    return await menu_service.update(rtx_id=token_rtx_id, model=params.model_dump())



#
# @router.post("", summary="新增")
# async def add(
#     params: Annotated[XtbRoleAddModel, Body()],
#     token_rtx_id: str = Depends(depend_token_rtx),
#     xtb_role_service: XtbRoleService = Depends(get_xtb_role_service)
# ) -> Status:
#     return await xtb_role_service.add(rtx_id=token_rtx_id, model=params.model_dump())
#
#

#
#
# @router.delete("/hard", summary="硬删除")
# async def delete_hard(
#     md5: str = Query(..., description="数据Md5-Id"),
#     token_rtx_id: str = Depends(depend_token_rtx),
#     xtb_role_service: XtbRoleService = Depends(get_xtb_role_service)
# ) -> Status:
#     return await xtb_role_service.delete_hard(rtx_id=token_rtx_id, md5=md5)
#
#


#
# @router.delete("/batch/hard", summary="批量硬删除")
# async def batch_delete_hard(
#     md5_list: List = Query(..., description="数据Md5-Id列表"),
#     token_rtx_id: str = Depends(depend_token_rtx),
#     xtb_role_service: XtbRoleService = Depends(get_xtb_role_service)
# ) -> Status:
#     return await xtb_role_service.batch_delete_hard(rtx_id=token_rtx_id, md5_list=md5_list)
#
#
# @router.delete("/batch/soft", summary="批量软删除")
# async def batch_delete_soft(
#     md5_list: List = Query(..., description="数据Md5-Id列表"),
#     token_rtx_id: str = Depends(depend_token_rtx),
#     xtb_role_service: XtbRoleService = Depends(get_xtb_role_service)
# ) -> Status:
#     return await xtb_role_service.batch_delete_soft(rtx_id=token_rtx_id, md5_list=md5_list)
#
