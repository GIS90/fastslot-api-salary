# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_xtbb curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtbb.py

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
from sqlalchemy import select, update, delete, insert, asc, desc, or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_xtbb import XtbXtbbModel
from deploy.utils.exception import SQLDBHandleException


class XtbXtbbCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbXtbbModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any,
        filter_lock: bool = False
    ) -> Optional[XtbXtbbModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbXtbbModel, field):
                    return None
                _field = getattr(XtbXtbbModel, field)
            else:
                _field = field

            stmt = select(XtbXtbbModel).where(
                _field == value,
                XtbXtbbModel.status != 1)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(
            self,
            db: AsyncSession,
            _id: int,
            filter_lock: bool = False
    ) -> Optional[XtbXtbbModel]:
        return await self._get_model_by_field(db, XtbXtbbModel.id, _id, filter_lock)

    async def get_by_md5(
            self,
            db: AsyncSession,
            md5: str,
            filter_lock: bool = False
    ) -> Optional[XtbXtbbModel]:
        return await self._get_model_by_field(db, XtbXtbbModel.md5, md5, filter_lock)

    async def get_by_name(
            self,
            db: AsyncSession,
            name: str,
            filter_lock: bool = False
    ) -> Optional[XtbXtbbModel]:
        return await self._get_model_by_field(db, XtbXtbbModel.name, name, filter_lock)

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbXtbbModel.id)).where(XtbXtbbModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def count_by_md5_list(cls, db: AsyncSession, md5_list: List[str]) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbXtbbModel.id)).where(
                    XtbXtbbModel.status != 1,
                    XtbXtbbModel.md5.in_(md5_list)
                )
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询总数]{e}")

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, content: str = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbXtbbModel).where(XtbXtbbModel.status != 1)
            if content:
                stmt = stmt.where(
                    or_(
                        XtbXtbbModel.name.like(content),
                        XtbXtbbModel.table.like(content),
                        XtbXtbbModel.remark.like(content)
                    )
                )
            stmt = stmt.order_by(asc(XtbXtbbModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbXtbbModel).where(XtbXtbbModel.status != 1)
            if params.get("list"):
                stmt = stmt.where(XtbXtbbModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(asc(XtbXtbbModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbXtbbModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbXtbbModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbXtbbModel
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
            stmt = delete(XtbXtbbModel).where(XtbXtbbModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbXtbbModel).where(XtbXtbbModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
