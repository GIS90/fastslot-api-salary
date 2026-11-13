# -*- coding: utf-8 -*-
"""用户头像收藏及头像超市数据操作。"""
from typing import Optional, List

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.schema.dao.xtb_user_avatar import XtbUserAvatarModel
from deploy.schema.dao.xtb_user_avatar_favorite import XtbUserAvatarFavoriteModel
from deploy.utils.exception import SQLDBHandleException


__all__ = ["XtbUserAvatarFavoriteCurd"]


class XtbUserAvatarFavoriteCurd:

    @staticmethod
    async def new_model() -> XtbUserAvatarFavoriteModel:
        return XtbUserAvatarFavoriteModel()

    async def get_by_user_avatar(
        self, db: AsyncSession, rtx_id: str, avatar_md5: str
    ) -> Optional[XtbUserAvatarFavoriteModel]:
        try:
            stmt = select(XtbUserAvatarFavoriteModel).where(
                XtbUserAvatarFavoriteModel.rtx_id == rtx_id,
                XtbUserAvatarFavoriteModel.avatar_md5 == avatar_md5,
            )
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise SQLDBHandleException(f"[{self.__class__.__name__}*查询收藏]{e}")

    @classmethod
    async def market_pagination(
        cls,
        db: AsyncSession,
        rtx_id: str,
        offset: int = 0,
        limit: int = 24,
        type_: str = None,
        favorite_status: int = None,
        sort_: str = None,
        content: str = None,
    ) -> List:
        try:
            join_condition = and_(
                XtbUserAvatarFavoriteModel.avatar_md5 == XtbUserAvatarModel.md5,
                XtbUserAvatarFavoriteModel.rtx_id == rtx_id,
                XtbUserAvatarFavoriteModel.status != True,
            )
            stmt = select(
                XtbUserAvatarModel.md5,
                XtbUserAvatarModel.name,
                XtbUserAvatarModel.url,
                XtbUserAvatarModel.type,
                XtbUserAvatarModel.summary,
                XtbUserAvatarModel.tag,
                XtbUserAvatarModel.count,
                XtbUserAvatarModel.favorite.label("favorite_count"),
                XtbUserAvatarFavoriteModel.id.is_not(None).label("favorite"),
            ).outerjoin(
                XtbUserAvatarFavoriteModel, join_condition
            ).where(
                XtbUserAvatarModel.status != True,
                XtbUserAvatarModel.lock != True,
            )
            if type_:
                stmt = stmt.where(XtbUserAvatarModel.type == type_)
            if content:
                like_value = f"%{content}%"
                stmt = stmt.where(or_(
                    XtbUserAvatarModel.name.like(like_value),
                    XtbUserAvatarModel.tag.like(like_value),
                    XtbUserAvatarModel.summary.like(like_value),
                ))
            if favorite_status == 1:
                stmt = stmt.where(XtbUserAvatarFavoriteModel.id.is_not(None))
            elif favorite_status == 0:
                stmt = stmt.where(XtbUserAvatarFavoriteModel.id.is_(None))
            if sort_ == "count":
                order_by = [desc(XtbUserAvatarModel.count), desc(XtbUserAvatarModel.create_time)]
            elif sort_ == "favorite":
                order_by = [desc(XtbUserAvatarModel.favorite), desc(XtbUserAvatarModel.create_time)]
            else:
                order_by = [desc(XtbUserAvatarModel.create_time), desc(XtbUserAvatarModel.id)]
            stmt = stmt.order_by(*order_by).offset(offset).limit(limit)
            result = await db.execute(stmt)
            return result.mappings().all()
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*头像超市列表]{e}")

    @classmethod
    async def market_count(
        cls,
        db: AsyncSession,
        rtx_id: str,
        type_: str = None,
        favorite_status: int = None,
        content: str = None,
    ) -> int:
        try:
            join_condition = and_(
                XtbUserAvatarFavoriteModel.avatar_md5 == XtbUserAvatarModel.md5,
                XtbUserAvatarFavoriteModel.rtx_id == rtx_id,
                XtbUserAvatarFavoriteModel.status != True,
            )
            stmt = select(func.count(XtbUserAvatarModel.id)).outerjoin(
                XtbUserAvatarFavoriteModel, join_condition
            ).where(
                XtbUserAvatarModel.status != True,
                XtbUserAvatarModel.lock != True,
            )
            if type_:
                stmt = stmt.where(XtbUserAvatarModel.type == type_)
            if content:
                like_value = f"%{content}%"
                stmt = stmt.where(or_(
                    XtbUserAvatarModel.name.like(like_value),
                    XtbUserAvatarModel.tag.like(like_value),
                    XtbUserAvatarModel.summary.like(like_value),
                ))
            if favorite_status == 1:
                stmt = stmt.where(XtbUserAvatarFavoriteModel.id.is_not(None))
            elif favorite_status == 0:
                stmt = stmt.where(XtbUserAvatarFavoriteModel.id.is_(None))
            result = await db.execute(stmt)
            return result.scalar() or 0
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*头像超市总数]{e}")

    @classmethod
    async def add(cls, db: AsyncSession, model: XtbUserAvatarFavoriteModel) -> None:
        try:
            db.add(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*新增收藏]{e}")

    @classmethod
    async def update(cls, db: AsyncSession, model: XtbUserAvatarFavoriteModel) -> None:
        try:
            await db.merge(model)
        except Exception as e:
            raise SQLDBHandleException(f"[{cls.__name__}*更新收藏]{e}")
