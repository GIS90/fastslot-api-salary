# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_xtbb_field curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_xtbb_field.py

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
from sqlalchemy import select, update, delete, asc, desc, or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_xtbb_field import XtbXtbbFieldModel
from deploy.utils.exception import SQLDBHandleException


class XtbXtbbFieldCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbXtbbFieldModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any,
        filter_lock: bool = False
    ) -> Optional[XtbXtbbFieldModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbXtbbFieldModel, field):
                    return None
                _field = getattr(XtbXtbbFieldModel, field)
            else:
                _field = field

            stmt = select(XtbXtbbFieldModel).where(
                _field == value,
                XtbXtbbFieldModel.status != 1)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(
            self,
            db: AsyncSession,
            _id: int,
            filter_lock: bool = False
    ) -> Optional[XtbXtbbFieldModel]:
        return await self._get_model_by_field(db, XtbXtbbFieldModel.id, _id, filter_lock)

    async def get_by_md5(
            self,
            db: AsyncSession,
            md5: str,
            filter_lock: bool = False
    ) -> Optional[XtbXtbbFieldModel]:
        return await self._get_model_by_field(db, XtbXtbbFieldModel.md5, md5, filter_lock)

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbXtbbFieldModel.id)).where(XtbXtbbFieldModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def count_by_xtbb(cls, db: AsyncSession, xtbb: str) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbXtbbFieldModel.id)).where(
                    XtbXtbbFieldModel.status != 1,
                    XtbXtbbFieldModel.xtbb == xtbb
                )
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询总数]{e}")

    @classmethod
    async def count_by_md5_list(cls, db: AsyncSession, md5_list: List[str]) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbXtbbFieldModel.id)).where(
                    XtbXtbbFieldModel.status != 1,
                    XtbXtbbFieldModel.md5.in_(md5_list)
                )
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询总数]{e}")

    @classmethod
    async def list_by_xtbb(
        cls, db: AsyncSession, xtbb: str
    ) -> Optional[List]:
        try:
            stmt = select(XtbXtbbFieldModel).where(
                XtbXtbbFieldModel.status != 1,
                XtbXtbbFieldModel.xtbb == xtbb
            ).order_by(asc(XtbXtbbFieldModel.order_id), asc(XtbXtbbFieldModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*按报表查询]{e}")

    @classmethod
    async def column_by_xtbb(
        cls, db: AsyncSession, xtbb: str, list_: bool = True, export_: bool = False
    ) -> Optional[List]:
        # 不允许同真、同假
        if list_ == export_: return None
        try:
            stmt = (select(XtbXtbbFieldModel).where(
                XtbXtbbFieldModel.status != 1,
                XtbXtbbFieldModel.xtbb == xtbb
            ))
            stmt = stmt.where(XtbXtbbFieldModel.list == True) if list_ else stmt.where(XtbXtbbFieldModel.export == True)
            stmt.order_by(asc(XtbXtbbFieldModel.order_id), asc(XtbXtbbFieldModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*按报表查询]{e}")

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, content: str = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbXtbbFieldModel).where(XtbXtbbFieldModel.status != 1)
            if kwargs.get("xtbb"):
                stmt = stmt.where(XtbXtbbFieldModel.xtbb == kwargs.get("xtbb"))
            if content:
                stmt = stmt.where(
                    or_(
                        XtbXtbbFieldModel.field.like(content),
                        XtbXtbbFieldModel.name_ch.like(content),
                        XtbXtbbFieldModel.name_zh.like(content),
                        XtbXtbbFieldModel.remark.like(content)
                    )
                )
            stmt = stmt.order_by(asc(XtbXtbbFieldModel.order_id), asc(XtbXtbbFieldModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbXtbbFieldModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbXtbbFieldModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbXtbbFieldModel
    ) -> None:
        try:
            await db.delete(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*删除]{e}")

    @classmethod
    async def delete_by_xtbb_soft(
            cls, db: AsyncSession, xtbb: str, rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbXtbbFieldModel).where(XtbXtbbFieldModel.xtbb == xtbb).values(
                status=True,
                delete_rtx=rtx_id,
                delete_time=func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*表删除整个字段]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbXtbbFieldModel).where(XtbXtbbFieldModel.md5.in_(md5_list)).values(
                status=True,
                delete_rtx=rtx_id,
                delete_time=func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")

    @classmethod
    async def download(cls, db: AsyncSession, params: dict) -> Optional[List]:
        try:
            stmt = select(XtbXtbbFieldModel).where(XtbXtbbFieldModel.status != 1)
            if params.get("xtbb"):
                stmt = stmt.where(XtbXtbbFieldModel.xtbb == params.get("xtbb"))
            stmt = stmt.order_by(asc(XtbXtbbFieldModel.order_id), asc(XtbXtbbFieldModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*download]{e}")

    @classmethod
    async def batch_delete(cls, db: AsyncSession, md5_list: List[str]) -> None:
        try:
            await cls.batch_soft_delete_update(db=db, md5_list=md5_list, rtx_id="batch")
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*batch_delete]{e}")
