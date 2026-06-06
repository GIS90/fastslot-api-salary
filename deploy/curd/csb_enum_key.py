# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    csb_enum_key curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/26 22:33
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = csb_enum_key.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, asc, desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.csb_enum_key import CsbEnumKeyModel
from deploy.utils.exception import SQLDBHandleException


class CsbEnumKeyCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return CsbEnumKeyModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any,
        filter_lock: bool = False
    ) -> Optional[CsbEnumKeyModel]:
        try:
            if isinstance(field, str):
                if not hasattr(CsbEnumKeyModel, field):
                    return None
                _field = getattr(CsbEnumKeyModel, field)
            else:
                _field = field

            stmt = select(CsbEnumKeyModel).where(
                _field == value,
                CsbEnumKeyModel.status != 1)
            if filter_lock:
                stmt = stmt.where(CsbEnumKeyModel.lock != True)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(
            self,
            db: AsyncSession,
            _id: int,
            filter_lock: bool = False
    ) -> Optional[CsbEnumKeyModel]:
        return await self._get_model_by_field(db, CsbEnumKeyModel.id, _id, filter_lock)

    async def get_by_md5(
            self,
            db: AsyncSession,
            md5: str,
            filter_lock: bool = False
    ) -> Optional[CsbEnumKeyModel]:
        return await self._get_model_by_field(db, CsbEnumKeyModel.md5, md5, filter_lock)

    @classmethod
    async def get_count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(CsbEnumKeyModel.id)).where(CsbEnumKeyModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def get_pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15
    ) -> Optional[List]:
        try:
            stmt = (select(CsbEnumKeyModel)
                    .where(CsbEnumKeyModel.status != 1)
                    .order_by(asc(CsbEnumKeyModel.order_id), desc(CsbEnumKeyModel.id))
                    .offset(offset)
                    .limit(limit))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: CsbEnumKeyModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: CsbEnumKeyModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: CsbEnumKeyModel
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
            stmt = delete(CsbEnumKeyModel).where(CsbEnumKeyModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(CsbEnumKeyModel).where(CsbEnumKeyModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
