# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    消息通知异步任务执行器

base_info:
    __author__ = PyGo
    __time__ = 2026/11/23 10:00
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = task_runner.py

python version:
    python3

------------------------------------------------
"""
from typing import Any, Dict
from deploy.curd.database import AsyncSessionLocal
from deploy.service.salary.notify.dtalk import SalaryNotifyDtalkService
from deploy.service.salary.notify.email import SalaryNotifyEmailService
from deploy.service.salary.notify.qywx import SalaryNotifyQywxService
from deploy.utils.logger import logger as LOG
from deploy.utils.notify_task import set_failure, set_running, set_success


async def run_notify_task(
    task_id: str,
    channel: str,
    action: str,
    rtx_id: str,
    params: Dict
) -> None:
    """在后台执行发送/重发任务，并写回任务状态"""
    await set_running(task_id)
    try:
        async with AsyncSessionLocal() as session:
            try:
                if channel == "qywx":
                    service: SalaryNotifyDtalkService = SalaryNotifyDtalkService(db_connection=session)
                elif channel == "dtalk":
                    service: SalaryNotifyQywxService = SalaryNotifyQywxService(db_connection=session)
                elif channel == "email":
                    service: SalaryNotifyEmailService = SalaryNotifyEmailService(db_connection=session)
                else:
                    raise ValueError(f"不支持的通知渠道：{channel}")

                handler = getattr(service, action, None)
                if not handler:
                    raise ValueError(f"不支持的通知操作：{action}")

                status = await handler(rtx_id=rtx_id, params=params)
                body: Dict = status.dict()
                await session.commit()
            except Exception:
                await session.rollback()
                raise

        code: int = int(body.get("code") or 0)
        if code in (100, 101):
            await set_success(
                task_id=task_id,
                result=body.get("data") or [],
                message=body.get("message") or "处理完成"
            )
        else:
            await set_failure(
                task_id=task_id,
                message=body.get("message") or "处理失败",
                code=code or 900
            )
    except Exception as e:
        LOG.error(f"[NotifyTask]任务执行异常：task_id={task_id}, channel={channel}, action={action}, error={e}")
        await set_failure(task_id=task_id, message=f"任务执行失败：{e}", code=900)
