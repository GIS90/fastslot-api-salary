# -*- coding: utf-8 -*-
"""用户头像收藏表模型。"""
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from deploy.schema._dao_base_model import baseModel
from .common_field import IDField, Md5Field, CUDField, StatusField


__all__ = ["XtbUserAvatarFavoriteModel"]


class XtbUserAvatarFavoriteModel(baseModel, IDField, Md5Field, CUDField, StatusField):
    __tablename__ = "xtb_user_avatar_favorite"
    __table_args__ = (
        UniqueConstraint("rtx_id", "avatar_md5", name="uq_user_avatar_favorite"),
        {"comment": "系统表-用户头像收藏表"},
    )

    rtx_id: Mapped[str] = mapped_column(name="rtx_id", type_=String(35), nullable=False, comment="收藏用户RTX-ID")
    avatar_md5: Mapped[str] = mapped_column(name="avatar_md5", type_=String(64), nullable=False, comment="头像MD5-ID")

    def __str__(self):
        return f"XtbUserAvatarFavoriteModel[id={self.id}, rtx_id={self.rtx_id}, avatar_md5={self.avatar_md5}]"
