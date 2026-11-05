# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_api curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/7/20 00:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_api.py

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
from sqlalchemy import select, update, delete, desc, asc, or_, func
from sqlalchemy.orm.attributes import InstrumentedAttribute

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_api import XtbApiModel
from deploy.utils.exception import SQLDBHandleException


class XtbApiCurd(BaseCurd):

    @staticmethod
    async def new_model() -> XtbApiModel:
        return XtbApiModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbApiModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbApiModel, field):
                    return None
                _field = getattr(XtbApiModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbApiModel).where(
                _field == value,
                XtbApiModel.status != 1
                )
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int):
        return await self._get_model_by_field(db, XtbApiModel.id, _id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbApiModel.md5, md5)

    async def get_by_endpoint(self, db: AsyncSession, endpoint: str):
        return await self._get_model_by_field(db, XtbApiModel.endpoint, endpoint)

    async def get_by_apiname(self, db: AsyncSession, apiname: str):
        return await self._get_model_by_field(db, XtbApiModel.apiname, apiname)

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbApiModel.id)).where(XtbApiModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def count_by_md5_list(
        cls, db: AsyncSession, md5_list: List
    ) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbApiModel.id)).where(
                    XtbApiModel.md5.in_(md5_list),
                    XtbApiModel.status != 1
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
            stmt = select(XtbApiModel).where(XtbApiModel.status != 1)
            if content:
                stmt = stmt.where(
                    or_(
                        XtbApiModel.blueprint.like(content),
                        XtbApiModel.apiname.like(content),
                        XtbApiModel.endpoint.like(content),
                        XtbApiModel.path.like(content),
                        XtbApiModel.short.like(content),
                        XtbApiModel.long.like(content)
                    )
                )
            stmt = stmt.order_by(asc(XtbApiModel.order_id), desc(XtbApiModel.create_time), asc(XtbApiModel.id)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbApiModel).where(XtbApiModel.status != 1)
            if params.get("list"):
                stmt = stmt.where(XtbApiModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(asc(XtbApiModel.order_id), asc(XtbApiModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def get_all(
        cls,
        db: AsyncSession,
        filter_status: bool = False
    ) -> Optional[List]:
        try:
            stmt = select(XtbApiModel)
            if filter_status:
                stmt = stmt.where(XtbApiModel.status != 1)
            stmt = stmt.order_by(desc(XtbApiModel.create_time), asc(XtbApiModel.id))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbApiModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbApiModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbApiModel
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
            stmt = delete(XtbApiModel).where(XtbApiModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbApiModel).where(XtbApiModel.md5.in_(md5_list)).values(
                status=True,
                delete_rtx=rtx_id,
                delete_time=func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
