# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    csb_enum_value curd
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/26 22:33
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = csb_enum_value.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Optional, List, Any, Union, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, asc, desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import func

from deploy.curd.base_curd import BaseCurd
from deploy.schema.dao.csb_enum_value import CsbEnumValueModel
from deploy.utils.exception import SQLDBHandleException
from deploy.utils.enumeration import DICT_KEY_ALL


class CsbEnumValueCurd(BaseCurd):

    @staticmethod
    async def new_model():
        return CsbEnumValueModel()

    async def _get_model_by_field(
        self,
        db: AsyncSession,
        field: str | InstrumentedAttribute,
        value: Any,
        filter_lock: bool = False
    ) -> Optional[CsbEnumValueModel]:
        try:
            if isinstance(field, str):
                if not hasattr(CsbEnumValueModel, field):
                    return None
                _field = getattr(CsbEnumValueModel, field)
            else:
                _field = field

            stmt = select(CsbEnumValueModel).where(
                _field == value,
                CsbEnumValueModel.status != 1)
            if filter_lock:
                stmt = stmt.where(CsbEnumValueModel.lock != True)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    async def get_by_id(self, db: AsyncSession, _id: int, filter_lock: bool = False) -> Optional[CsbEnumValueModel]:
        return await self._get_model_by_field(db, CsbEnumValueModel.id, _id, filter_lock)

    async def get_by_md5(self, db: AsyncSession, md5: str,filter_lock: bool = False) -> Optional[CsbEnumValueModel]:
        return await self._get_model_by_field(db, CsbEnumValueModel.md5, md5, filter_lock)

    async def get_by_key_name(self, db: AsyncSession, key: str, name: str) -> Optional[CsbEnumValueModel]:
        try:
            stmt = select(CsbEnumValueModel).where(
                CsbEnumValueModel.name == name,
                CsbEnumValueModel.key == key,
                CsbEnumValueModel.status != 1)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询One]{e}")

    @classmethod
    async def get_list_by_name(
            cls,
            db: AsyncSession,
            name: str,
            filter_lock: bool = False
    ) -> Union[List, None]:
        try:
            stmt = select(CsbEnumValueModel).where(
                CsbEnumValueModel.name == name,
                CsbEnumValueModel.status != 1)
            if filter_lock:
                stmt = stmt.where(CsbEnumValueModel.lock != True)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询Many]{e}")

    @classmethod
    async def get_list_by_names(
            cls,
            db: AsyncSession,
            name_list: List[str],
            filter_lock: bool = False
    ) -> Union[List, None]:
        try:
            stmt = select(CsbEnumValueModel).where(
                CsbEnumValueModel.name.in_(name_list),
                CsbEnumValueModel.status != 1)
            if filter_lock:
                stmt = stmt.where(CsbEnumValueModel.lock != True)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询Many]{e}")

    @classmethod
    async def count(cls, db: AsyncSession, name: str = None, filter_lock: bool = False) -> int:
        try:
            stmt = select(func.count(CsbEnumValueModel.id)).where(CsbEnumValueModel.status != 1)
            if name and name != DICT_KEY_ALL.key:
                stmt = stmt.where(CsbEnumValueModel.name == name)
            if filter_lock:
                stmt = stmt.where(CsbEnumValueModel.lock != 1)
            result = await db.execute(stmt)
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*总数]{e}")

    @classmethod
    async def pagination(
        cls,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 15,
        name: str = None,
        filter_lock: bool = False
    ) -> Optional[List]:
        try:
            stmt = select(CsbEnumValueModel).where(CsbEnumValueModel.status != 1)
            if name and name != DICT_KEY_ALL.key:
                stmt = stmt.where(CsbEnumValueModel.name == name)
            if filter_lock:
                stmt = stmt.where(CsbEnumValueModel.lock != 1)
            stmt = stmt.order_by(
                asc(CsbEnumValueModel.name),
                asc(CsbEnumValueModel.order_id),
                desc(CsbEnumValueModel.id)
            ).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询All]{e}")

    @classmethod
    async def count_by_md5_list(cls, db: AsyncSession, md5_list: List[str]) -> int:
        try:
            result = await db.execute(
                select(func.count(CsbEnumValueModel.id)).where(
                    CsbEnumValueModel.status != 1,
                    CsbEnumValueModel.md5.in_(md5_list)
                )
            )
            return result.scalar()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*查询总数]{e}")

    @classmethod
    async def download(
            cls, db: AsyncSession, params: Dict, *args, **kwargs
    ) -> Optional[List]:
        ...

    @classmethod
    async def add(
            cls, db: AsyncSession, model: CsbEnumValueModel
    ) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增]{e}")

    @classmethod
    async def update(
            cls, db: AsyncSession, model: CsbEnumValueModel
    ) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新]{e}")

    @classmethod
    async def delete(
            cls, db: AsyncSession, model: CsbEnumValueModel
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
            stmt = delete(CsbEnumValueModel).where(CsbEnumValueModel.md5.in_(md5_list))
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量删除]{e}")

    @classmethod
    async def batch_soft_delete_update(
            cls, db: AsyncSession, md5_list: List[str], rtx_id: str
    ) -> None:
        try:
            stmt = update(CsbEnumValueModel).where(CsbEnumValueModel.md5.in_(md5_list)).values(
                status = True,
                delete_rtx = rtx_id,
                delete_time = func.now(),
            )
            await db.execute(stmt)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*批量更新]{e}")
