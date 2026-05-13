# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:57
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = user.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_user import XtbUserCurd
from deploy.curd.xtb_role import XtbRoleCurd
from deploy.curd.xtb_menu import XtbMenuCurd
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_menu import xtb_tree_detail_fields
from deploy.utils.utils import get_all_parent_ids_iterative, build_menu_tree_iterative, build_menu_tree_fci
from deploy.config import (server_user as SERVER_USER_ADMIN,
                           server_role as SERVER_ROLE_ADMIN,
                           menu_root as MENU_ROOT_ID)


class XUserService:

    __xtb_menu_tree_attrs = [
        'id', 'name', 'path', 'pid', 'level', 'md5', 'component', 'type', 'link', 'redirect', 'order_id',
        'title', 'icon', 'cache', 'affix', 'full', 'hidden', 'tag', 'breadcrumb'
    ]

    def __init__(self, db_connection: AsyncSession):
        """
        XUserService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_curd: XtbUserCurd = XtbUserCurd()
        self.xtb_role_curd: XtbRoleCurd = XtbRoleCurd()
        self.xtb_menu_curd: XtbMenuCurd = XtbMenuCurd()

    def __str__(self):
        return "XUserService class."

    def __repr__(self):
        return self.__str__()

    @staticmethod
    async def __contain_admin_role(roles: list) -> bool:
        return SERVER_ROLE_ADMIN in roles

    async def __xtb_menu_model_to_tree_dict(self, model) -> Dict:
        if not model:
            return {}

        _res = dict()
        _meta = dict()
        for attr in self.__xtb_menu_tree_attrs:
            if attr == 'id':
                _res[attr] = model.id
            elif attr == 'name':
                _res[attr] = model.name
            elif attr == 'path':
                _res[attr] = model.path
            elif attr == 'pid':
                _res[attr] = model.pid
            elif attr == 'level':
                _res[attr] = model.level
            elif attr == 'md5':
                _res[attr] = model.md5
            elif attr == 'order_id':
                _res[attr] = model.order_id
            elif attr == 'component':
                _res[attr] = model.component
            elif attr == 'redirect':
                _res[attr] = model.redirect
            # * * * * * * * * * * * * * * * * * * * * * * * *
            elif attr == 'type':
                # 此菜单类型，MENU=菜单，LINK=外链，BUTTON=按钮
                _meta[attr] = model.type or "MENU"
            elif attr == 'title':
                # 菜单标题
                _meta[attr] = model.title
            elif attr == 'icon':
                # 菜单图标
                _meta[attr] = model.icon
            elif attr == 'cache':
                # 是否缓存路由
                _meta["isKeepAlive"] = True if model.cache else False
            elif attr == 'affix':
                # 菜单是否固定在标签页中 (首页通常是固定项)
                _meta["isAffix"] = True if model.affix else False
            elif attr == 'full':
                # 菜单是否全屏 (示例：数据大屏页面)
                _meta["isFull"] = True if model.full else False
            elif attr == 'hidden':
                # 是否在菜单中隐藏
                _meta["isHide"] = True if model.hidden else False
            elif attr == 'breadcrumb':
                # 是否在面包屑菜单中显示
                _meta["isBreadcrumb"] = True if model.breadcrumb else False
            elif attr == 'tag':
                _meta[attr] = model.tag
            # * * * * * * * * * * * * * * * * * * * * * * * *
        else:
            _res['meta'] = _meta
            return _res

    async def auth(self, token_rtx_id: str) -> Status:
        """
        用户系统菜单权限
        :param token_rtx_id: token_rtx_id
        :return: [dict]status model
        """
        # >>>>>第一步：用户信息
        user_model = await self.xtb_user_curd.get_by_rtx_id(db=self.db, rtx_id=token_rtx_id)
        if not user_model:
            return FailureStatus(
                code=status_code.CODE_202_LOGIN_USER_NO_REGISTER.value)
        if getattr(user_model, "status"):
            return FailureStatus(
                code=status_code.CODE_203_LOGIN_USER_OFF.value)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # >>>>>第二步：用户角色
        user_model_roles = [] if not getattr(user_model, "role") else str(user_model.role).split(";")
        # 非管理员角色，未分配权限
        if getattr(user_model, "rtx_id") != SERVER_USER_ADMIN and not user_model_roles:
            return FailureStatus(
                code=status_code.CODE_208_USER_MENU_INVALID.value)
        user_role_admin = await self.__contain_admin_role(user_model_roles)  # 是否包含管理员角色权限
        if getattr(user_model, "rtx_id") == SERVER_USER_ADMIN: user_role_admin = True  # 管理员
        auth_menu_ids = []  # 权限菜单
        if not user_role_admin:
            # >> 非管理员用户
            user_role = await self.xtb_role_curd.get_model_by_engname_list(
                db=self.db,
                engname_list=user_model_roles
            )  # 多角色
            for r in user_role:
                if not r or not getattr(r, "authority"): continue
                auth_menu_ids += [int(x) for x in str(r.authority).split(";")]  # 菜单ID转整型
            auth_menu_ids = list(set(auth_menu_ids))  # 去重

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # >>>>>第三步：用户菜单权限
        auth_menu_list = []  # 权限菜单
        all_menus = await self.xtb_menu_curd.get_all(db=self.db, root=False)
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        # 特殊处理：因为在el-tree存储树节点的id，如果为子节点为半选状态，那么父节点为全选状态，
        #    因此，获取角色权限id的父节点ID加入到权限中
        # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
        _all_menus_dict_list = list()  # 菜单字典列表
        for menu in all_menus:
            # lose menu information
            if not menu \
                    or getattr(menu, "status") \
                    or getattr(menu, "hidden"):
                continue

            _d = await self.__xtb_menu_model_to_tree_dict(model=menu)
            if not _d: continue
            _all_menus_dict_list.append(_d)

        if not user_role_admin:
            # 递归查找父节点
            menu_ids = get_all_parent_ids_iterative(
                flat_menus=_all_menus_dict_list,
                permission_ids=auth_menu_ids,
                id_key="id",
                parent_key="pid"
            )

            for _m in _all_menus_dict_list:
                if _m.get("id") in menu_ids:
                    auth_menu_list.append(_m)

        """
        方式：
          1、递归
          2、For循环，公共方法
        """
        __menu = auth_menu_list if not user_role_admin else _all_menus_dict_list
        # menus_tree = build_menu_tree_fci(flat_menus=menu, parent_id=MENU_ROOT_ID, id_key="id", parent_key="pid", children_key="children")   # 方式一
        menus_tree = build_menu_tree_iterative(flat_menus=__menu, root_id=MENU_ROOT_ID, id_key="id", parent_key="pid", children_key="children")  # 方式二
        return SuccessStatus(data={"menu": menus_tree})
