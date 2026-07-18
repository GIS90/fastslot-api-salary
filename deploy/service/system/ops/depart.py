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
from typing import Dict, List, Tuple, Literal, Any, Union
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
from deploy.utils.utils import md5 as md5_func, get_now, build_menu_tree_iterative, flatten_tree_recursive
from deploy.config import depart_root as DEPART_ROOT_ID, depart_root_pid as DEPART_ROOT_PID


class SystemOpsDepartService:

    def __init__(self, db_connection: AsyncSession):
        """
        SystemOpsDepartService class initialize
        """
        self.DEPART_SPLIT = ">"
        self.db: AsyncSession = db_connection
        self.xtb_department_curd: XtbDepartmentCurd = XtbDepartmentCurd()
        self.system_config_ev_service: SystemConfigEnumVService = SystemConfigEnumVService(db_connection=self.db)
        self.system_main_user_service: SystemMainUserService = SystemMainUserService(db_connection=self.db)

    def __str__(self):
        return "SystemOpsDepartService class."

    def __repr__(self):
        return self.__str__()

    async def __valid_model_by_md5(
            self,
            md5_id: str,
            status_check: bool = True,
            response_type: Literal["dict", "model"] = "model",
            fields: Union[List, None] = xtb_depart_tree_fields,
            lock_check: bool = False,
            root_check: bool = False
    ) -> Tuple[bool, Any]:
        if not md5_id:
            return False, FailureStatus(
                code=status_code.CODE_400_REQUEST_PARAMETER_MISS,
                message="缺少md5参数")

        model: XtbDepartmentModel = await self.xtb_department_curd.get_by_md5(db=self.db, md5=md5_id)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        if lock_check and getattr(model, "lock", None):
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT)
        if root_check and getattr(model, "id") ==  DEPART_ROOT_ID:
            return False, FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="部门根节点不允许操作")

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

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

        tree = build_menu_tree_iterative(flat_menus=_res, root_id=DEPART_ROOT_PID, id_key="id", parent_key="pid", children_key="children")
        if type_ == "flat":
            tree = flatten_tree_recursive(tree_data=tree)
        return tree, expand, check


    async def tree(self, rtx_id: str) -> Status:
        tree, expand, check = await self.__depart_format(type_="tree")
        return SuccessStatus(data={"data": tree, "expand": expand, "check": check})


    async def add_enum(self, token_rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=True,
            response_type="dict",
            fields=xtb_depart_tree_fields,
            lock_check=False,
            root_check=False
        )
        if not __flag: return data

        _res = {
            "data": data,
            "user": await self.system_main_user_service.option(status_view=True)
        }
        return SuccessStatus(data=_res)

    async def __update_depart_node_leaf(self, node_id: int, leaf: bool) -> bool:
        """
        更新节点leaf状态
        :param node_id: node id
        :param leaf: leaf
        :return: bool
        """
        model: XtbDepartmentModel = await self.xtb_department_curd.get_by_id(db=self.db, _id=node_id)
        if model:
            try:
                setattr(model, "leaf", leaf)
                await self.xtb_department_curd.update(db=self.db, model=model)
                return True
            except:
                return False
        else:
            return False
    async def __verify_by_name(self, name: str) -> bool:
        model = await self.xtb_department_curd.get_by_name_not_md5(db=self.db, name=name, md5=None)
        return True if model else False

    async def add(self, rtx_id: str, params: Dict) -> Status:
        if await self.__verify_by_name(name=params.get("name")):
            return FailureStatus(
                code=status_code.CODE_502_DATA_EXIST_NOT_ADD.value,
                message="部门名称已存在，请重新输入")

        new_model: XtbDepartmentModel = await self.xtb_department_curd.new_model()  # 创建新model
        # ***** 基本信息 *****
        params["manage_rtx"]: str = ",".join(params.get("manage_rtx")) if params.get("manage_rtx") else ""
        for k, v in params.items():
            if hasattr(new_model, k):
                setattr(new_model, k, v)
        p_node: XtbDepartmentModel = await self.xtb_department_curd.get_by_id(db=self.db, _id=params.get("pid"))   # 父节点
        new_model.level = p_node.level + 1
        new_model.dept_path = f"{p_node.dept_path}>{params.get('name')}"
        new_model.leaf = True   # 默认为叶子节点

        # <<<<< 其他信息 >>>>>
        now: str = get_now()
        node_md5_id: str = md5_func(v="%s-%s" % (params["name"], now))
        new_model.md5 = node_md5_id
        new_model.create_rtx = rtx_id
        new_model.create_time = now
        new_model.status = False
        await self.xtb_department_curd.add(db=self.db, model=new_model)

        # 更新父节点为非叶子节点
        await self.__update_depart_node_leaf(node_id=params.get("pid"), leaf=False)

        data = {
            "md5": node_md5_id,
            "pid": params.get("pid"),
            "label": params["name"]
        }
        return SuccessStatus(data=data)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_depart_tree_fields,
            lock_check=False,
            root_check=False
        )
        if not __flag: return data
        tree, _, _ = await self.__depart_format(type_="flat")
        _res = {
            "data": data,
            "tree": tree,
            "user": await self.system_main_user_service.option(status_view=True)
        }
        return SuccessStatus(data=_res)

    async def __update_parent_node_leaf_by_q_sub_node(self, node_id: int) -> bool:
        """
        更新节点leaf状态，需要进行表查询是否还有子节点
        :param node_id: node id
        :return: bool
        """
        p_node_sub = await self.xtb_department_curd.get_by_pid(db=self.db, pid=node_id)
        if not p_node_sub:
            await self.__update_depart_node_leaf(node_id=node_id, leaf=True)

        return True

    async def update(self, rtx_id: str, params: Dict) -> Status:
        # ***** 数据检查 *****
        _md5: str = params.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5_id=_md5, status_check=True, response_type="model", lock_check=False, root_check=False)
        if not __flag: return data
        model: XtbDepartmentModel = await self.xtb_department_curd.get_by_name_not_md5(
            db=self.db,
            name=params.get("label"),
            md5=_md5)
        if model:
            return FailureStatus(
                code=status_code.CODE_502_DATA_EXIST_NOT_ADD.value,
                message="部门名称已存在，请重新输入")

        # ***** 当前节点更新 *****
        update_before_pid = getattr(data, "pid")  # 更新前节点PID
        update_after_pid = params.get("pid")  # 更新后节点PID
        params["manage_rtx"]: str = ",".join(params.get("manage_rtx")) if params.get("manage_rtx") else ""
        for k, v in params.items():
            if hasattr(data, k):
                setattr(data, k, v)
        p_node: XtbDepartmentModel = await self.xtb_department_curd.get_by_id(db=self.db, _id=update_after_pid)
        # ------ level ------
        update_after_level = p_node.level + 1 if p_node else 1  # 更新后节点Level
        setattr(data, "level", update_after_level)
        # ------ dept_path ------
        update_before_dept_path = getattr(data, "dept_path")     # 更新前节点dept
        update_after_dept_path = "%s>%s" % (p_node.dept_path, getattr(data, "name")) if p_node else getattr(data, "name")  # 更新后节点dept
        setattr(data, "dept_path", update_after_dept_path)
        # ------ 其他信息 ------
        data.update_rtx = rtx_id
        data.update_time = get_now()
        await self.xtb_department_curd.update(db=self.db, model=data)

        # 更新后父节点为非叶子节点
        await self.__update_depart_node_leaf(node_id=update_after_pid, leaf=False)
        # 判断更新前节点是否为叶子节点
        await self.__update_parent_node_leaf_by_q_sub_node(node_id=update_before_pid)
        # 更新节点子节点dept_path、level
        sub_nodes = await self.xtb_department_curd.get_models_by_dept_path(db=self.db, dept_path=update_before_dept_path)
        for _node in sub_nodes:
            if not _node: continue
            _dept_path = _node.dept_path.replace(update_before_dept_path, update_after_dept_path)
            _node.dept_path = _dept_path
            _node.level = _dept_path.count(self.DEPART_SPLIT) + 1
            try:
                await self.xtb_department_curd.update(db=self.db, model=_node)
            except:
                pass

        return SuccessStatus()

    async def drag(self, rtx_id: str, params: Dict) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=params.get("md5"), status_check=True, response_type="model", lock_check=True, root_check=True)
        if not __flag: return data

        # ***** pid *****
        update_before_pid = getattr(data, "pid")    # 更新前节点PID
        update_after_pid = params.get("pid")        # 更新后节点PID
        setattr(data, "pid", update_after_pid)
        # ------ level ------
        p_node: XtbDepartmentModel = await self.xtb_department_curd.get_by_id(db=self.db, _id=update_after_pid)
        update_after_level = p_node.level + 1  # 更新后节点Level
        setattr(data, "level", update_after_level)
        # ------ dept_path ------
        update_before_dept_path = getattr(data, "dept_path")       # 更新前节点dept
        update_after_dept_path = "%s>%s" % (p_node.dept_path, getattr(data, "name"))    # 更新后节点dept
        setattr(data, "dept_path", update_after_dept_path)
        # <<<<< 其他信息 >>>>>
        data.update_rtx = rtx_id
        data.update_time = get_now()
        await self.xtb_department_curd.update(db=self.db, model=data)

        # 更新后父节点为非叶子节点
        await self.__update_depart_node_leaf(node_id=update_after_pid, leaf=False)
        # 判断更新前节点是否为叶子节点
        await self.__update_parent_node_leaf_by_q_sub_node(node_id=update_before_pid)
        # 更新节点子节点dept_path、level
        sub_nodes = await self.xtb_department_curd.get_models_by_dept_path(db=self.db, dept_path=update_before_dept_path)
        for _node in sub_nodes:
            if not _node: continue
            _dept_path = _node.dept_path.replace(update_before_dept_path, update_after_dept_path)
            _node.dept_path = _dept_path
            _node.level = _dept_path.count(self.DEPART_SPLIT) + 1
            try:
                await self.xtb_department_curd.update(db=self.db, model=_node)
            except:
                pass

        return SuccessStatus()

    async def delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5_id=md5, status_check=True, response_type="model", lock_check=False, root_check=True
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_department_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        db_model: List = await self.xtb_department_curd.get_id_by_md5_list(db=self.db, md5_list=md5_list)
        if not db_model:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if db_model and DEPART_ROOT_ID in db_model:
            return FailureStatus(code=status_code.CODE_500_DATA_ADMIN_NOT, message="部门根节点不允许删除")
        query_count: int = len(db_model)
        request_count: int = len(md5_list)
        await self.xtb_department_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")
