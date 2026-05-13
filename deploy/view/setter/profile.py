# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

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
from typing import Annotated, List
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.setter.profile import SetterProfileService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx
from deploy.schema.po.xtb_user import XtbUserAddModel, XtbUserUpdateModel


# router
router: APIRouter = APIRouter(prefix="/setter", tags=["设置-个人中心"])
# service
def get_profile_service(db: AsyncSession = Depends(get_session)) -> SetterProfileService:
    return SetterProfileService(db_connection=db)


@router.get("/profile", summary="通过Md5-Id获取单条数据")
async def profile(
    md5: str = Query(..., description="数据Md5-Id"),
    token_rtx_id: str = Depends(depend_token_rtx),
    profile_service: SetterProfileService = Depends(get_profile_service)
) -> Status:
    return await profile_service.profile_detail(rtx_id=token_rtx_id, md5=md5)
