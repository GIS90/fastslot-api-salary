# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    system>ops>redis view

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = redis.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！！
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.system.ops.redis import SystemOpsRedisService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx, pageable_filter_params
from deploy.schema.po.x import (
    RequestMd5Model, RequestMd5Models, RequestMd5StatusModel
)
from deploy.schema.po.system_ops_redis import (
    XtbRedisConfigAddModel, XtbRedisConfigUpdateModel,
    XtbRedisRuleAddModel, XtbRedisRuleUpdateModel,
)


# router
router: APIRouter = APIRouter(prefix="/system/ops", tags=["系统->系统维护->Redis缓存管理"])


# service
def get_service(db: AsyncSession = Depends(get_session)) -> SystemOpsRedisService:
    return SystemOpsRedisService(db_connection=db)


# ======================== Redis配置 ========================

@router.get("/redis.config.list", summary="Redis连接配置列表")
async def config_list(
    content: Optional[str] = Query(default=None, description="配置名称/主机模糊查询"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_list(content=content)


@router.get("/redis.config.options", summary="Redis连接配置下拉选项")
async def config_options(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_options()


@router.get("/redis.config", summary="Redis连接配置详情")
async def config_one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_one(md5=md5)


@router.post("/redis.config", summary="新增Redis连接配置")
async def config_add(
    params: Annotated[XtbRedisConfigAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/redis.config", summary="更新Redis连接配置")
async def config_update(
    params: Annotated[XtbRedisConfigUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_update(rtx_id=token_rtx_id, model=params.model_dump())


@router.delete("/redis.config.delete", summary="删除Redis连接配置")
async def config_delete(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_delete(rtx_id=token_rtx_id, md5=md5)


@router.post("/redis.config.test", summary="测试Redis连接")
async def config_test(
    params: Annotated[XtbRedisConfigAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.config_test(model=params.model_dump())


@router.get("/redis.ping", summary="Redis PING连通性检测")
async def ping(
    md5: Optional[str] = Query(default=None, description="指定配置Md5-Id，为空则检测全部启用的配置"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.ping(md5=md5)


@router.get("/redis.keys", summary="浏览Redis键和值（只读）")
async def keys_browser(
    md5: str = Query(..., description="Redis配置Md5-Id"),
    pattern: Optional[str] = Query(default="*", description="key筛选，支持*和?通配符"),
    limit: int = Query(default=200, ge=1, le=10000, description="最多返回key数量"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.keys_browser(md5=md5, pattern=pattern, limit=limit)


# ======================== 清理规则 ========================

@router.get("/redis.rule.filter", summary="规则过滤条件")
async def filter_(
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.filter_()


@router.post("/redis.rule.list", summary="规则数据列表")
async def pagination(
    params: dict = Depends(pageable_filter_params),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)


@router.get("/redis.rule", summary="规则详情")
async def rule_one(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.rule_one(md5=md5)


@router.post("/redis.rule", summary="新增清理规则")
async def rule_add(
    params: Annotated[XtbRedisRuleAddModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.rule_add(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/redis.rule", summary="更新清理规则")
async def rule_update(
    params: Annotated[XtbRedisRuleUpdateModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.rule_update(rtx_id=token_rtx_id, model=params.model_dump())


@router.put("/redis.rule.lock", summary="启用/停用清理规则")
async def rule_lock(
    params: Annotated[RequestMd5StatusModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.rule_lock(rtx_id=token_rtx_id, params=params.model_dump())


@router.delete("/redis.rule.delete", summary="删除清理规则")
async def rule_delete(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.rule_delete(rtx_id=token_rtx_id, md5=md5)


@router.put("/redis.rule.batch.delete", summary="批量删除清理规则")
async def rule_batch_delete(
    params: Annotated[RequestMd5Models, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.rule_batch_delete(rtx_id=token_rtx_id, md5_list=params.model_dump().get("md5"))


@router.post("/redis.rule.preview", summary="预览规则匹配的缓存键")
async def rule_preview(
    params: Annotated[RequestMd5Model, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.preview(md5=params.model_dump().get("md5"))


@router.post("/redis.rule.clean", summary="按后台规则执行缓存清理")
async def rule_clean(
    params: Annotated[RequestMd5Model, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    service: SystemOpsRedisService = Depends(get_service)
) -> Status:
    return await service.clean(rtx_id=token_rtx_id, md5=params.model_dump().get("md5"))
