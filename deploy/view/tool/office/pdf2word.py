# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/8/8 11:58
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = pdf2word.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Annotated, Dict, List
from fastapi import APIRouter, Depends, Query, Body, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.database import get_session
from deploy.service.tool.office.pdf2word import ToolOfficePdf2WordService
from deploy.utils.status import Status
from deploy.utils.depend import pageable_like_params, auth_token_rtx, depend_token_rtx, md5_params, md5_list_params
from deploy.schema.po.system_main_user import XtbUserAddModel, XtbUserUpdateModel, XtbUserImportModel
from deploy.schema.po.x import RequestMd5Models, RequestMd5StatusModel


# router
router: APIRouter = APIRouter(prefix="/tool/office", tags=["工具->文档工具->PDF转WORD"])
# service
def get_service(db: AsyncSession = Depends(get_session)) -> ToolOfficePdf2WordService:
    return ToolOfficePdf2WordService(db_connection=db)


@router.get("/pdf2word.list", summary="数据列表")
async def pagination(
    params: dict = Depends(pageable_like_params),
    token_rtx_id: str = Depends(auth_token_rtx),
    service: ToolOfficePdf2WordService = Depends(get_service)
) -> Status:
    return await service.pagination(rtx_id=token_rtx_id, params=params)