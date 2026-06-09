# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_xtcs curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/26 22:33
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtcs.py

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
from deploy.schema.dao.xtb_xtcs import XtbXtcsModel
from deploy.utils.exception import SQLDBHandleException


class XtbXtcsCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbXtcsModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any,
        filter_lock: bool = False
    ) -> Optional[XtbXtcsModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbXtcsModel, field):
                    return None
                _field = getattr(XtbXtcsModel, field)
            else:
                _field = field

            stmt = select(XtbXtcsModel).where(
                _field == value,
                XtbXtcsModel.status != 1)
            if filter_lock:
                stmt = stmt.where(XtbXtcsModel.lock != True)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(
            self,
            db: AsyncSession,
            _id: int,
            filter_lock: bool = False
    ) -> Optional[XtbXtcsModel]:
        return await self._get_model_by_field(db, XtbXtcsModel.id, _id, filter_lock)

    async def get_by_key(
            self,
            db: AsyncSession,
            key: str,
            filter_lock: bool = False
    ) -> Optional[XtbXtcsModel]:
        return await self._get_model_by_field(db, XtbXtcsModel.key, key, filter_lock)

    async def get_by_md5(
            self,
            db: AsyncSession,
            md5: str,
            filter_lock: bool = False
    ) -> Optional[XtbXtcsModel]:
        return await self._get_model_by_field(db, XtbXtcsModel.md5, md5, filter_lock)

    @classmethod
    async def get_count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbXtcsModel.id)).where(XtbXtcsModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def get_pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15
    ) -> Optional[List]:
        try:
            stmt = (select(XtbXtcsModel)
                    .where(XtbXtcsModel.status != 1)
                    .order_by(asc(XtbXtcsModel.order_id), desc(XtbXtcsModel.id))
                    .offset(offset)
                    .limit(limit))
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
            cls, db: AsyncSession, model: XtbXtcsModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbXtcsModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbXtcsModel
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
            stmt = delete(XtbXtcsModel).where(XtbXtcsModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbXtcsModel).where(XtbXtcsModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
