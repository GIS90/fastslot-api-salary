# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user service

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:22
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_user import XtbUserCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_user import xtb_user_list_fields, xtb_user_detail_fields, xtb_user_login_fields
from deploy.utils.utils import get_now, random_string, md5 as generator_md5
from deploy.config import server_user as SERVER_USER_ADMIN


class XtbUserService:

    DEFAULT_AVATAR: str = "http://pygo2.top/images/article_github.jpg"

    def __init__(self, db_connection: AsyncSession):
        """
        XtbUserService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_curd: XtbUserCurd = XtbUserCurd()

    def __str__(self):
        print("XtbUserService class.")

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5_or_rtx(
            self,
            query_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            query_type: Literal["md5", "rtx"] = "md5",
            fields: List[Dict] = xtb_user_detail_fields
    ) -> Tuple[bool, Any]:
        if not query_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数" if query_type == "md5" else "缺少rtx参数")

        model: XtbUserModel = await self.xtb_user_curd.get_by_md5(db=self.db, md5=query_id) if query_type == "md5" \
            else await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=query_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List = await self.xtb_user_curd.get_pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit")
        )
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        data: List = list()
        data.extend(
            filter(
                lambda x: x is not None and x is not {},
                [await model_converter_dict(model=u, fields=xtb_user_list_fields) for u in models if u]
            )
        )
        result: Dict = {
            "list": data,
            "total": await self.xtb_user_curd.get_count(self.db)
        }
        return SuccessStatus(data=result)

    async def login_by_rtx_id(self, rtx_id: str) -> Dict:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=rtx_id,
            status_check=False,
            response_type="dict",
            query_type="rtx",
            fields=xtb_user_login_fields
        )
        return data if __flag else None

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=False, response_type="dict", query_type="md5"
        )
        return SuccessStatus(data=data) if __flag else data

    async def depend_by_rtx_id(self, rtx_id: str) -> Dict:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=rtx_id, status_check=False, response_type="dict", query_type="rtx"
        )
        return data if __flag else {}

    async def add(self, rtx_id: str, model: Dict) -> Status:
        db_model: XtbUserModel = await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=model.get("rtx_id"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="用户rtx_id已存在，请更换")

        new_model: XtbUserModel = await self.xtb_user_curd.new_model()
        __password: str = random_string()
        __salt: str = random_string()
        # TODO 用户默认的头像、密码可以放在数据库中
        new_model.md5 = generator_md5(v=f"{model.get('rtx_id')}-{get_now()}-{__password}")
        new_model.avatar = self.DEFAULT_AVATAR
        new_model.status = False
        new_model.salt = __salt
        new_model.create_time = datetime.now()
        new_model.create_rtx = rtx_id
        new_model.password = generator_md5(v=f"{__password}{__salt}")
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_user_curd.add(db=self.db, model=new_model)
        return SuccessStatus(data={"password": __password})

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        if model.get("rtx_id"):
            del model["rtx_id"]
        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_hard(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=True, response_type="model", query_type="md5"
        )
        if not __flag: return data

        await self.xtb_user_curd.delete(db=self.db, model=data)
        return SuccessStatus()


    async def delete_soft(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5_or_rtx(
            query_id=md5, status_check=True, response_type="model", query_type="md5"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_user_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def __verify_contain_admin_user(self, md5_list: List) -> Tuple[bool, Any]:
        db_model: List = await self.xtb_user_curd.get_rtx_by_md5_list(db=self.db, md5_list=md5_list)
        if db_model and SERVER_USER_ADMIN in db_model:
            return True, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="管理员用户不允许删除")
        else:
            return False, db_model

    async def batch_delete_hard(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_user(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_user_curd.batch_delete(db=self.db, md5_list=md5_list)
        return SuccessStatus() if query_count == len(md5_list) \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def batch_delete_soft(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_user(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_user_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == len(md5_list) \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")
