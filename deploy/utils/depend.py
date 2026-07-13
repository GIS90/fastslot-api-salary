# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    depend

base_info:
    __author__ = PyGo
    __time__ = 2025/12/6 10:47
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = depend.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from os.path import splitext as os_path_splitext
from fastapi import Header, Query
from typing import Optional, Dict, List

from deploy.utils.token import decode_access_token_rtx
from deploy.utils.exception import JwtCredentialsException, UserInvalidException
from deploy.utils.utils import get_now
from deploy.delib.redis_lib import RedisClientLib
from deploy.config import redis_host, redis_port, redis_db, redis_password
from deploy.schema.po.x import PageFilterModel, DownloadFileModel
from deploy.schema.po.system_main_menu import XtbMenuBaseModel, XtbMenuUpdateModel
from deploy.curd.database import get_session_context
from deploy.service.system.main.user import SystemMainUserService
from deploy.utils.enumeration import DownloadExcelFormat as DEF


# redis-cli
redis_cli = RedisClientLib(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
# parameters
MIN_LENGTH = 1
MAX_LENGTH = 299


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Token-Rtx-ID依赖
> depend_token_rtx：解码X-Token的Rtx-id
> depend_token_rtx_valid：解码X-Token的Rtx-id + 验证用户可用性（过滤数据不存在、已删除）
"""


async def __get_token_rtx(token: str) -> str:
    token_rtx_id = None
    # >>>>> 优先redis
    try:
        if redis_cli.connection:
            token_rtx_id = redis_cli.get_key(key=token)
    except:
        ...

    # >>>>> jwt解码token
    if not token_rtx_id:
        token_rtx_id = await decode_access_token_rtx(token)
        if not token_rtx_id:
            raise JwtCredentialsException("无效X-Token")

    return token_rtx_id


async def depend_token_rtx(
    x_token: str = Header(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH, convert_underscores=True, description="X-Token")
) -> str:
    return await __get_token_rtx(token=x_token)


async def depend_token_rtx_valid(
    x_token: str = Header(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH, convert_underscores=True, description="X-Token")
) -> str:
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    token_rtx_id = await __get_token_rtx(token=x_token)
    # 用户数据验证
    async with get_session_context() as db:
        try:
            service: SystemMainUserService = SystemMainUserService(db_connection=db)
            # 调用 add 方法
            model = await service.depend_by_rtx_id(rtx_id=token_rtx_id)
        except Exception as e:
            raise UserInvalidException("用户信息异常")
        # 数据不存在
        if not model:
            raise UserInvalidException("用户不存在")
        # 数据已删除
        if getattr(model, "status"):
            raise UserInvalidException("用户已注销")

    return token_rtx_id


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
md5参数请求
> md5_params：Md5单条参数请求体
> md5_list_params：Md5列表参数请求体
"""
async def md5_params(
    md5: str = Query(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH, description="数据Md5-Id")
) -> str:
    return md5


async def md5_list_params(
    md5: List[str] = Query(..., description="数据Md5-Id列表")
) -> List:
    return md5


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Pageable-Params依赖
> pageable_params：分页参数
> pageable_query_params：分页参数 + 非模糊查询
> pageable_like_params：分页参数 + 模糊查询
> pageable_model_params：分页参数 + 条件数据模型（type：dict）
"""
async def pageable_params(
    page: int = Query(default=1, ge=MIN_LENGTH, description="页码"),
    pageSize: int = Query(default=15, ge=MIN_LENGTH, description="条数"),
) -> Dict:
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize}


async def pageable_query_params(
    page: int = Query(default=1, ge=MIN_LENGTH, description="页码"),
    pageSize: int = Query(default=15, ge=MIN_LENGTH, description="条数"),
    content: str | None = Query(default=None, max_length=MAX_LENGTH, description="非模糊查询"),
) -> Dict:
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize, "content": content}


async def pageable_like_params(
    page: int = Query(default=1, ge=MIN_LENGTH, description="页码"),
    pageSize: int = Query(default=15, ge=MIN_LENGTH, description="条数"),
    content: Optional[str] = Query(default=None, max_length=MAX_LENGTH, description="模糊查询参数"),
) -> Dict:
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize, "content": f"%{content}%"}


async def pageable_model_params(
    params: PageFilterModel
) -> Dict:
    page, pageSize, filter_ = params.page, params.pageSize, params.filter
    if filter_.get("content"):
        filter_["content"] = "%" + filter_.get("content") + "%"
    if filter_.get("dateRange"):
        filter_["start"] = filter_.get("dateRange")[0] + " 00:00:00"
        filter_["end"] = filter_.get("dateRange")[1] + " 23:59:59"
        filter_.pop("dateRange")
    return {"page": page, "limit": pageSize, "offset": (page - 1) * pageSize, "filter_": filter_}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
X->Download依赖
> download_params：下载数据请求参数
"""
async def download_params(params: DownloadFileModel) -> Dict:
    file_name = params.name
    # 直接是.xlsx、.xls格式，名称则自动加上时间戳
    if file_name in [DEF.XLSX.value, DEF.XLS.value]:
        file_name = "%s%s" % (get_now(format="%Y-%m-%d-%H-%M-%S"), file_name)
    # 文件名称不包含扩展名，则自动加上扩展名
    file_names = os_path_splitext(file_name)
    if not file_names[1]:
        file_name = "%s%s" % (file_name, DEF.XLSX.value)
    # 扩展名不是.xlsx、.xls，则自动加上扩展名
    if file_names[1] not in [DEF.XLSX.value, DEF.XLS.value]:
        file_name = "%s%s" % (file_name, DEF.XLSX.value)
    return {"api": params.api, "name": file_name, "md5": params.md5, "type": params.type}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""
Menu菜单依赖
"""


async def __menu_params(params: Dict) -> Dict:
    new_params: Dict = {}
    for key, value in params.items():
        if key == "isKeepAlive":
            new_params["cache"] = value
        elif key == "isAffix":
            new_params["affix"] = value
        elif key == "isFull":
            new_params["full"] = value
        elif key == "isBreadcrumb":
            new_params["breadcrumb"] = value
        else:
            new_params[key] = value
    return new_params


async def menu_edit_params(params: XtbMenuUpdateModel) -> Dict:
    return await __menu_params(params=params.model_dump())


async def menu_add_params(params: XtbMenuBaseModel) -> Dict:
    return await __menu_params(params=params.model_dump())
