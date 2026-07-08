# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_menu curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:02
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_menu.py

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
from sqlalchemy import select, update, delete, insert, desc, asc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func, and_

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_menu import XtbMenuModel
from deploy.utils.exception import SQLDBHandleException
from deploy.config import menu_root as MENU_ROOT_ID


class XtbMenuCurd(BaseCurd):

    @staticmethod
    async def new_model() -> XtbMenuModel:
        return XtbMenuModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbMenuModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbMenuModel, field):
                    return None
                _field = getattr(XtbMenuModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbMenuModel).where(_field == value))
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int):
        return await self._get_model_by_field(db, XtbMenuModel.id, _id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbMenuModel.md5, md5)

    async def get_by_name(self, db: AsyncSession, name: str):
        return await self._get_model_by_field(db, XtbMenuModel.name, name)

    @classmethod
    async def get_count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbMenuModel.id)).where(XtbMenuModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def get_pagination(
            cls, db: AsyncSession, offset: int = 0, limit: int = 15, content: str = None, *args, **kwargs
    ) -> Optional[List]:
        ...

    @classmethod
    async def get_all(cls, db: AsyncSession, root: bool = True) -> Optional[List]:
        try:
            stmt = select(XtbMenuModel).where(XtbMenuModel.status != 1)
            if not root:
                stmt = stmt.where(XtbMenuModel.id != MENU_ROOT_ID)
            stmt = stmt.order_by(asc(XtbMenuModel.order_id), asc(XtbMenuModel.id))
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
            cls, db: AsyncSession, model: XtbMenuModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbMenuModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbMenuModel
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
            stmt = delete(XtbMenuModel).where(XtbMenuModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbMenuModel).where(XtbMenuModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
