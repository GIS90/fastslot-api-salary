# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>ops>depart service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/7/17 00:50
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = depart.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_department import XtbDepartmentCurd
from deploy.schema.dao.xtb_department import XtbDepartmentModel
from deploy.service.system.config.enum_value import SystemConfigEnumVService
from deploy.service.system.main.user import SystemMainUserService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict
from deploy.schema.dto.xtb_department import xtb_depart_tree_fields
from deploy.utils.utils import get_now, build_menu_tree_iterative, flatten_tree_recursive
from deploy.utils.enumeration import CsbEnumKEY
from deploy.config import depart_root as DEPART_ROOT_ID, depart_root_pid as DEPART_ROOT_PID


class SystemOpsDepartService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemOpsDepartService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_department_curd: XtbDepartmentCurd = XtbDepartmentCurd()
        self.system_config_ev_service: SystemConfigEnumVService = SystemConfigEnumVService(db_connection=self.db)
        self.system_main_user_service: SystemMainUserService = SystemMainUserService(db_connection=self.db)

    def __str__(self):
        return "SystemOpsDepartService class."

    def __repr__(self):
        return self.__str__()

    async def __depart_format(self, type_: Literal["flat", "tree"] = "tree"):
        models = await self.xtb_department_curd.get_all(db=self.db, root=True, filter_status=True)
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        _res: List = []       # 全部数据
        expand: List = []     # 默认展开
        check: List = []      # 默认选中
        for model in models:
            if not model: continue
            model_dict = await model_converter_dict(model=model, fields=xtb_depart_tree_fields)
            if model_dict: _res.append(model_dict)
            # 默认展开根节点
            if model_dict.get("id") == DEPART_ROOT_ID: expand.append(model_dict.get("md5"))

        print('-' * 100)
        print(_res)
        tree = build_menu_tree_iterative(flat_menus=_res, root_id=DEPART_ROOT_PID, id_key="id", parent_key="pid", children_key="children")
        print(tree)
        if type_ == "flat":
            tree = flatten_tree_recursive(tree_data=tree)
        return tree, expand, check


    async def tree(self, rtx_id: str) -> Status:
        tree, expand, check = await self.__depart_format(type_="tree")
        print("*" * 100)
        print(tree, expand, check)
        return SuccessStatus(data={"data": tree, "expand": expand, "check": check})