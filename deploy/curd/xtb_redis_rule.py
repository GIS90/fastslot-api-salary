# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    curd of table xtb_redis_rule

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = xtb_redis_rule.py

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
from sqlalchemy import select, func, update, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import InstrumentedAttribute

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_redis_rule import XtbRedisRuleModel
from deploy.utils.exception import SQLDBHandleException


__all__ = ["XtbRedisRuleCurd"]


class XtbRedisRuleCurd(BaseCurd):
    """Redis清理规则数据操作"""

    @staticmethod
    async def new_model() -> XtbRedisRuleModel:
        return XtbRedisRuleModel()

    @staticmethod
    def _not_deleted():
        return XtbRedisRuleModel.status != True

    async def _get_model_by_field(
            self,
            db: AsyncSession,
            field: str | InstrumentedAttribute,
            value: Any
    ) -> Optional[XtbRedisRuleModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbRedisRuleModel, field):
                    return None
                _field = getattr(XtbRedisRuleModel, field)
            else:
                _field = field
            result = await db.execute(
                select(XtbRedisRuleModel).where(_field == value, self._not_deleted())
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbRedisRuleModel.md5, md5)

    async def get_by_name(self, db: AsyncSession, name: str):
        return await self._get_model_by_field(db, XtbRedisRuleModel.name, name)

    @classmethod
    async def count(
            cls, db: AsyncSession, filter_: dict = None, *args, **kwargs
    ) -> int:
        try:
            filter_ = filter_ or {}
            stmt = select(func.count(XtbRedisRuleModel.id)).where(cls._not_deleted())
            stmt = cls._apply_filter(stmt, filter_)
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    def _apply_filter(cls, stmt, filter_: dict):
        content = filter_.get("content")
        if content:
            keyword = f"%{content}%"
            stmt = stmt.where(or_(
                XtbRedisRuleModel.name.like(keyword),
                XtbRedisRuleModel.pattern.like(keyword),
                XtbRedisRuleModel.summary.like(keyword),
            ))
        if filter_.get("redisMd5") or filter_.get("configMd5"):
            _redis_md5 = filter_.get("redisMd5") or filter_.get("configMd5")
            stmt = stmt.where(XtbRedisRuleModel.redis_md5 == _redis_md5)
        if filter_.get("match"):
            _match = filter_.get("match")
            stmt = stmt.where(XtbRedisRuleModel.match.in_(_match if isinstance(_match, list) else [_match]))
        if filter_.get("lock") in (True, False):
            stmt = stmt.where(XtbRedisRuleModel.lock == filter_.get("lock"))
        return stmt

    @classmethod
    async def pagination(
            cls, db: AsyncSession, offset: int = 0, limit: int = 15,
            filter_: dict = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            filter_ = filter_ or {}
            stmt = select(XtbRedisRuleModel).where(cls._not_deleted())
            stmt = cls._apply_filter(stmt, filter_)
            stmt = stmt.order_by(
                asc(XtbRedisRuleModel.lock),
                asc(XtbRedisRuleModel.order_id),
                desc(XtbRedisRuleModel.create_time),
                desc(XtbRedisRuleModel.id),
            ).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*分页]{e}")

    @classmethod
    async def add(cls, db: AsyncSession, model: XtbRedisRuleModel) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(cls, db: AsyncSession, model: XtbRedisRuleModel) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def get_models_by_md5_list(cls, db: AsyncSession, md5_list: List[str]):
        try:
            result = await db.execute(
                select(XtbRedisRuleModel).where(
                    XtbRedisRuleModel.md5.in_(md5_list), cls._not_deleted()
                )
            )
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询]{e}")

    @classmethod
    async def batch_soft_delete_update(cls, db: AsyncSession, md5_list: List[str], rtx_id: str) -> None:
        try:
            from deploy.utils.utils import get_now
            stmt = update(XtbRedisRuleModel).where(
                XtbRedisRuleModel.md5.in_(md5_list)
            ).values(status=True, delete_rtx=rtx_id, delete_time=get_now())
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")
