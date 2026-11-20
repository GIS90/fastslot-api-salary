# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    salary_dtalk_robot curd

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = salary_dtalk_robot.py

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
from sqlalchemy import select, update, delete, asc, and_, func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.salary_dtalk import SalaryDtalkRobotModel
from deploy.utils.exception import SQLDBHandleException


class SalaryDtalkRobotCurd(BaseCurd):

    @staticmethod
    async def new_model() -> SalaryDtalkRobotModel:
        return SalaryDtalkRobotModel()

    @classmethod
    async def get_by_md5(cls, db: AsyncSession, md5: str) -> Optional[SalaryDtalkRobotModel]:
        try:
            stmt = select(SalaryDtalkRobotModel).where(SalaryDtalkRobotModel.md5 == md5)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询One]{e}")

    @classmethod
    async def get_by_key_secret(
            cls, db: AsyncSession, key: str, secret: str, agent_id: str = ""
    ) -> Optional[SalaryDtalkRobotModel]:
        try:
            conditions = [
                SalaryDtalkRobotModel.key == key,
                SalaryDtalkRobotModel.secret == secret,
                SalaryDtalkRobotModel.status.is_(False)
            ]
            if agent_id:
                conditions.append(SalaryDtalkRobotModel.agent_id == agent_id)
            stmt = select(SalaryDtalkRobotModel).where(and_(*conditions))
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询One]{e}")

    @classmethod
    async def count(cls, db: AsyncSession) -> int:
        try:
            stmt = select(func.count(SalaryDtalkRobotModel.id)).where(
                SalaryDtalkRobotModel.status.is_(False)
            )
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def pagination(
            cls, db: AsyncSession, offset: int = 0, limit: int = 15, *args, **kwargs
    ) -> Optional[List[SalaryDtalkRobotModel]]:
        try:
            stmt = select(SalaryDtalkRobotModel).where(
                SalaryDtalkRobotModel.status.is_(False)
            ).order_by(asc(SalaryDtalkRobotModel.create_time)).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def download(cls, db: AsyncSession, params: Dict, *args, **kwargs) -> Optional[List]:
        return await cls.option(db=db)

    @classmethod
    async def option(cls, db: AsyncSession) -> Optional[List[SalaryDtalkRobotModel]]:
        try:
            stmt = select(SalaryDtalkRobotModel).where(
                SalaryDtalkRobotModel.status.is_(False)
            ).order_by(asc(SalaryDtalkRobotModel.create_time))
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def clear_select(cls, db: AsyncSession) -> None:
        try:
            stmt = update(SalaryDtalkRobotModel).where(
                SalaryDtalkRobotModel.select.is_(True)
            ).values(select=False)
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")

    @classmethod
    async def add(cls, db: AsyncSession, model: SalaryDtalkRobotModel) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(cls, db: AsyncSession, model: SalaryDtalkRobotModel) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(cls, db: AsyncSession, model: SalaryDtalkRobotModel) -> None:
        try:
            await db.delete(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*删除]{e}")

    @classmethod
    async def batch_soft_delete(cls, db: AsyncSession, md5_list: List[str], rtx_id: str) -> None:
        try:
            stmt = update(SalaryDtalkRobotModel).where(
                and_(
                    SalaryDtalkRobotModel.md5.in_(md5_list),
                    SalaryDtalkRobotModel.status.is_(False)
                )
            ).values(status=True, delete_rtx=rtx_id, delete_time=func.now())
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
