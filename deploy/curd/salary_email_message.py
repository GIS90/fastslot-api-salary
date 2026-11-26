# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    salary_email_message curd

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = salary_email_message.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, desc, and_, func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.salary_email import SalaryEmailMessageModel
from deploy.utils.exception import SQLDBHandleException


class SalaryEmailMessageCurd(BaseCurd):

    @staticmethod
    async def new_model() -> SalaryEmailMessageModel:
        return SalaryEmailMessageModel()

    @staticmethod
    def _not_deleted():
        return SalaryEmailMessageModel.status != True

    @classmethod
    async def get_by_md5(cls, db: AsyncSession, md5: str) -> Optional[SalaryEmailMessageModel]:
        try:
            stmt = select(SalaryEmailMessageModel).where(SalaryEmailMessageModel.md5 == md5)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询One]{e}")

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            stmt = select(func.count(SalaryEmailMessageModel.id)).where(
                cls._not_deleted()
            )
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def pagination(
            cls, db: AsyncSession, offset: int = 0, limit: int = 15,
            content: Optional[str] = None, *args, **kwargs
    ) -> Optional[List[SalaryEmailMessageModel]]:
        try:
            stmt = select(SalaryEmailMessageModel).where(
                cls._not_deleted()
            )
            if content:
                stmt = stmt.where(SalaryEmailMessageModel.file_name.like("%%%s%%" % content))
            stmt = stmt.order_by(desc(SalaryEmailMessageModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(cls, db: AsyncSession, params: Dict, *args, **kwargs) -> Optional[List]:
        return await cls.list_all(db=db, md5_list=(params or {}).get("list"))

    @classmethod
    async def list_all(
            cls, db: AsyncSession, md5_list: Optional[List] = None
    ) -> Optional[List[SalaryEmailMessageModel]]:
        try:
            stmt = select(SalaryEmailMessageModel).where(
                cls._not_deleted()
            )
            if md5_list:
                stmt = stmt.where(SalaryEmailMessageModel.md5.in_(md5_list))
            stmt = stmt.order_by(desc(SalaryEmailMessageModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def add(cls, db: AsyncSession, model: SalaryEmailMessageModel) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(cls, db: AsyncSession, model: SalaryEmailMessageModel) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(cls, db: AsyncSession, model: SalaryEmailMessageModel) -> None:
        try:
            await db.delete(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*删除]{e}")

    @classmethod
    async def batch_soft_delete(cls, db: AsyncSession, md5_list: List[str], rtx_id: str) -> None:
        try:
            stmt = update(SalaryEmailMessageModel).where(
                and_(
                    SalaryEmailMessageModel.md5.in_(md5_list),
                    cls._not_deleted()
                )
            ).values(status=True, delete_rtx=rtx_id, delete_time=func.now())
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
