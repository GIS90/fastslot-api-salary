# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    xtb_user curd

base_info:
    __author__ = PyGo
    __time__ = 2025/12/9 22:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = xtb_user.py

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
from sqlalchemy import select, update, delete, insert, asc, or_
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.xtb_user import XtbUserModel
from deploy.schema.dao.csb_enum_value import CsbEnumValueModel
from deploy.utils.exception import SQLDBHandleException


class XtbUserCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return XtbUserModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any
    ) -> Optional[XtbUserModel]:
        try:
            if isinstance(field, str):
                if not hasattr(XtbUserModel, field):
                    return None
                _field = getattr(XtbUserModel, field)
            else:
                _field = field

            result = await db.execute(select(XtbUserModel).where(_field == value))
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int):
        return await self._get_model_by_field(db, XtbUserModel.id, _id)

    async def get_by_rtx_id(self, db: AsyncSession, rtx_id: str):
        return await self._get_model_by_field(db, XtbUserModel.rtx_id, rtx_id)

    async def get_by_md5(self, db: AsyncSession, md5: str):
        return await self._get_model_by_field(db, XtbUserModel.md5, md5)

    async def get_by_name(self, db: AsyncSession, name: str):
        return await self._get_model_by_field(db, XtbUserModel.name, name)

    async def get_by_email(self, db: AsyncSession, email: str):
        return await self._get_model_by_field(db, XtbUserModel.email, email)

    async def get_by_phone(self, db: AsyncSession, phone: str):
        return await self._get_model_by_field(db, XtbUserModel.phone, phone)

    @classmethod
    async def get_count(cls, db: AsyncSession) -> int:
        try:
            result = await db.execute(
                select(func.count(XtbUserModel.id))
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def get_pagination(
        cls, db: AsyncSession, offset: int = 0, limit: int = 15, content: str = None, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(
                XtbUserModel.id,
                XtbUserModel.rtx_id,
                XtbUserModel.md5,
                XtbUserModel.name,
                CsbEnumValueModel.value.label("sex"),
                XtbUserModel.phone,
                XtbUserModel.email,
                XtbUserModel.avatar,
                XtbUserModel.introduction,
                XtbUserModel.department,
                XtbUserModel.create_rtx,
                XtbUserModel.create_time,
                XtbUserModel.status
            ).outerjoin(
                CsbEnumValueModel,
                XtbUserModel.sex == CsbEnumValueModel.key
            )
            if content:
                stmt = stmt.where(
                    or_(
                        XtbUserModel.rtx_id.like(content),
                        XtbUserModel.name.like(content),
                        XtbUserModel.phone.like(content),
                        XtbUserModel.email.like(content),
                        XtbUserModel.introduction.like(content)
                    )
                )
            stmt = stmt.order_by(asc(XtbUserModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(
        cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        try:
            stmt = select(
                XtbUserModel.id,
                XtbUserModel.rtx_id,
                XtbUserModel.name,
                CsbEnumValueModel.value.label("sex"),
                XtbUserModel.phone,
                XtbUserModel.email,
                XtbUserModel.avatar,
                XtbUserModel.introduction,
                XtbUserModel.role,
                XtbUserModel.department,
                XtbUserModel.create_rtx,
                XtbUserModel.create_time,
                XtbUserModel.status
            ).outerjoin(
                CsbEnumValueModel,
                XtbUserModel.sex == CsbEnumValueModel.key
            )
            if params.get("list"):
                stmt = stmt.where(XtbUserModel.md5.in_(params.get("list")))
            stmt = stmt.order_by(asc(XtbUserModel.create_time))
            result = await db.execute(stmt)
            return result.all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*下载]{e}")

    @classmethod
    async def get_rtx_by_md5_list(
        cls, db: AsyncSession, md5_list: List
    ) -> Optional[List]:
        try:
            stmt = select(XtbUserModel.rtx_id).where(XtbUserModel.md5.in_(md5_list))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询]{e}")

    @classmethod
    async def add(
            cls, db: AsyncSession, model: XtbUserModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: XtbUserModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: XtbUserModel
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
            stmt = delete(XtbUserModel).where(XtbUserModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(XtbUserModel).where(XtbUserModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
