# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    消息通知异步任务状态存储（Redis）

base_info:
    __author__ = PyGo
    __time__ = 2026/11/23 12:00
    __version__ = v.2.0.0
    __project__ = fastslot-api-salary
    __file_name__ = notify_task.py

python version:
    python3

------------------------------------------------
"""
import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from deploy.config import redis_host, redis_db, redis_password, redis_port
from deploy.delib.redis_lib import RedisClientLib
from deploy.utils.logger import logger as LOG


class NotifyTaskStatus:
    PENDING: str = "PENDING"
    RUNNING: str = "RUNNING"
    SUCCESS: str = "SUCCESS"
    FAILURE: str = "FAILURE"


_TASK_KEY_PREFIX: str = "salary:notify:task:"
_TASK_EXPIRE_SECONDS: int = 12 * 60 * 60

_redis_cli: RedisClientLib = RedisClientLib(
    host=redis_host,
    port=redis_port,
    db=redis_db,
    password=redis_password
)

# Redis不可用时的临时兜底，避免任务接口直接500
_memory_fallback: Dict[str, Dict[str, Any]] = {}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _task_key(task_id: str) -> str:
    return f"{_TASK_KEY_PREFIX}{task_id}"


def _set_task_sync(task: Dict[str, Any]) -> None:
    task_id: str = str(task.get("taskId") or "")
    if not task_id:
        return
    try:
        _redis_cli.set_key(
            key=_task_key(task_id),
            value=json.dumps(task, ensure_ascii=False),
            ex=_TASK_EXPIRE_SECONDS
        )
    except Exception as e:
        LOG.error(f"[NotifyTask]Redis写入失败，使用内存兜底：{e}")
        _memory_fallback[task_id] = task


def _get_task_sync(task_id: str) -> Optional[Dict[str, Any]]:
    try:
        raw = _redis_cli.get_key(key=_task_key(task_id))
        if raw:
            task = json.loads(raw)
            return dict(task) if isinstance(task, dict) else None
    except Exception as e:
        LOG.error(f"[NotifyTask]Redis读取失败，使用内存兜底：{e}")
    task = _memory_fallback.get(task_id)
    return dict(task) if task else None


def _delete_task_sync(task_id: str) -> None:
    try:
        _redis_cli.delete_key(_task_key(task_id))
    except Exception as e:
        LOG.error(f"[NotifyTask]Redis删除失败：{e}")
    _memory_fallback.pop(task_id, None)


def _clear_tasks_sync() -> List[str]:
    task_ids: List[str] = []
    try:
        keys: List[str] = _redis_cli.keys(pattern=f"{_TASK_KEY_PREFIX}*") or []
        task_ids = [str(key).replace(_TASK_KEY_PREFIX, "", 1) for key in keys]
        if keys:
            _redis_cli.delete_key(*keys)
    except Exception as e:
        LOG.error(f"[NotifyTask]Redis清空失败：{e}")
    task_ids.extend(_memory_fallback.keys())
    _memory_fallback.clear()
    return list(dict.fromkeys(task_ids))


async def _to_thread(func, *args, **kwargs) -> Any:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def create_task(channel: str, action: str, md5: str, owner: str = "") -> str:
    """创建任务并返回任务ID"""
    task_id: str = uuid.uuid4().hex
    now: str = _now()
    task: Dict[str, Any] = {
        "taskId": task_id,
        "channel": channel,
        "action": action,
        "md5": md5,
        "owner": owner,
        "status": NotifyTaskStatus.PENDING,
        "message": "任务已提交，正在等待处理",
        "code": 100,
        "result": [],
        "createdAt": now,
        "updatedAt": now
    }
    await _to_thread(_set_task_sync, task)
    return task_id


async def set_running(task_id: str) -> None:
    task = await get_task(task_id)
    if not task:
        return
    task["status"] = NotifyTaskStatus.RUNNING
    task["message"] = "任务处理中"
    task["updatedAt"] = _now()
    await _to_thread(_set_task_sync, task)


async def set_success(task_id: str, result: Any, message: str = "处理完成") -> None:
    task = await get_task(task_id)
    if not task:
        return
    task["status"] = NotifyTaskStatus.SUCCESS
    task["code"] = 100
    task["message"] = message
    task["result"] = result if isinstance(result, (list, dict)) else []
    task["updatedAt"] = _now()
    await _to_thread(_set_task_sync, task)


async def set_failure(task_id: str, message: str, code: int = 900) -> None:
    task = await get_task(task_id)
    if not task:
        return
    task["status"] = NotifyTaskStatus.FAILURE
    task["code"] = code
    task["message"] = message or "任务处理失败"
    task["result"] = []
    task["updatedAt"] = _now()
    await _to_thread(_set_task_sync, task)


async def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    return await _to_thread(_get_task_sync, task_id)


async def clear_tasks() -> List[str]:
    """清空任务记录"""
    return await _to_thread(_clear_tasks_sync)
