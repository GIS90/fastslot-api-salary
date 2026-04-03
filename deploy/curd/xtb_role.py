# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_role curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/4/2 23:26
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_role.py

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
from sqlalchemy import select, update, delete, insert, desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_role import XtbRoleModel
from deploy.utils.exception import SQLDBHandleException


class XtbRoleCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbRoleModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbRoleModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbRoleModel, field):
                    return None
                _field = getattr(XtbRoleModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbRoleModel).where(_field == value))
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, data_id: int):
        return await self._get_model_by_field(db, XtbRoleModel.id, data_id)

    async def get_by_md5_id(self, db: AsyncSession, md5_id: str):
        return await self._get_model_by_field(db, XtbRoleModel.md5_id, md5_id)

    @classmethod
    async def get_count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbRoleModel.id)).where(XtbRoleModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def get_pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15
    ) -> Optional[List]:
        try:
            stmt = (select(XtbRoleModel)
                    .where(XtbRoleModel.status != 1)
                    .order_by(desc(XtbRoleModel.id))
                    .offset(offset)
                    .limit(limit))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbRoleModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbRoleModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbRoleModel
    ) -> None:
        try:
            await db.delete(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*删除]{e}")

    @classmethod
    async def batch_delete(
            cls, db: AsyncSession, md5_id: List[str]
    ) -> None:
        try:
            stmt = delete(XtbRoleModel).where(XtbRoleModel.md5_id.in_(md5_id))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_id: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbRoleModel).where(XtbRoleModel.md5_id.in_(md5_id)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
