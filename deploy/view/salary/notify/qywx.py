# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    salary>notify>qywx view

base_info:
    __author__ = PyGo
    __time__ = 2026/11/19 10:00
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = qywx.py

python version:
    python3

------------------------------------------------
"""
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.salary.notify.qywx import SalaryNotifyQywxService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_params, depend_token_rtx, md5_params
from deploy.schema.po.salary_notify_qywx import (
    SalaryQywxUpdateModel,
    SalaryQywxRobotAddModel,
    SalaryQywxRobotUpdateModel,
    SalaryQywxRobotSelectModel,
    SalaryQywxSendModel
)
from deploy.schema.po.x import RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/salary/notify", tags=["工资->消息通知->企业微信通知"])


def get_service(db: AsyncSession = Depends(get_session)) -> SalaryNotifyQywxService:
    return SalaryNotifyQywxService(db_connection=db)


# - - - - - - - - - - - - - - - - - - - - 消息文件 - - - - - - - - - - - - - - - - - - - -
@router.get("/qywx.list", summary="数据列表")
async def pagination(
    params: Dict = Depends(pageable_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/qywx", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.detail(rtx_id=token_rtx_id, md5=md5)


@router.put("/qywx", summary="更新设置")
async def update(
    params: Annotated[SalaryQywxUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, params=params.model_dump())


@router.get("/qywx.changeSheet", summary="切换Sheet")
async def change_sheet(
    md5: str = Depends(md5_params),
    sheet: str = Query(..., min_length=1, max_length=4, description="Sheet索引"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.change_sheet(rtx_id=token_rtx_id, md5=md5, sheet=sheet)


@router.delete("/qywx.soft", summary="单条软删除")
async def delete(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.delete(rtx_id=token_rtx_id, md5=md5)


@router.put("/qywx.batch.soft", summary="批量软删除")
async def delete_batch(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.delete_batch(
        rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.get("/qywx.sendInit", summary="发送初始化")
async def send_init(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.send_init(rtx_id=token_rtx_id, md5=md5)


@router.post("/qywx.send", summary="发送企业微信消息")
async def send(
    params: Annotated[SalaryQywxSendModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.send(rtx_id=token_rtx_id, params=params.model_dump())


# - - - - - - - - - - - - - - - - - - - - 机器人配置 - - - - - - - - - - - - - - - - - - - -
@router.get("/qywx/robot.list", summary="机器人列表")
async def robot_list(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_list(rtx_id=token_rtx_id)


@router.post("/qywx/robot", summary="新增机器人")
async def robot_add(
    params: Annotated[SalaryQywxRobotAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_add(rtx_id=token_rtx_id, params=params.model_dump())


@router.get("/qywx/robot", summary="机器人详情")
async def robot_detail(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_detail(rtx_id=token_rtx_id, md5=md5)


@router.put("/qywx/robot", summary="更新机器人")
async def robot_update(
    params: Annotated[SalaryQywxRobotUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_update(rtx_id=token_rtx_id, params=params.model_dump())


@router.delete("/qywx/robot.soft", summary="单条删除机器人")
async def robot_delete(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_delete(rtx_id=token_rtx_id, md5=md5)


@router.put("/qywx/robot.batch.soft", summary="批量删除机器人")
async def robot_delete_batch(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_delete_batch(
        rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put("/qywx/robot.select", summary="设置默认机器人")
async def robot_select(
    params: Annotated[SalaryQywxRobotSelectModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_select(
        rtx_id=token_rtx_id, md5=params.md5, select=params.select)


@router.get("/qywx/robot.ping", summary="机器人连通性测试")
async def robot_ping(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyQywxService = Depends(get_service)
) -> Status:
    return await service.robot_ping(rtx_id=token_rtx_id, md5=md5)
