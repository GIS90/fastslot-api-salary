# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>main>role service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/4/2 23:29
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = role.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from datetime import datetime
from typing import Dict, List, Tuple, Literal, Any
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_role import XtbRoleCurd
from deploy.curd.xtb_menu import XtbMenuCurd
from deploy.schema.dao.xtb_role import XtbRoleModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict, menu_converter_dict
from deploy.schema.dto.xtb_role import xtb_role_list_fields, xtb_role_download_fields
from deploy.utils.utils import get_now, d2s, md5 as generator_md5, build_menu_tree_iterative
from deploy.config import server_role as SERVER_ROLE_ADMIN, menu_root as MENU_ROOT_ID


class SystemMainRoleService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemMainRoleService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_role_curd: XtbRoleCurd = XtbRoleCurd()
        self.xtb_menu_curd: XtbMenuCurd = XtbMenuCurd()

    def __str__(self):
        return "SystemMainRoleService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: List[Dict] = xtb_role_list_fields,
            admin_check: bool = False
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbRoleModel = await self.xtb_role_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if admin_check and getattr(model, "engname") == SERVER_ROLE_ADMIN:
            return False, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbRoleModel] = await self.xtb_role_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            content=params.get("content")
        )
        if not models:
            __data = {
                "list": [],
                "page": params.get("page"),
                "pageSize": params.get("limit"),
                "total": 0
            }
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA, data=__data)

        id_value: int = params.get("offset") + 1
        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_role_list_fields,
            auto_id=True,
            auto_id_value=id_value
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_role_curd.count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_role_list_fields,
            admin_check=False
        )
        return SuccessStatus(data=data) if __flag else data

    @staticmethod
    async def __converter_select_option(models: List) -> List:
        if not models: return []

        _res: List = []
        for item in models:
            if not item: continue
            if not getattr(item, "engname", None) or not getattr(item, "md5", None): continue
            _res.append({
                "label": item.chnname,
                "value": item.engname,
                "md5": item.md5,
                "desc": item.introduction})
        else:
            return _res

    async def role_select_option(self) -> List:
        models: List[XtbRoleModel] = await self.xtb_role_curd.get_all(
            db=self.db,
            filter_status=True
        )
        return await self.__converter_select_option(models) if models else []

    async def add(self, rtx_id: str, model: Dict) -> Status:
        # 验证角色名称是否已存在
        db_model: XtbRoleModel = await self.xtb_role_curd.get_by_engname(
            db=self.db,
            engname=model.get("engname"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="角色ID已存在，请更换")

        # 新增角色
        new_model: XtbRoleModel = await self.xtb_role_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('engname')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_role_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5_id=_md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_role_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_hard(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        await self.xtb_role_curd.delete(db=self.db, model=data)
        return SuccessStatus()

    async def delete_soft(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_role_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def __verify_contain_admin_role(self, md5_list: List) -> Tuple[bool, Any]:
        db_model: List = await self.xtb_role_curd.get_engname_by_md5_list(db=self.db, md5_list=md5_list)
        if db_model and SERVER_ROLE_ADMIN in db_model:
            return True, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="管理员角色不允许删除")
        else:
            return False, db_model

    async def batch_delete_hard(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_role(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_role_curd.batch_delete(db=self.db, md5_list=md5_list)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count-query_count}")

    async def batch_delete_soft(self, rtx_id: str, md5_list: List) -> Status:
        __flag, data = await self.__verify_contain_admin_role(md5_list)
        if __flag: return data
        query_count: int = len(data)
        request_count: int = len(md5_list)
        await self.xtb_role_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def download(self, params: dict) -> List:
        models = await self.xtb_role_curd.download(db=self.db, params=params)
        data: List = list()
        _id = 1
        for u in models:
            if not u: continue
            _d = await model_converter_dict(model=u, fields=xtb_role_download_fields)
            _d["序号"] = _id
            _id +=  1
            data.append(_d)
        return data

    async def auth(self, rtx_id: str, md5: str) -> Status:
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # >>>>>第一步：数据判断
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # >>>>>第二步：用户角色权限
        role_id = getattr(data, "engname")
        role_auth = getattr(data, "authority")
        role_auth_list = [] if not role_auth else role_auth.split(",")
        if role_id != SERVER_ROLE_ADMIN:
            __role_auth_list = [int(x) for x in role_auth_list]  # 菜单ID转整型
            role_auth_list = list(set(__role_auth_list))  # 去重

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # >>>>>第三步：用户菜单权限
        auth_menu_list = []  # 权限菜单
        admin_menu_list = []  # 管理角色菜单权限
        all_menus = await self.xtb_menu_curd.get_all(db=self.db, root=False)
        for menu in all_menus:
            # lose menu information
            if not menu or menu.status \
                    or menu.hidden:
                continue

            _d = await menu_converter_dict(model=menu, type_="detail", format_="flat")
            if not _d: continue
            admin_menu_list.append(int(_d.get("id")))   # 管理角色菜单权限

            # Tree数据格式
            _new_d = dict()
            _new_d["id"] = int(_d.get("id"))    # 整型
            _new_d["md5"] = _d.get("md5")
            _new_d["name"] = _d.get("name")
            _new_d["path"] = _d.get("path")
            _new_d["label"] = _d.get("title")
            _new_d["disabled"] = False
            _new_d["pid"] = int(_d.get("pid"))
            auth_menu_list.append(_new_d)   # 整型

        data = {
            "menu": build_menu_tree_iterative(flat_menus=auth_menu_list, root_id=MENU_ROOT_ID, id_key="id", parent_key="pid", children_key="children"),
            "checked": role_auth_list if role_id != SERVER_ROLE_ADMIN else admin_menu_list,
            "expanded": role_auth_list if role_id != SERVER_ROLE_ADMIN else []
        }
        return SuccessStatus(data=data)

    async def auth_update(self, rtx_id: str, model: Dict) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=model.get("md5"), status_check=True, response_type="model", admin_check=True
        )
        if not __flag: return data

        # 去重 + 格式化
        menu_ids = list(set([str(x) for x in model.get("id")]))
        menu_ids_str = ",".join(menu_ids)

        setattr(data, "authority", menu_ids_str)
        setattr(data, "update_rtx", rtx_id)
        setattr(data, "update_time", get_now())  
        await self.xtb_role_curd.update(db=self.db, model=data)
        return SuccessStatus()
