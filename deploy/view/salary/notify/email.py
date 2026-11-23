# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    salary>notify>email view

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = email.py

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
from fastapi import APIRouter, Depends, Body, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.salary.notify.email import SalaryNotifyEmailService
from deploy.service.salary.notify.task_runner import run_notify_task
from deploy.utils.notify_task import NotifyTaskStatus, create_task, get_task
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.depend import pageable_params, depend_token_rtx, md5_params
from deploy.schema.po.salary_notify_email import (
    SalaryEmailUpdateModel,
    SalaryEmailRobotAddModel,
    SalaryEmailRobotUpdateModel,
    SalaryEmailRobotSelectModel,
    SalaryEmailSendModel,
    SalaryEmailResendModel
)
from deploy.schema.po.x import RequestMd5Models


# router
router: APIRouter = APIRouter(prefix="/salary/notify", tags=["工资->消息通知->邮件通知"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> SalaryNotifyEmailService:
    return SalaryNotifyEmailService(db_connection=db)


# - - - - - - - - - - - - - - - - - - - - 消息文件 - - - - - - - - - - - - - - - - - - - -
@router.get("/email.list", summary="数据列表")
async def pagination(
    params: Dict = Depends(pageable_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/email", summary="通过Md5-Id获取单条数据")
async def one(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.detail(rtx_id=token_rtx_id, md5=md5)


@router.put("/email", summary="更新设置")
async def update(
    params: Annotated[SalaryEmailUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.update(rtx_id=token_rtx_id, params=params.model_dump())


@router.get("/email.changeSheet", summary="切换Sheet")
async def change_sheet(
    md5: str = Depends(md5_params),
    sheet: str = Query(..., min_length=1, max_length=4, description="Sheet索引"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.change_sheet(rtx_id=token_rtx_id, md5=md5, sheet=sheet)


@router.delete("/email.soft", summary="单条软删除")
async def delete(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.delete(rtx_id=token_rtx_id, md5=md5)


@router.put("/email.batch.soft", summary="批量软删除")
async def delete_batch(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.delete_batch(
        rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.get("/email.sendInit", summary="发送初始化")
async def send_init(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.send_init(rtx_id=token_rtx_id, md5=md5)


@router.post("/email.send", summary="提交邮件发送消息任务")
async def send(
    params: Annotated[SalaryEmailSendModel, Body()],
    background_tasks: BackgroundTasks,
    token_rtx_id: str = Depends(depend_token_rtx)
) -> Status:
    payload: Dict = params.model_dump()
    task_id: str = await create_task(
        channel="email", action="send", md5=payload.get("md5") or "", owner=token_rtx_id)
    background_tasks.add_task(run_notify_task, task_id, "email", "send", token_rtx_id, payload)
    return SuccessStatus(data={"taskId": task_id, "status": NotifyTaskStatus.PENDING})


@router.get("/email.task", summary="查询邮件发送/重发任务状态")
async def notify_task(
    task_id: str = Query(..., alias="taskId", min_length=32, max_length=32, description="异步任务ID"),
    token_rtx_id: str = Depends(depend_token_rtx)
) -> Status:
    task = await get_task(task_id)
    if not task or (task.get("owner") and task.get("owner") != token_rtx_id):
        return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST.value, message="任务不存在或已过期")
    return SuccessStatus(data=task)


@router.get("/email.resendInit", summary="重发失败人员初始化")
async def resend_init(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.resend_init(rtx_id=token_rtx_id, md5=md5)


@router.post("/email.resend", summary="提交邮件失败人员重发任务")
async def resend(
    params: Annotated[SalaryEmailResendModel, Body()],
    background_tasks: BackgroundTasks,
    token_rtx_id: str = Depends(depend_token_rtx)
) -> Status:
    payload: Dict = params.model_dump()
    task_id: str = await create_task(
        channel="email", action="resend", md5=payload.get("md5") or "", owner=token_rtx_id)
    background_tasks.add_task(run_notify_task, task_id, "email", "resend", token_rtx_id, payload)
    return SuccessStatus(data={"taskId": task_id, "status": NotifyTaskStatus.PENDING})


# - - - - - - - - - - - - - - - - - - - - 邮件服务配置 - - - - - - - - - - - - - - - - - - - -
@router.get("/email/robot.list", summary="邮件服务列表")
async def robot_list(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_list(rtx_id=token_rtx_id)


@router.post("/email/robot", summary="新增邮件服务")
async def robot_add(
    params: Annotated[SalaryEmailRobotAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_add(rtx_id=token_rtx_id, params=params.model_dump())


@router.get("/email/robot", summary="邮件服务详情")
async def robot_detail(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_detail(rtx_id=token_rtx_id, md5=md5)


@router.put("/email/robot", summary="更新邮件服务")
async def robot_update(
    params: Annotated[SalaryEmailRobotUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_update(rtx_id=token_rtx_id, params=params.model_dump())


@router.delete("/email/robot.soft", summary="单条删除邮件服务")
async def robot_delete(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_delete(rtx_id=token_rtx_id, md5=md5)


@router.put("/email/robot.batch.soft", summary="批量删除邮件服务")
async def robot_delete_batch(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_delete_batch(
        rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.put("/email/robot.select", summary="设置默认邮件服务")
async def robot_select(
    params: Annotated[SalaryEmailRobotSelectModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_select(
        rtx_id=token_rtx_id, md5=params.md5, select=params.select)


@router.get("/email/robot.ping", summary="邮件服务连通性测试")
async def robot_ping(
    md5: str = Depends(md5_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SalaryNotifyEmailService = Depends(get_service)
) -> Status:
    return await service.robot_ping(rtx_id=token_rtx_id, md5=md5)
