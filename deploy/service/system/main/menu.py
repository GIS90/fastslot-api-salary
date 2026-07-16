# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>menu service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/5/6 21:06
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = menu.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from itertools import groupby
from datetime import datetime
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.xtb_menu import XtbMenuCurd
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.service.system.config.enum_value import SystemConfigEnumVService
from deploy.schema.dao.xtb_menu import XtbMenuModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import menu_converter_dict, option_converter_dict
from deploy.utils.utils import get_now, d2s, md5 as generator_md5, build_menu_tree_iterative
from deploy.config import menu_root as MENU_ROOT_ID
from deploy.utils.enumeration import CsbEnumKEY


class SystemMainMenuService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemMainMenuService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_menu_curd: XtbMenuCurd = XtbMenuCurd()
        self.csb_ev_curd: CsbEnumValueCurd = CsbEnumValueCurd()
        self.system_config_ev_service: SystemConfigEnumVService = SystemConfigEnumVService(db_connection=db_connection)

    def __str__(self):
        return "SystemMainMenuService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: Literal["base", "list", "detail", "all"] = "detail" ,
            format_: Literal["tree", "flat"] = "flat" ,
            root_check: bool = False
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbMenuModel = await self.xtb_menu_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if root_check and getattr(model, "id", None) == MENU_ROOT_ID:
            return False, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="菜单根节点不允许操作")

        return (True, model if response_type == "model"
                        else await menu_converter_dict(model=model, type_=fields, format_=format_))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        all_menus = await self.xtb_menu_curd.get_all(db=self.db, root=False)
        if not all_menus:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA)

        auth_menu_list = []
        for menu in all_menus:
            # lose menu information
            if not menu or getattr(menu, "status"): continue
            _menu_d = await menu_converter_dict(menu, type_="detail", format_="flat")
            if not _menu_d: continue
            auth_menu_list.append(_menu_d)  # 管理角色菜单权限

        tree_menu_list = build_menu_tree_iterative(flat_menus=auth_menu_list, root_id=MENU_ROOT_ID, id_key="id", parent_key="pid", children_key="children")
        return SuccessStatus(data=tree_menu_list)

    async def _get_menu_group_option(self, root: bool = True):
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        # Group Option格式菜单
        all_menus = await self.xtb_menu_curd.get_all(db=self.db, root=root)
        all_menu_list: List = []
        for menu in all_menus:
            # lose menu information
            if not menu or getattr(menu, "status"): continue

            _menu_d: Dict = await menu_converter_dict(model=menu, type_="detail", format_="flat")
            if not _menu_d: continue
            all_menu_list.append({
                "value": _menu_d.get("id"),
                "label": _menu_d.get("title"),
                "name": _menu_d.get("name"),
                "group": _menu_d.get("level")
            })
        all_menu_group_list: List = []
        __MENU_LEVEL_ENUM: Dict = await self.system_config_ev_service.enum_by_name(
            name=CsbEnumKEY.MENU_LEVEL.value,
            key_trans_int=False,
            response_="dict",
            filter_lock=False
        )
        if all_menu_list:
            all_menu_list_sorted = sorted(all_menu_list, key=lambda x: x.get("group"))
            for key, group in groupby(all_menu_list_sorted, key=lambda x: x.get("group")):
                all_menu_group_list.append({
                    "label": __MENU_LEVEL_ENUM.get(str(key)) or "菜单级别",
                    "options": list(group)
                })
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        return all_menu_group_list

    async def _get_csb_enum_option(
            self,
            key: str,
            key_trans_int: bool = False,
            filter_lock: bool = True,
            lock_view: bool = False
    ):
        """
        用户性别枚举值
        :return: list
        """
        if not key:return []
        _res = await self.csb_ev_curd.get_list_by_name(db=self.db, name=key, filter_lock=filter_lock)
        return await option_converter_dict(models=_res, key_trans_int=key_trans_int, lock_view=lock_view) if _res else []

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields="detail",
            format_="flat",
            root_check=False
        )
        if not __flag: return data
        __res: Dict = {
                "menu": data,
                "menuOption": await self._get_menu_group_option(root=True),
                "menuType": await self.system_config_ev_service.enum_by_name(
                    name=CsbEnumKEY.MENU_TYPE.value, response_="option", filter_lock=False, key_trans_int=False
                ),
                "menuLevel": await self.system_config_ev_service.enum_by_name(
                    name=CsbEnumKEY.MENU_LEVEL.value, response_="option", filter_lock=True, key_trans_int=True
                )
            }
        return SuccessStatus(data=__res)

    async def add_enum(self, rtx_id: str) -> Status:
        data: Dict = {
            "menuOption": await self._get_menu_group_option(root=True),
            "menuType": await self.system_config_ev_service.enum_by_name(
                name=CsbEnumKEY.MENU_TYPE.value, response_="option", filter_lock=False, key_trans_int=False
            ),
            "menuLevel": await self.system_config_ev_service.enum_by_name(
                name=CsbEnumKEY.MENU_LEVEL.value, response_="option", filter_lock=True, key_trans_int=True
            )
        }
        return SuccessStatus(data=data)

    async def add(self, rtx_id: str, model: Dict) -> Status:
        # 验证角色名称是否已存在
        db_model: XtbMenuModel = await self.xtb_menu_curd.get_by_name(
            db=self.db,
            name=model.get("name"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="菜单名称已存在，请更换")

        # 新增角色
        new_model: XtbMenuModel = await self.xtb_menu_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('name')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        model["cache"] = model.get("isKeepAlive")
        del model["isKeepAlive"]
        model["affix"] = model.get("isAffix")
        del model["isAffix"]
        model["full"] = model.get("isFull")
        del model["isFull"]
        model["breadcrumb"] = model.get("isBreadcrumb")
        del model["isBreadcrumb"]
        model["hidden"] = model.get("isHide")
        del model["isHide"]
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_menu_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5_id=_md5, status_check=False, response_type="model", root_check=False
        )
        if not __flag: return data

        del model["md5"]
        del model["id"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        model["cache"] = model.get("isKeepAlive")
        del model["isKeepAlive"]
        model["affix"] = model.get("isAffix")
        del model["isAffix"]
        model["full"] = model.get("isFull")
        del model["isFull"]
        model["breadcrumb"] = model.get("isBreadcrumb")
        del model["isBreadcrumb"]
        model["hidden"] = model.get("isHide")
        del model["isHide"]
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_menu_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", root_check=True
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_menu_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def status(self, rtx_id: str, md5: str, value: bool) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", root_check=True
        )
        if not __flag: return data

        setattr(data, "hidden", value)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_menu_curd.update(db=self.db, model=data)
        return SuccessStatus()
