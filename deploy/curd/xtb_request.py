# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_request curd
base_info:
    __author__ = PyGo
    __time__ = 2026/3/26 23:25
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_request.py

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
from sqlalchemy import select, update, delete, insert, desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_request import XtbRequestModel
from deploy.utils.exception import SQLDBHandleException


class XtbRequestCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbRequestModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbRequestModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbRequestModel, field):
                    return None
                _field = getattr(XtbRequestModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbRequestModel).where(_field == value))
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, data_id: int):
        return await self._get_model_by_field(db, XtbRequestModel.id, data_id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbRequestModel.md5, md5)

    @classmethod
    async def count(cls, db: AsyncSession, rtx_id: str = None, **filter_) -> int:
        try:
            stmt = select(func.count(XtbRequestModel.id)).where(XtbRequestModel.status != 1)
            if rtx_id:
                stmt = stmt.where(XtbRequestModel.rtx_id == rtx_id)
            if filter_.get("method"):
                stmt = stmt.where(XtbRequestModel.method.in_(filter_.get("method")))
            if filter_.get("user"):
                stmt = stmt.where(XtbRequestModel.rtx_id.in_(filter_.get("user")))
            if filter_.get("content"):
                stmt = stmt.where(XtbRequestModel.url.like(f"%{filter_.get('content')}%"))
            if filter_.get("dateRange"):
                stmt = stmt.where(XtbRequestModel.create_time.between(filter_.get("dateRange")[0], filter_.get("dateRange")[1]))
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def count_by_md5_list(cls, db: AsyncSession, md5_list: List[str]) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbRequestModel.id)).where(
                    XtbRequestModel.status != 1,
                    XtbRequestModel.md5.in_(md5_list)
                )
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询总数]{e}")

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, rtx_id: str = None, **filter_
    ) -> Optional[List]:
        try:
            stmt = select(XtbRequestModel).where(XtbRequestModel.status != 1)
            if rtx_id:
                stmt = stmt.where(XtbRequestModel.rtx_id == rtx_id)
            if filter_.get("method"):
                stmt = stmt.where(XtbRequestModel.method.in_(filter_.get("method")))
            if filter_.get("user"):
                stmt = stmt.where(XtbRequestModel.rtx_id.in_(filter_.get("user")))
            if filter_.get("content"):
                stmt = stmt.where(XtbRequestModel.url.like(f"%{filter_.get('content')}%"))
            if filter_.get("dateRange"):
                stmt = stmt.where(XtbRequestModel.create_time.between(filter_.get("dateRange")[0], filter_.get("dateRange")[1]))
            stmt = (stmt
                    .order_by(desc(XtbRequestModel.id))
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
        try:
            stmt = select(XtbRequestModel).where(XtbRequestModel.status != 1)
            if params.get("list"):
                stmt = stmt.where(XtbRequestModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(desc(XtbRequestModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbRequestModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbRequestModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbRequestModel
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
            stmt = delete(XtbRequestModel).where(XtbRequestModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbRequestModel).where(XtbRequestModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
