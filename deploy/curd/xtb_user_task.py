# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_user_task curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/6/7 16:34
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user_task.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, asc, desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func
from sqlalchemy.orm import aliased

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_user_task import XtbUserTaskModel
from deploy.schema.dao.csb_enum_value import CsbEnumValueModel
from deploy.utils.exception import SQLDBHandleException
from deploy.utils.enumeration import CsbEnumKEY
from deploy.utils.utils import automatic_time


EV1 = aliased(CsbEnumValueModel)
EV2 = aliased(CsbEnumValueModel)


class XtbUserTaskCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbUserTaskModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbUserTaskModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbUserTaskModel, field):
                    return None
                _field = getattr(XtbUserTaskModel, field)
            else:
                _field = field

            stmt = select(XtbUserTaskModel).where(
                _field == value,
                XtbUserTaskModel.status != 1)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int) -> Optional[XtbUserTaskModel]:
        return await self._get_model_by_field(db, XtbUserTaskModel.id, _id)

    async def get_by_md5(self, db: AsyncSession, md5: str) -> Optional[XtbUserTaskModel]:
        return await self._get_model_by_field(db, XtbUserTaskModel.md5, md5)

    @classmethod
    async def count(cls, db: AsyncSession, rtx_id: str = None, filter_: Dict | None = None) -> int:
        if filter_ is None: filter_ = {}
        try:
            stmt = select(func.count(XtbUserTaskModel.id)).where(XtbUserTaskModel.status != 1)
            if rtx_id:
                stmt = stmt.where(XtbUserTaskModel.rtx_id == rtx_id)
            if filter_.get("ds"):
                stmt = stmt.where(XtbUserTaskModel.data.in_(filter_.get("ds")))
            if filter_.get("status"):
                stmt = stmt.where(XtbUserTaskModel.task.in_(filter_.get("status")))
            if filter_.get("user"):
                stmt = stmt.where(XtbUserTaskModel.rtx_id.in_(filter_.get("user")))
            if filter_.get("content"):
                stmt = stmt.where(XtbUserTaskModel.name.like(f"%{filter_.get('content')}%"))
            if filter_.get("dateRange"):
                __start, __end = automatic_time(dateRange=filter_.get("dateRange"))
                stmt = stmt.where(XtbUserTaskModel.create_time.between(__start, __end))
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def count_by_md5_list(cls, db: AsyncSession, md5_list: List[str]) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbUserTaskModel.id)).where(
                    XtbUserTaskModel.status != 1,
                    XtbUserTaskModel.md5.in_(md5_list)
                )
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询总数]{e}")

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, rtx_id: str = None, filter_: Dict | None = None
    ) -> Optional[List]:
        if filter_ is None: filter_ = {}
        try:
            stmt = (select(
                XtbUserTaskModel.rtx_id,
                XtbUserTaskModel.api,
                XtbUserTaskModel.name,
                XtbUserTaskModel.md5,
                XtbUserTaskModel.data,
                EV1.value.label("data_value"),
                XtbUserTaskModel.task,
                EV2.value.label("task_value"),
                XtbUserTaskModel.cost,
                XtbUserTaskModel.create_time,
                XtbUserTaskModel.update_time,
            ).outerjoin(
                EV1,
                XtbUserTaskModel.data == EV1.key
            ).outerjoin(
                EV2,
                XtbUserTaskModel.task == EV2.key
            ).where(
                XtbUserTaskModel.status != 1,
                EV1.name == CsbEnumKEY.DOWNLOAD_SELECT.value,
                EV2.name == CsbEnumKEY.TASK_STATUS.value
            ))
            if rtx_id:
                stmt = stmt.where(XtbUserTaskModel.rtx_id == rtx_id)
            if filter_.get("ds"):
                stmt = stmt.where(XtbUserTaskModel.data.in_(filter_.get("ds")))
            if filter_.get("status"):
                stmt = stmt.where(XtbUserTaskModel.task.in_(filter_.get("status")))
            if filter_.get("user"):
                stmt = stmt.where(XtbUserTaskModel.rtx_id.in_(filter_.get("user")))
            if filter_.get("content"):
                stmt = stmt.where(XtbUserTaskModel.name.like(f"%{filter_.get('content')}%"))
            if filter_.get("dateRange"):
                __start, __end = automatic_time(dateRange=filter_.get("dateRange"))
                stmt = stmt.where(XtbUserTaskModel.create_time.between(__start, __end))
            stmt = stmt.order_by(desc(XtbUserTaskModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.mappings().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = (select(
                XtbUserTaskModel.rtx_id,
                XtbUserTaskModel.api,
                XtbUserTaskModel.name,
                XtbUserTaskModel.md5,
                XtbUserTaskModel.data,
                EV1.value.label("data_value"),
                XtbUserTaskModel.task,
                EV2.value.label("task_value"),
                XtbUserTaskModel.cost,
                XtbUserTaskModel.create_time,
                XtbUserTaskModel.update_time,
            ).outerjoin(
                EV1,
                XtbUserTaskModel.data == EV1.key
            ).outerjoin(
                EV2,
                XtbUserTaskModel.task == EV2.key
            ).where(
                XtbUserTaskModel.status != 1,
                EV1.name == CsbEnumKEY.DOWNLOAD_SELECT.value,
                EV2.name == CsbEnumKEY.TASK_STATUS.value
            ))
            if params.get("list"):
                stmt = stmt.where(XtbUserTaskModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(desc(XtbUserTaskModel.create_time))
            result = await db.execute(stmt)
            return result.mappings().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbUserTaskModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbUserTaskModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbUserTaskModel
    ) -> None:
        try:
            await db.delete(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*删除]{e}")

    @classmethod
    async def batch_delete(
            cls, db: AsyncSession, md5_list: List[str]
    ) -> None:
        try:
            stmt = delete(XtbUserTaskModel).where(XtbUserTaskModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbUserTaskModel).where(XtbUserTaskModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
