# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    setter>profile view

base_info:
    __author__ = PyGo
    __time__ = 2026/5/11 22:36
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = profile.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, Body, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.setter.profile import SetterProfileService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx, pageable_params, pageable_like_params, depend_token_rtx_valid
from deploy.schema.po.setter_profile import ProfileUserBaseModel, ProfileUserPasswordModel
from deploy.schema.po.x import RequestMd5Model, RequestMd5StatusModel


# router
router: APIRouter = APIRouter(prefix="/setter", tags=["设置->个人中心"])
# service
def get_profile_service(db: AsyncSession = Depends(get_session)) -> SetterProfileService:
    return SetterProfileService(db_connection=db)


@router.get("/profile", summary="系统用户详情")
async def profile_detail(
    token_rtx_id: str = Depends(depend_token_rtx),
    profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_detail(rtx_id=token_rtx_id)


@router.put("/profile", summary="系统用户更新")
async def profile_update(
    data: Annotated[ProfileUserBaseModel, Body()],
    token_rtx_id: str = Depends(depend_token_rtx),
    profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_update(rtx_id=token_rtx_id, model=data.model_dump())


@router.put('/profile.password', summary="系统用户密码更新")
async def profile_password(
        data: Annotated[ProfileUserPasswordModel, Body()],
        token_rtx_id: str = Depends(depend_token_rtx),
        profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_password(rtx_id=token_rtx_id, model=data.model_dump())


@router.get('/profile.log', summary="系统用户日志")
async def profile_log(
        params: dict = Depends(pageable_params),
        token_rtx_id: str = Depends(depend_token_rtx_valid),
        profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_log(rtx_id=token_rtx_id, params=params)


@router.get('/profile.avatar.market', summary="头像超市列表")
async def profile_avatar_market(
        params: dict = Depends(pageable_like_params),
        type_: Optional[str] = Query(default=None, alias="type", description="头像分类"),
        favorite: bool = Query(default=False, description="仅查询我的收藏"),
        token_rtx_id: str = Depends(depend_token_rtx),
        profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_avatar_market(
        rtx_id=token_rtx_id, params=params, type_=type_, favorite_only=favorite
    )


@router.put('/profile.avatar.favorite', summary="收藏或取消收藏头像")
async def profile_avatar_favorite(
        data: Annotated[RequestMd5StatusModel, Body()],
        token_rtx_id: str = Depends(depend_token_rtx),
        profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_avatar_favorite(rtx_id=token_rtx_id, model=data.model_dump())


@router.put('/profile.avatar.set', summary="设置头像超市头像")
async def profile_avatar_set(
        data: Annotated[RequestMd5Model, Body()],
        token_rtx_id: str = Depends(depend_token_rtx),
        profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_avatar_set(rtx_id=token_rtx_id, md5=data.md5)


@router.post('/profile.avatar', summary="系统用户头像上传")
async def profile_avatar(
        file: UploadFile = File(...),
        token_rtx_id: str = Depends(depend_token_rtx),
        profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_avatar(rtx_id=token_rtx_id, image_file=file)

