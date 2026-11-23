# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    消息通知异步任务状态存储

base_info:
    __author__ = PyGo
    __time__ = 2026/11/23 10:00
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = notify_task.py

python version:
    python3

------------------------------------------------
"""
import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


class NotifyTaskStatus:
    PENDING: str = "PENDING"
    RUNNING: str = "RUNNING"
    SUCCESS: str = "SUCCESS"
    FAILURE: str = "FAILURE"


_task_store: Dict[str, Dict[str, Any]] = {}
_task_lock: asyncio.Lock = asyncio.Lock()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


async def create_task(channel: str, action: str, md5: str, owner: str = "") -> str:
    """创建任务并返回任务ID"""
    task_id: str = uuid.uuid4().hex
    async with _task_lock:
        _task_store[task_id] = {
            "taskId": task_id,
            "channel": channel,
            "action": action,
            "md5": md5,
            "owner": owner,
            "status": NotifyTaskStatus.PENDING,
            "message": "任务已提交，正在等待处理",
            "code": 100,
            "result": [],
            "createdAt": _now(),
            "updatedAt": _now()
        }
    return task_id


async def set_running(task_id: str) -> None:
    async with _task_lock:
        task = _task_store.get(task_id)
        if task:
            task["status"] = NotifyTaskStatus.RUNNING
            task["message"] = "任务处理中"
            task["updatedAt"] = _now()


async def set_success(task_id: str, result: Any, message: str = "处理完成") -> None:
    async with _task_lock:
        task = _task_store.get(task_id)
        if task:
            task["status"] = NotifyTaskStatus.SUCCESS
            task["code"] = 100
            task["message"] = message
            task["result"] = result if isinstance(result, (list, dict)) else []
            task["updatedAt"] = _now()


async def set_failure(task_id: str, message: str, code: int = 900) -> None:
    async with _task_lock:
        task = _task_store.get(task_id)
        if task:
            task["status"] = NotifyTaskStatus.FAILURE
            task["code"] = code
            task["message"] = message or "任务处理失败"
            task["result"] = []
            task["updatedAt"] = _now()


async def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    async with _task_lock:
        task = _task_store.get(task_id)
        return dict(task) if task else None


async def clear_tasks() -> List[str]:
    """清空任务记录，便于测试或重启后手动清理"""
    async with _task_lock:
        task_ids = list(_task_store.keys())
        _task_store.clear()
        return task_ids
