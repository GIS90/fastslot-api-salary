# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    curd of table xtb_user_avatar

base_info:
    __author__ = PyGo
    __time__ = 2026/11/06 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user_avatar.py

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
from deploy.schema.dao.xtb_user_avatar import XtbUserAvatarModel
from deploy.utils.exception import SQLDBHandleException


__all__ = ["XtbUserAvatarCurd"]


class XtbUserAvatarCurd(BaseCurd):
    """
    头像表数据操作
    """

    @staticmethod
    async def new_model() -> XtbUserAvatarModel:
        return XtbUserAvatarModel()

    @staticmethod
    def _not_deleted():
        return XtbUserAvatarModel.delete_time.is_(None)

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbUserAvatarModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbUserAvatarModel, field):
                    return None
                _field = getattr(XtbUserAvatarModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbUserAvatarModel).where(
                _field == value,
                self._not_deleted()
            ))
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int):
        return await self._get_model_by_field(db, XtbUserAvatarModel.id, _id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbUserAvatarModel.md5, md5)

    async def get_by_name(self, db: AsyncSession, name: str):
        return await self._get_model_by_field(db, XtbUserAvatarModel.name, name)

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbUserAvatarModel.id)).where(cls._not_deleted())
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, content: str = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbUserAvatarModel).where(cls._not_deleted())
            if content:
                stmt = stmt.where(
                    or_(
                        XtbUserAvatarModel.name.like(content),
                        XtbUserAvatarModel.type.like(content),
                        XtbUserAvatarModel.tag.like(content),
                        XtbUserAvatarModel.summary.like(content)
                    )
                )
            stmt = stmt.order_by(desc(XtbUserAvatarModel.create_time), desc(XtbUserAvatarModel.id)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(XtbUserAvatarModel).where(cls._not_deleted())
            if params.get("list"):
                stmt = stmt.where(XtbUserAvatarModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(desc(XtbUserAvatarModel.create_time), desc(XtbUserAvatarModel.id))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def get_models_by_md5_list(
            cls, db: AsyncSession, md5_list: List
    ) -> Optional[List]:
        try:
            stmt = select(XtbUserAvatarModel).where(
                XtbUserAvatarModel.md5.in_(md5_list),
                cls._not_deleted()
            )
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbUserAvatarModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbUserAvatarModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbUserAvatarModel
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
            stmt = delete(XtbUserAvatarModel).where(XtbUserAvatarModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbUserAvatarModel).where(XtbUserAvatarModel.md5.in_(md5_list)).values(
                status=True,
                delete_rtx=rtx_id,
                delete_time=func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
