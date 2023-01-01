# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    model class              DB table               ZH DB table
    ------------------------------------------------------------------------
    XtbMenuModel             xtb_menu               系统表-菜单表

base_info:
    __author__ = PyGo
    __time__ = 2026/4/14 21:49
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
from sqlalchemy import (
        Column,
        String,
        Integer,
        Boolean,
        TIMESTAMP,
        Text
)
from deploy.schema._dao_base_model import baseModel
from sqlalchemy.orm import Mapped, mapped_column
from .common_field import IDField, Md5Field, CUDField, StatusField, OrderIdFiled
from typing import Optional

__all__ = ["XtbMenuModel"]


class XtbMenuModel(baseModel, IDField, Md5Field, CUDField, StatusField, OrderIdFiled):
    __tablename__ = 'xtb_menu'
    __table_args__ = ({'comment': '系统表-系统菜单表'})

    name: Mapped[str] = mapped_column(name="name", type_=String(55), comment="路由英文名称，大驼峰命名方式[注：需要与父节点连接映射]，例如SystemMenu")
    path: Mapped[str] = mapped_column(name="path", type_=String(255), comment="路由path，全小写字母[注：需要与父节点连接映射]")
    title: Mapped[str] = mapped_column(name="title", type_=String(35), comment="菜单标题")
    pid: Mapped[int] = mapped_column(name="pid", type_=Integer, comment="父ID")
    level: Mapped[int] = mapped_column(name="level", type_=Integer, default=1, comment="菜单级别，默认1级菜单，根节点为0")
    type: Mapped[str] = mapped_column(name="type", type_=String(35), default="MENU", comment="菜单类型：MENU=菜单，LINK=外链，BUTTON=按钮")
    component: Mapped[str] = mapped_column(name="component", type_=String(255), comment="路由组件，与Vue router mappings映射[注：需要与父节点连接映射]")
    hidden: Mapped[bool] = mapped_column(name="hidden", type_=Boolean(), default=False,comment="是否在SideBar显示，默认为false")
    redirect: Mapped[str] = mapped_column(name="redirect", type_=String(255), comment="菜单重定向，主要用于URL一级菜单跳转")
    icon: Mapped[str] = mapped_column(name="icon", type_=String(35), comment="菜单图标")
    cache: Mapped[bool] = mapped_column(name="cache", type_=Boolean(), default=True, comment="页面是否进行cache，默认true缓存")
    affix: Mapped[bool] = mapped_column(name="affix", type_=Boolean(), default=False, comment="是否在tags-view固定，默认false")
    full: Mapped[bool] = mapped_column(name="full", type_=Boolean(), default=False, comment="是否全屏，默认false")
    breadcrumb: Mapped[bool] = mapped_column(name="breadcrumb", default=True, type_=Boolean(), comment="是否Breadcrumb中显示，默认true")
    shortcut: Mapped[bool] = mapped_column(name="shortcut", type_=Boolean(), default=True, comment="Dashboard快捷入口是否显示，默认true")
    tag: Mapped[Optional[str]] = mapped_column(name="tag", type_=String(10), comment="菜单TAG")

    def __str__(self):
        return f"XtbMenuModel Class[DB table: xtb_menu], id: {self.id}, name: {self.name}, title: {self.title}."

    def __repr__(self):
        return self.__str__()

