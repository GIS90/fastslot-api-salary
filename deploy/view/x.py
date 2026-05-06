# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    user view

base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:55
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = user.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.x.user import UserService
from deploy.utils.status import Status
from deploy.utils.depend import depend_token_rtx

# router
router: APIRouter = APIRouter(prefix="/x", tags=["系统正常运行相关APIs"])
# service
def get_user_service(db: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(db_connection=db)


@router.get("/auth", summary="用户菜单权限，用于系统登录后获取用户权限菜单树")
async def auth(
    token_rtx_id: str = Depends(depend_token_rtx),
    user_service: UserService = Depends(get_user_service)
) -> Status:
    return await user_service.auth(token_rtx_id)
