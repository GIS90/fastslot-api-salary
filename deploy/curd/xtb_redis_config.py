# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    curd of table xtb_redis_config

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = xtb_redis_config.py

usage:

design:

reference urls:

python version:
    python3


Enjoy the good life every day！！！
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional, List, Any
from sqlalchemy import select, update, desc, asc, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_redis_config import XtbRedisConfigModel
from deploy.utils.exception import SQLDBHandleException


__all__ = ["XtbRedisConfigCurd"]


class XtbRedisConfigCurd(BaseCurd):
    """Redis连接配置数据操作"""

    @staticmethod
    async def new_model() -> XtbRedisConfigModel:
        return XtbRedisConfigModel()

    @staticmethod
    def _not_deleted():
        return XtbRedisConfigModel.status != True

    async def _get_model_by_field(
            self,
            db: AsyncSession,
            field: str | InstrumentedAttribute,
            value: Any
    ) -> Optional[XtbRedisConfigModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbRedisConfigModel, field):
                    return None
                _field = getattr(XtbRedisConfigModel, field)
            else:
                _field = field
            result = await db.execute(
                select(XtbRedisConfigModel).where(_field == value, self._not_deleted())
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbRedisConfigModel.md5, md5)

    async def get_by_name(self, db: AsyncSession, name: str):
        return await self._get_model_by_field(db, XtbRedisConfigModel.name, name)

    @classmethod
    async def list_all(
            cls, db: AsyncSession, content: str = None, *args, **kwargs
    ) -> Optional[List[XtbRedisConfigModel]]:
        try:
            stmt = select(XtbRedisConfigModel).where(cls._not_deleted())
            if content:
                keyword = f"%{content}%"
                stmt = stmt.where(or_(
                    XtbRedisConfigModel.name.like(keyword),
                    XtbRedisConfigModel.host.like(keyword),
                ))
            stmt = stmt.order_by(asc(XtbRedisConfigModel.id))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(cls, db: AsyncSession, model: XtbRedisConfigModel) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(cls, db: AsyncSession, model: XtbRedisConfigModel) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def count(cls, db: AsyncSession, content: str = None, *args, **kwargs) -> int:
        try:
            stmt = select(func.count(XtbRedisConfigModel.id)).where(cls._not_deleted())
            if content:
                keyword = f"%{content}%"
                stmt = stmt.where(or_(
                    XtbRedisConfigModel.name.like(keyword),
                    XtbRedisConfigModel.host.like(keyword),
                ))
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def pagination(
            cls, db: AsyncSession, offset: int = 0, limit: int = 15,
            content: str = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbRedisConfigModel).where(cls._not_deleted())
            if content:
                keyword = f"%{content}%"
                stmt = stmt.where(or_(
                    XtbRedisConfigModel.name.like(keyword),
                    XtbRedisConfigModel.host.like(keyword),
                ))
            stmt = stmt.order_by(asc(XtbRedisConfigModel.order_id), asc(XtbRedisConfigModel.id)) \
                .offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*分页]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbRedisConfigModel).where(cls._not_deleted())
            if params.get("list"):
                stmt = stmt.where(XtbRedisConfigModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(asc(XtbRedisConfigModel.order_id), asc(XtbRedisConfigModel.id))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def delete(cls, db: AsyncSession, model: XtbRedisConfigModel) -> None:
        try:
            await db.delete(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*删除]{e}")

    @classmethod
    async def batch_soft_delete_update(cls, db: AsyncSession, md5_list: List[str], rtx_id: str) -> None:
        try:
            from deploy.utils.utils import get_now
            stmt = update(XtbRedisConfigModel).where(
                XtbRedisConfigModel.md5.in_(md5_list)
            ).values(status=True, delete_rtx=rtx_id, delete_time=get_now())
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")
