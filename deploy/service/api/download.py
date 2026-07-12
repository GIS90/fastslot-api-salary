# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 

base_info:
    __author__ = PyGo
    __time__ = 2026/6/7 15:32
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = download.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.service.system.config.enum_value import SystemConfigEnumVService
from deploy.utils.enumeration import CsbEnumKEY, DownloadExcelType as DET, TaskStatus as TS
from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.utils import md5 as md5_func, get_now
from deploy.curd.xtb_user_task import XtbUserTaskCurd
from deploy.schema.dao.xtb_user_task import XtbUserTaskModel
from deploy.service.system.main.user import SystemMainUserService
from deploy.service.system.main.role import SystemMainRoleService
from deploy.service.system.config.xtcs import SystemConfigXtcsService
from deploy.service.system.ops.task import SystemOpsTaskService


class ApiDownloadService(object):
    """
    ApiDownloadService Service
    """

    def __init__(self, db_connection: AsyncSession):
        """
        ApiRequestService class initialize
        """
        self.db: AsyncSession = db_connection
        self.xtb_user_task_curd: XtbUserTaskCurd = XtbUserTaskCurd()
        self.system_config_csb_enum_v_service: SystemConfigEnumVService = SystemConfigEnumVService(db_connection=db_connection)
        self.system_main_user_service: SystemMainUserService = SystemMainUserService(db_connection=db_connection)
        self.system_main_role_service: SystemMainRoleService = SystemMainRoleService(db_connection=db_connection)
        self.system_config_xtcs_service: SystemConfigXtcsService = SystemConfigXtcsService(db_connection=db_connection)
        self.system_ops_task_service: SystemOpsTaskService = SystemOpsTaskService(db_connection=db_connection)


    def __str__(self):
        return "ApiDownloadService class."

    def __repr__(self):
        return self.__str__()

    async def download_enum(self, rtx_id: str) -> Status:
        res = {
            "typeList":  await self.system_config_csb_enum_v_service.get_select_option_data(name=CsbEnumKEY.DOWNLOAD_SELECT.value, lock_view=False),
            "formatList":  await self.system_config_csb_enum_v_service.get_select_option_data(name=CsbEnumKEY.DOWNLOAD_FORMAT.value, lock_view=False)
        }
        return SuccessStatus(data=res)

    async def download(self, rtx_id: str, params: Dict) -> Status:
        dl_type = params.get("type")
        # 下载类型验证
        if dl_type not in [DET.ALL.value, DET.SELECT.value]:
            return FailureStatus(
                code=status_code.CODE_401_REQUEST_PARAMETER_ILLEGAL.value,
                message="下载类型参数错误")
        # 选择数据下载类型，md5数据列表不允许为空
        if dl_type == DET.SELECT.value and not params.get("md5"):
            return FailureStatus(
                code=status_code.CODE_403_REQUEST_PARAMETER_NOT_NULL.value,
                message="选择数据不允许为空")

        api = params.get("api")     # 区分API请求数据
        # 选择数据参数
        new_params = dict()
        if dl_type == DET.SELECT.value:
            new_params["list"] = params.get("md5")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        __task_status: str = TS.SUCCESS.value
        __error: str = ""
        __res = []
        start_time = datetime.now()
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        try:
            if api == "SystemMainUser":
                # 系统>权限>用户管理
                __res = await self.system_main_user_service.download(params=new_params)
            elif api == "SystemMainRole":
                # 系统>权限>角色管理
                __res = await self.system_main_role_service.download(params=new_params)
            elif api == "SystemConfigXtcs":
                # 系统>配置>系统参数
                __res = await self.system_config_xtcs_service.download(params=new_params)
            # elif api == "SystemOpsDict":
            #     # 系统>系统维护>数据字典
            #     __res = await self.system_ops_service.dict_enum_download(params=new_params)
            # elif api == "SystemOpsLog":
            #     # 系统>系统维护>系统日志
            #     __res = await self.system_ops_service.log_download(params=new_params)
            elif api == "SystemOpsTask":
                # 系统>系统维护>任务中心
                __res = await self.system_ops_task_service.download(params=new_params)
            else:
                return FailureStatus(
                    code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR.value,
                    message="请求参数api值不合法")
        except Exception as e:
            __task_status = TS.FAILURE.value
            __error = "服务端请求数据异常：" + str(e)

        end_time = datetime.now()
        cost = (end_time - start_time).microseconds * pow(0.1, 6)
        if cost == 0: cost = 0.0001
        new_task_model: XtbUserTaskModel = await self.xtb_user_task_curd.new_model()
        new_task_model.md5 = md5_func("%s-%s-%s-%s" % (rtx_id, params.get("api"), params.get("name"), get_now()))
        new_task_model.api = params.get("api")
        new_task_model.name = params.get("name")
        new_task_model.data = params.get("type")
        new_task_model.task = __task_status
        new_task_model.create_time = start_time
        new_task_model.cost = cost
        new_task_model.update_time = end_time
        new_task_model.rtx_id = rtx_id
        new_task_model.status = False
        await self.xtb_user_task_curd.add(db=self.db, model=new_task_model)
        if __task_status == TS.FAILURE.value:
            return FailureStatus(
                code=status_code.CODE_900_SERVER_API_EXCEPTION.value,
                message=__error)

        data = {'list': __res, 'total': len(__res), 'name': params.get("name")}
        return SuccessStatus(data=data)
