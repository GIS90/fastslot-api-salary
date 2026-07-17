# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    xtb_department curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:49
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = xtb_department.py

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
from sqlalchemy import select, update, delete, insert, desc, asc, or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_department import XtbDepartmentModel
from deploy.utils.exception import SQLDBHandleException
from deploy.config import depart_root as DEPART_ROOT_ID


class XtbDepartmentCurd(BaseCurd):

    @staticmethod
    async def new_model() -> XtbDepartmentModel:
        return XtbDepartmentModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbDepartmentModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbDepartmentModel, field):
                    return None
                _field = getattr(XtbDepartmentModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbDepartmentModel).where(
                _field == value,
                XtbDepartmentModel.status != 1
                )
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int):
        return await self._get_model_by_field(db, XtbDepartmentModel.id, _id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbDepartmentModel.md5, md5)

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15
    ) -> Optional[List]:
        ...

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        ...

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbDepartmentModel).where(XtbDepartmentModel.status != 1)
            if params.get("list"):
                stmt = stmt.where(XtbDepartmentModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(asc(XtbDepartmentModel.order_id), desc(XtbDepartmentModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def get_all(
        cls,
        db: AsyncSession,
        root: bool = False,
        filter_status: bool = False
    ) -> Optional[List]:
        try:
            stmt = select(XtbDepartmentModel)
            if filter_status:
                stmt = stmt.where(XtbDepartmentModel.status != True)
            if not root:
                stmt = stmt.where(XtbDepartmentModel.id != DEPART_ROOT_ID)
            stmt = stmt.order_by(asc(XtbDepartmentModel.order_id), desc(XtbDepartmentModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbDepartmentModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbDepartmentModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbDepartmentModel
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
            stmt = delete(XtbDepartmentModel).where(XtbDepartmentModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbDepartmentModel).where(XtbDepartmentModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
