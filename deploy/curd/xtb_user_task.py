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

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_user_task import XtbUserTaskModel
from deploy.utils.exception import SQLDBHandleException


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
    async def get_count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbUserTaskModel.id)).where(XtbUserTaskModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def get_pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, rtx_id: str = None
    ) -> Optional[List]:
        try:
            stmt = select(XtbUserTaskModel).where(XtbUserTaskModel.status != 1)
            if rtx_id:
                stmt = stmt.where(XtbUserTaskModel.rtx_id == rtx_id)
            stmt = stmt.order_by(desc(XtbUserTaskModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        ...

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
