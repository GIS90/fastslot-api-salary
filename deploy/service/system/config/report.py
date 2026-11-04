# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    system>config>report service
    
base_info:
    __author__ = PyGo
    __time__ = 2026/10/3 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api-salary
    __file_name__ = report.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any, Union, Literal
from sqlalchemy.ext.asyncio import AsyncSession
from deploy.curd.xtb_xtbb import XtbXtbbCurd
from deploy.curd.xtb_xtbb_field import XtbXtbbFieldCurd
from deploy.schema.dao.xtb_xtbb import XtbXtbbModel
from deploy.schema.dao.xtb_xtbb_field import XtbXtbbFieldModel
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import (StatusCode as status_code,
                                       StatusMsg as status_msg)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.schema.dto.xtb_xtbb import xtb_xtbb_detail_fields
from deploy.schema.dto.xtb_xtbb_field import xtb_xtbb_field_list_fields, xtb_xtbb_field_detail_fields
from deploy.utils.utils import get_now, md5 as generator_md5, d2s, xtbb_field_id_value
from deploy.config import (
    table_selection_width as TABLE_SW, 
    table_default_null as TABLE_DEFAULT_NULL, 
    table_default_db_id as TABLE_DEFAULT_DB_ID
)
from deploy.utils.variable import REPORT_NOT_SELECTION_LIST
from deploy.utils.exception import ReportNotColumnException
from deploy.utils.enumeration import XtbReportKey


class SystemConfigReportService:

    def __init__(self, db_connection: AsyncSession):
        self.db: AsyncSession = db_connection
        self.xtb_xtbb_curd: XtbXtbbCurd = XtbXtbbCurd()
        self.xtb_xtbb_field_curd: XtbXtbbFieldCurd = XtbXtbbFieldCurd()

    def __str__(self):
        return "SystemConfigReportService class."

    def __repr__(self):
        return self.__str__()

    # ======================== xtb_xtbb ========================

    async def __valid_model_by_md5(
            self,
            md5: str,
            status_check: bool = True,
            response_type: str = "model",
            fields: Union[List, None] = xtb_xtbb_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少md5参数")

        model: XtbXtbbModel = await self.xtb_xtbb_curd.get_by_md5(db=self.db, md5=md5)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[XtbXtbbModel] = await self.xtb_xtbb_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            content=params.get("content")
        )
        _default_data = {
            "list": [],
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": 0,
        }
        if not models:
            return FailureStatus(
                code=status_code.CODE_101_SUCCESS_NO_DATA.value, data=_default_data
            )
        fields: Dict = await self.report_column_by_xtbb(
            rtx_id=rtx_id,
            xtbb=XtbReportKey.SystemConfigReport.value,
            type_="list",
            is_md5=True,
        )
        if not fields:
            return FailureStatus(
                code=status_code.CODE_102_SUCCESS_NO_COLUMN.value, data=_default_data
            )

        data: List = await many_model_converter_dict(
            models=models,
            fields=fields.get("column"),
            default_value=TABLE_DEFAULT_NULL,
            auto_id=fields.get("id_auto"),
            auto_id_value=params.get("offset") + 1,
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.xtb_xtbb_curd.count(self.db)
        }
        return SuccessStatus(data=result)

    async def one_by_md5(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5=md5,
            status_check=False,
            response_type="dict",
            fields=xtb_xtbb_detail_fields
        )
        return SuccessStatus(data=data) if __flag else data

    async def add(self, rtx_id: str, model: Dict) -> Status:
        db_model: XtbXtbbModel = await self.xtb_xtbb_curd.get_by_name(
            db=self.db,
            name=model.get("name"))
        if db_model:
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD,
                                 message="报表名称已存在，请更换")

        new_model: XtbXtbbModel = await self.xtb_xtbb_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('name')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_xtbb_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_model_by_md5(
            md5=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        # 不可用更新字段
        del model["md5"]
        del model["name"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_xtbb_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            md5=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        # 删除xtbb
        await self.xtb_xtbb_curd.update(db=self.db, model=data)
        # 删除xtbb-field
        await self.xtb_xtbb_field_curd.delete_by_xtbb_soft(db=self.db, xtbb=data.name, rtx_id=rtx_id)
        return SuccessStatus()

    async def batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.xtb_xtbb_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.xtb_xtbb_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def download(self, rtx_id: str, params: dict) -> List:
        models = await self.xtb_xtbb_curd.download(db=self.db, params=params)
        fields: Dict = await self.report_column_by_xtbb(
            rtx_id=rtx_id,
            xtbb=XtbReportKey.SystemConfigReport.value,
            type_="export",
            is_md5=False
        )
        if not fields:
            raise ReportNotColumnException(detail="[系统表-系统报表]未配置导出表头")

        __auto_id_name: Any = xtbb_field_id_value(options=fields.get("column"))
        data: List = await many_model_converter_dict(
            models=models,
            fields=fields.get("column"),
            default_value=TABLE_DEFAULT_NULL,
            auto_id=fields.get("id_auto"),
            auto_id_name=__auto_id_name if __auto_id_name else TABLE_DEFAULT_DB_ID,
            auto_id_value=1,
        )

        return data

    # ======================== xtb_xtbb_field ========================

    async def __valid_field_model_by_md5(
            self,
            md5: str,
            status_check: bool = True,
            response_type: str = "model",
            fields: Union[List, None] = xtb_xtbb_field_detail_fields
    ) -> Tuple[bool, Any]:
        if not md5:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少md5参数")

        model: XtbXtbbFieldModel = await self.xtb_xtbb_field_curd.get_by_md5(db=self.db, md5=md5)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and getattr(model, "status", None):
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)

        return (True, model if response_type == "model"
                        else await model_converter_dict(model=model, fields=fields, default_value="****"))

    async def field_list_by_xtbb(self, rtx_id: str, xtbb: str) -> Status:
        models: List[XtbXtbbFieldModel] = await self.xtb_xtbb_field_curd.list_by_xtbb(
            db=self.db, xtbb=xtbb
        )
        if not models:
            return SuccessStatus(data=[])

        data: List = await many_model_converter_dict(
            models=models,
            fields=xtb_xtbb_field_list_fields
        )
        return SuccessStatus(data=data)

    async def field_column_by_xtbb(self, rtx_id: str, xtbb: str) -> Status:
        # 第一步：报表
        xtbb_model: XtbXtbbModel = await self.xtb_xtbb_curd.get_by_name(db=self.db, name=xtbb)
        if not xtbb_model:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        # 第二步：报表字段
        models: List[XtbXtbbFieldModel] = await self.xtb_xtbb_field_curd.column_by_xtbb(
            db=self.db, xtbb=xtbb, list_=True, export_=False
        )
        if not models:
            return SuccessStatus(data=[])

        if xtbb in REPORT_NOT_SELECTION_LIST:
            data: List = []
        else:
            data: List = [
                {"prop": "", "width": str(TABLE_SW), "type": "selection", "fixed": "left", "align": "center"}   # 默认选择列
            ]
        for model in models:
            if not model: continue
            _d: Dict = dict[str, Any]()
            _d["prop"] = getattr(model, "name_zh", "")
            _d["label"] = getattr(model, "name_ch", "")
            _d["align"] = getattr(model, "align", "center") # 默认居中对齐
            _d["sortable"] = getattr(model, "sortable", False)
            if model.width:
                # mode=0 固定宽度(width)，mode=1 最小宽度(min-width)
                if model.mode is False:
                    _d["width"] = str(model.width)
                else:
                    _d["min-width"] = str(model.width)
            if model.filter:
                _d["filter"] = json.loads(model.filter)
            if model.fixed:
                _d["fixed"] = model.fixed
            data.append(_d)
        return SuccessStatus(data=data)
        
    async def field_add(self, rtx_id: str, model: Dict) -> Status:
        if not model.get("xtbb"):
            return FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少xtbb参数")

        new_model: XtbXtbbFieldModel = await self.xtb_xtbb_field_curd.new_model()
        __now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('field')}-{model.get('xtbb_md5')}-{d2s(__now)}-{rtx_id}")
        new_model.create_time = __now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.xtb_xtbb_field_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def field_update(self, rtx_id: str, model: Dict) -> Status:
        _md5: str = model.get("md5")
        __flag, data = await self.__valid_field_model_by_md5(
            md5=_md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        del model["md5"]
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.xtb_xtbb_field_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def field_delete_(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_field_model_by_md5(
            md5=md5, status_check=True, response_type="model"
        )
        if not __flag: return data

        setattr(data, "status", True)
        setattr(data, "delete_rtx", rtx_id)
        setattr(data, "delete_time", get_now())
        await self.xtb_xtbb_field_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def field_batch_delete(self, rtx_id: str, md5_list: List) -> Status:
        query_count: int = await self.xtb_xtbb_field_curd.count_by_md5_list(db=self.db, md5_list=md5_list)
        if not query_count:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        request_count: int = len(md5_list)
        await self.xtb_xtbb_field_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus() if query_count == request_count \
            else FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                               message=f"总数{request_count}，成功删除{query_count}，查询失败{request_count - query_count}")

    async def field_check_exist(self, rtx_id: str, table_name: str, fields: List[str]) -> Status:
        if not table_name:
            return FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少table参数")
        if not fields:
            return FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少fields参数")

        from sqlalchemy import text as sa_text
        try:
            result = await self.db.execute(sa_text(f"SHOW COLUMNS FROM `{table_name}`"))
            db_columns = {row[0] for row in result.fetchall()}
        except Exception as e:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST,
                                 message=f"表 `{table_name}` 不存在或无权限访问: {str(e)}")

        exist_list = []
        not_exist_list = []
        for f in fields:
            if not f:
                continue
            if f in db_columns:
                exist_list.append(f)
            else:
                not_exist_list.append(f)

        return SuccessStatus(data={
            "table": table_name,
            "db_columns": sorted(db_columns),
            "check_fields": fields,
            "exist": exist_list,
            "not_exist": not_exist_list,
            "all_exist": len(not_exist_list) == 0
        })

    async def report_column_by_xtbb(
            self,
            rtx_id: str,
            xtbb: str,
            type_: Literal["list", "export"],
            is_md5: bool = True
    ) -> Dict:
        """
        用于数据展示的字段列
        :param rtx_id: 用户RTD-ID
        :param xtbb: 系统报表
        :param type_: 列类型，list表示列表列，export表示导出列
        :param is_md5: 是否需要md5标识，默认True
        :return: Dict
            格式：{
                "column": [],
                "id_auto": True
            }
        """
        xtbb_model: XtbXtbbModel = await self.xtb_xtbb_curd.get_by_name(db=self.db, name=xtbb)
        if not xtbb_model: return {}

        if type_ == "list":
            models: List[XtbXtbbFieldModel] = await self.xtb_xtbb_field_curd.column_by_xtbb(
                db=self.db, xtbb=xtbb, list_=True, export_=False
            )
        else:
            models: List[XtbXtbbFieldModel] = await self.xtb_xtbb_field_curd.column_by_xtbb(
                db=self.db, xtbb=xtbb, list_=False, export_=True
            )
        if not models: return {}

        column: List = []
        if is_md5:
            column.append({"key": "md5", "type": "string"})
        _id_auto: bool = False
        for model in models:
            if not model: continue
            _d: Dict = dict()
            _d["key"] = getattr(model, "field", "")
            _d["name"] = getattr(model, "name_zh", "") if type_ == "list" else getattr(model, "name_ch", "")
            _d["type"] = getattr(model, f"{type_}_type", "")
            _d["null"] = getattr(model, "null", "")
            column.append(_d)
            if str(_d["key"]).lower() == "id":
                _id_auto = getattr(model, "id_auto", False)
        data: Dict = {
            "column": column,
            "id_auto": _id_auto
        }
        return data
