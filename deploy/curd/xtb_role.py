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
from typing import Optional, List, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, desc, asc, or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_role import XtbRoleModel
from deploy.utils.exception import SQLDBHandleException


class XtbRoleCurd(BaseCurd):

    @staticmethod
    async def new_model() -> XtbRoleModel:
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

            result = await db.execute(select(XtbRoleModel).where(
                _field == value,
                XtbRoleModel.status != 1
                )
            )
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int):
        return await self._get_model_by_field(db, XtbRoleModel.id, _id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbRoleModel.md5, md5)

    async def get_by_engname(self, db: AsyncSession, engname: str):
        return await self._get_model_by_field(db, XtbRoleModel.engname, engname)

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbRoleModel.id)).where(XtbRoleModel.status != 1)
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, content: str = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbRoleModel).where(XtbRoleModel.status != 1)
            if content:
                stmt = stmt.where(
                    or_(
                        XtbRoleModel.engname.like(content),
                        XtbRoleModel.chnname.like(content),
                        XtbRoleModel.introduction.like(content)
                    )
                )
            stmt = stmt.order_by(desc(XtbRoleModel.create_time), asc(XtbRoleModel.id)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbRoleModel).where(XtbRoleModel.status != 1)
            if params.get("list"):
                stmt = stmt.where(XtbRoleModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(asc(XtbRoleModel.create_time))
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
            stmt = select(XtbRoleModel)
            if filter_status:
                stmt = stmt.where(XtbRoleModel.status != 1)
            stmt = stmt.order_by(desc(XtbRoleModel.create_time), asc(XtbRoleModel.id))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def get_engname_by_md5_list(
        cls, db: AsyncSession, md5_list: List
    ) -> Optional[List]:
        try:
            stmt = select(XtbRoleModel.engname).where(XtbRoleModel.md5.in_(md5_list))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询]{e}")

    @classmethod
    async def get_model_by_engname_list(
            cls, db: AsyncSession, engname_list: List
    ) -> Optional[List]:
        try:
            stmt = select(XtbRoleModel).where(XtbRoleModel.engname.in_(engname_list))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询]{e}")

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
            cls, db: AsyncSession, md5_list: List[str]
    ) -> None:
        try:
            stmt = delete(XtbRoleModel).where(XtbRoleModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbRoleModel).where(XtbRoleModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
