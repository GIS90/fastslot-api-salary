# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    salary>notify>dtalk service

base_info:
    __author__ = PyGo
    __time__ = 2026/11/18 10:00
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = dtalk.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import os
import json
import hashlib
from typing import Dict, List, Optional, Tuple, Any, Literal
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

import xlrd
import openpyxl

from deploy.config import (
    store_yun_base,
    table_default_null as TABLE_DEFAULT_NULL,
    table_default_db_id as TABLE_DEFAULT_DB_ID
)
from deploy.curd.salary_dtalk_message import SalaryDtalkMessageCurd
from deploy.curd.salary_dtalk_robot import SalaryDtalkRobotCurd
from deploy.schema.dao.salary_dtalk import SalaryDtalkMessageModel, SalaryDtalkRobotModel
from deploy.service.system.config.report import SystemConfigReportService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.utils import (
    get_now, md5 as generator_md5, get_qiniu_abs_file_url, xtbb_field_id_value, 
    random_uuid4, rename_local_file
)
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.utils.enumeration import FileTypeEnum, XtbReportKey
from deploy.schema.dto.salary_dtalk import (
    salary_dtalk_message_detail_fields,
    salary_dtalk_robot_detail_fields
)
from deploy.utils.exception import ReportNotColumnException
from deploy.utils.upload import uploadUtils
from deploy.delib.excel_lib import ExcelLib
from deploy.utils.variable import EXCEL_FORMAT
from deploy.delib.dingtalk_lib import DingtalkLib
from deploy.utils.logger import logger as LOG


class SalaryNotifyDtalkService:
    """钉钉绩效通知"""

    def __init__(self, db_connection: AsyncSession):
        self.db: AsyncSession = db_connection
        self.salary_dtalk_message_curd: SalaryDtalkMessageCurd = SalaryDtalkMessageCurd()
        self.salary_dtalk_robot_curd: SalaryDtalkRobotCurd = SalaryDtalkRobotCurd()
        self.system_config_report_service: SystemConfigReportService = SystemConfigReportService(db_connection=db_connection)
        self.upload_utils: uploadUtils = uploadUtils()
        self.excel_lib: ExcelLib = ExcelLib()

    def __str__(self):
        return "SalaryNotifyDtalkService class."

    def __repr__(self):
        return self.__str__()

    # - - - - - - - - - - - - - - - - - - - - 内部方法 - - - - - - - - - - - - - - - - - - - -
    @staticmethod
    def __json_dict(value: Optional[str]) -> Dict:
        if not value:
            return {}
        try:
            result = json.loads(value)
            return result if isinstance(result, dict) else {}
        except Exception:
            return {}

    @staticmethod
    def __json_list(value: Optional[str]) -> List[str]:
        if not value:
            return []
        try:
            result = json.loads(value)
            return [str(i) for i in result] if isinstance(result, list) else []
        except Exception:
            return []

    @staticmethod
    def __parse_user_map(value: Optional[str]) -> Dict[str, List[str]]:
        """解析人员名单：兼容 {"0": [...]} 分组格式与旧扁平数组格式"""
        if not value:
            return {}
        try:
            result = json.loads(value)
        except Exception:
            return {}
        if isinstance(result, dict):
            return {
                str(sheet): [str(uid) for uid in users]
                for sheet, users in result.items()
                if isinstance(users, list)
            }
        if isinstance(result, list):
            return {"0": [str(uid) for uid in result]}
        return {}

    @staticmethod
    def __resend_target_map(
        users: Any,
        failure_map: Dict[str, List[str]],
        sheets: List[str]
    ) -> Dict[str, List[str]]:
        """解析提交的重发人员，按 Sheet 过滤，确保只重发对应 Sheet 的失败人员"""
        target_map: Dict[str, List[str]] = {}
        if not users:
            target_map = {sheet: list(failure_map.get(sheet) or []) for sheet in sheets}
        elif isinstance(users, dict):
            for sheet, items in users.items():
                target_map[str(sheet)] = [str(i) for i in (items or []) if i]
        elif isinstance(users, list):
            if users and all(isinstance(item, dict) for item in users if item is not None):
                for item in users:
                    if not item:
                        continue
                    sheet = str(item.get("sheet") or item.get("sheetIndex") or "")
                    if not sheet:
                        continue
                    target_map[sheet] = [str(i) for i in (item.get("users") or []) if i]
            else:
                flat_ids = {str(i) for i in users if i}
                target_map = {
                    sheet: [uid for uid in (failure_map.get(sheet) or []) if uid in flat_ids]
                    for sheet in sheets
                }

        result: Dict[str, List[str]] = {}
        for sheet, items in target_map.items():
            allowed = set(failure_map.get(sheet) or [])
            filtered = list(dict.fromkeys(str(i) for i in items if str(i) in allowed))
            if filtered:
                result[sheet] = filtered
        return result

    @staticmethod
    def __file_md5(file_path: str) -> str:
        if not file_path or not os.path.exists(file_path):
            return ""
        _md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    _md5.update(chunk)
            return _md5.hexdigest()
        except Exception:
            return ""

    @staticmethod
    def __default_columns(columns: Dict) -> Dict:
        """默认全部列被选中"""
        __res: Dict = {}
        if not columns:
            return __res
        for k, v in columns.items():
            __res[str(k)] = [str(item.get("key")) for item in v if item and item.get("key")]
        return __res

    @staticmethod
    def __set_sheet_index(model: SalaryDtalkMessageModel) -> List[str]:
        if not model.set_sheet:
            return ["0"]
        return [str(i) for i in str(model.set_sheet).split(";") if str(i) != ""]

    def __sheet_names(self, model: SalaryDtalkMessageModel) -> Dict:
        return self.__json_dict(model.sheet_names)

    def __sheet_options(self, model: SalaryDtalkMessageModel) -> List[Dict]:
        return [{"key": k, "value": v} for k, v in self.__sheet_names(model).items()]

    async def __message_detail_dict(self, model: SalaryDtalkMessageModel) -> Dict:
        titles = self.__json_dict(model.set_title)
        all_columns = self.__json_dict(model.sheet_columns)
        set_columns = self.__json_dict(model.set_column)
        cur_sheet = str(model.cur_sheet or "0")
        # DTO字段转换
        data: Dict = await model_converter_dict(
            model=model,
            fields=salary_dtalk_message_detail_fields,
            default_value=""
        ) or {}
        # 业务计算字段
        data.update({
            "curSheet": cur_sheet,
            "nsheet": model.nsheet or 1,
            "sheetNames": self.__sheet_options(model),
            "setSheetIndex": self.__set_sheet_index(model),
            "setTitle": titles.get(cur_sheet) or "",
            "setColumns": all_columns.get(cur_sheet) or [],
            "setSelectColumn": [str(i) for i in (set_columns.get(cur_sheet) or [])],
            "url": get_qiniu_abs_file_url(model.file_store_url or ""),
        })
        return data

    async def __valid_model_by_md5(
        self,
        query_id: str,
        query_type: Literal["message", "robot"] = "message",
        status_check: bool = True,
        response_type: Literal["dict", "model"] = "model",
    ) -> Tuple[bool, Any]:
        """统一校验md5对应的数据是否存在、是否已删除（参考system main user service）"""
        if not query_id:
            return False, FailureStatus(code=status_code.CODE_4002_REQUEST_PARAMETER_MISS_MD5.value)

        is_message: bool = query_type == "message"
        model = (
            await self.salary_dtalk_message_curd.get_by_md5(db=self.db, md5=query_id)
            if is_message
            else await self.salary_dtalk_robot_curd.get_by_md5(db=self.db, md5=query_id)
        )
        entity: str = "数据" if is_message else "机器人数据"
        if not model:
            return False, FailureStatus(
                code=status_code.CODE_501_DATA_NOT_EXIST.value,
                message=f"{entity}不存在"
            )
        if status_check and getattr(model, "status", False):
            return False, FailureStatus(
                code=status_code.CODE_503_DATA_DELETE_NOT_EDIT.value,
                message=f"{entity}已删除，不允许操作"
            )
        if response_type == "dict":
            return True, (
                await self.__message_detail_dict(model) if is_message
                else await self.__robot_dict(model)
            )
        return True, model

    async def __get_alive_message(self, md5: str) -> Tuple[bool, Any]:
        return await self.__valid_model_by_md5(query_id=md5, query_type="message")

    async def __get_alive_robot(self, md5: str) -> Tuple[bool, Any]:
        return await self.__valid_model_by_md5(query_id=md5, query_type="robot")

    def __read_headers(self, file_path: str) -> Dict:
        """读取Excel的Sheet与表头信息：xlrd仅支持.xls，.xlsx使用openpyxl"""
        if os.path.splitext(file_path)[-1].lower() != ".xlsx":
            return self.excel_lib.read_headers(file_path)
        __res: Dict = {'sheets': {}, 'nsheet': 0, 'names': {}, 'columns': {}}
        try:
            book = openpyxl.load_workbook(filename=file_path, data_only=True, read_only=True)
            for index, sheet in enumerate(book.worksheets):
                __res['sheets'][str(index)] = {
                    'row': sheet.max_row, 'col': sheet.max_column,
                    'index': index, 'name': sheet.title
                }
                __res['names'][str(index)] = sheet.title
                row_values = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True), tuple())
                __res['columns'][str(index)] = [
                    {'key': str(k), 'value': '' if v is None else str(v)}
                    for k, v in enumerate(row_values)
                ]
            __res['nsheet'] = len(__res['sheets'])
            book.close()
        except Exception:
            return {'sheets': {}, 'nsheet': 0, 'names': {}, 'columns': {}}
        return __res

    @staticmethod
    def __rows_build(titles: tuple, values_list: List, columns: List) -> List[Dict]:
        rows: List[Dict] = []
        for values in values_list:
            user_id = str(values[0]).strip() if values and values[0] is not None else ""
            if not user_id:
                continue
            unit: Dict = {}
            for col in columns or []:
                try:
                    col_index = int(col)
                except Exception:
                    continue
                if col_index < 0 or col_index >= len(titles):
                    continue
                title = titles[col_index]
                value = values[col_index] if col_index < len(values) else ""
                if value is None:
                    value = ""
                if not title and value == "":
                    continue
                unit[str(title)] = value if value != "" else "/"
            rows.append({"id": user_id, "data": unit})
        return rows

    @classmethod
    def __read_sheet_rows(cls, file_path: str, sheet_index: int, columns: List) -> List[Dict]:
        """读取Sheet数据：第1列为钉钉User-ID，其余按设置的列读取"""
        if os.path.splitext(file_path)[-1].lower() == ".xlsx":
            try:
                book = openpyxl.load_workbook(filename=file_path, data_only=True, read_only=True)
                if sheet_index < 0 or sheet_index >= len(book.worksheets):
                    book.close()
                    return []
                rows_iter = book.worksheets[sheet_index].iter_rows(values_only=True)
                titles = next(rows_iter, tuple())
                rows = cls.__rows_build(titles=titles, values_list=list(rows_iter), columns=columns)
                book.close()
                return rows
            except Exception:
                return []
        try:
            book = xlrd.open_workbook(file_path)
            if sheet_index < 0 or sheet_index >= book.nsheets:
                return []
            sheet = book.sheet_by_index(sheet_index)
            titles = sheet.row_values(0)
            values_list = [sheet.row_values(index) for index in range(1, sheet.nrows)]
            return cls.__rows_build(titles=titles, values_list=values_list, columns=columns)
        except Exception:
            return []

    @staticmethod
    def __format_message(content: Dict, title: str) -> Dict:
        title = title or f"{get_now()}【自动化提醒】"
        text = f"### {title}"
        for k, v in (content or {}).items():
            if not k and not v:
                continue
            if isinstance(v, float):
                v = round(v, 2)
            text += f"  \n  - {k}: {v}"
        # return {"title": f"{title}    详情...", "text": text}
        return {"title": title, "text": text}

    def __send_by_robot(self, app_key: str, app_secret: str, rows: List[Dict], title: str) -> Tuple[int, int]:
        """同步方法：在线程池中执行钉钉发送，返回(成功数, 失败数)，-1表示Token失败"""
        dtalk_api = DingtalkLib(app_key=app_key, app_secret=app_secret)
        if not dtalk_api.access_token:
            dtalk_api.close()
            return -1, 0
        success: List = list()
        failure: List = list()
        
        for row in rows:
            try:
                result = dtalk_api.robot2send(
                    message=self.__format_message(content=row.get("data"), title=title),
                    to_id=row.get("id")
                )
                result_dict = result.dict()
                if result_dict.get("code") == status_code.CODE_100_SUCCESS.value:
                    success.append(row.get("id"))
                else:
                    LOG.warning(f"[SalaryNotifyDtalkService]发送失败：{result_dict.get('message')}")
                    failure.append(row.get("id"))
            except Exception as e:
                LOG.error(f"[SalaryNotifyDtalkService]发送消息异常：{e}")
                failure.append(row.get("id"))
        else:
            dtalk_api.close()
        return success, failure

    @staticmethod
    def __ping_robot(app_key: str, app_secret: str) -> bool:
        dtalk_api = DingtalkLib(app_key=app_key, app_secret=app_secret)
        try:
            return bool(dtalk_api.access_token)
        finally:
            dtalk_api.close()

    # - - - - - - - - - - - - - - - - - - - - 消息文件 - - - - - - - - - - - - - - - - - - - -
    async def store_upload(self, rtx_id: str, file_: UploadFile) -> Status:
        """上传Excel文件并解析入库"""
        file_name = getattr(file_, "filename", "") or ""
        if os.path.splitext(file_name)[-1].lower() not in EXCEL_FORMAT:
            return FailureStatus(code=status_code.CODE_454_REQUEST_FILE_NOT_SUPPORT.value)
        if len(file_name) > 80:
            return FailureStatus(code=status_code.CODE_405_REQUEST_PARAMETER_EXCEED_LEN_MAX.value, message="文件名称长度超出限制")

        result = await self.upload_utils.upload(
            rtx_id=rtx_id, upload_type=str(FileTypeEnum.DINGTALK.value), file_=file_)
        if result.dict().get("code") != status_code.CODE_100_SUCCESS.value:
            return result
        data: Dict = result.dict().get("data") or {}
        local_file: str = data.get("local") or ""
        store_name: str = data.get("store_name") or ""

        md5_value: str = self.__file_md5(local_file)
        if not md5_value:
            return FailureStatus(code=status_code.CODE_456_REQUEST_FILE_LOCAL_STORE_FAILURE.value)
        if await self.salary_dtalk_message_curd.get_by_md5(db=self.db, md5=md5_value):
            try:
                os.remove(local_file)
            except Exception:
                ...
            return FailureStatus(
                code=status_code.CODE_458_REQUEST_FILE_DATA_EXIST.value,
                message="文件数据已存在，无需重复上传"
            )

        excel_headers: Dict = self.__read_headers(local_file)
        nsheet: int = excel_headers.get("nsheet") or 0
        if not nsheet:
            return FailureStatus(
                code=status_code.CODE_455_REQUEST_FILE_CONTENT_ERROR.value,
                message="Excel文件解析失败，请检查文件内容"
            )

        model: SalaryDtalkMessageModel = await self.salary_dtalk_message_curd.new_model()
        model.md5 = md5_value
        model.file_name = file_name
        model.file_local_url = local_file
        model.file_store_url = store_name
        model.robot = ""
        model.count = 0
        model.number = 0
        model.nsheet = nsheet
        model.sheet_names = json.dumps(excel_headers.get("names") or {}, ensure_ascii=False)
        model.sheet_columns = json.dumps(excel_headers.get("columns") or {}, ensure_ascii=False)
        model.headers = json.dumps(excel_headers.get("sheets") or {}, ensure_ascii=False)
        model.set_sheet = "0"
        model.cur_sheet = "0"
        model.set_column = json.dumps(self.__default_columns(excel_headers.get("columns") or {}), ensure_ascii=False)
        model.set_title = json.dumps({})
        model.create_rtx = rtx_id
        model.create_time = get_now()
        model.status = False
        await self.salary_dtalk_message_curd.add(db=self.db, model=model)
        return SuccessStatus(data={"name": model.file_name, "md5": md5_value})

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        models: List[SalaryDtalkMessageModel] | None = await self.salary_dtalk_message_curd.pagination(
            db=self.db,
            offset=params.get("offset"),
            limit=params.get("limit"),
            content=params.get("content")
        )
        _default_data = {
            "list": [],
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": 0
        }
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value, data=_default_data)

        fields: Dict = await self.system_config_report_service.report_column_by_xtbb(
            rtx_id=rtx_id,
            xtbb=XtbReportKey.SalaryNotifyDtalk.value,
            type_="list",
            is_md5=True,
            is_file_url=True
        )
        if not fields:
            return FailureStatus(code=status_code.CODE_102_SUCCESS_NO_COLUMN.value, data=_default_data)
        data: List | None = await many_model_converter_dict(
            models=models,
            fields=fields.get("column"),
            default_value=TABLE_DEFAULT_NULL,
            auto_id=fields.get("id_auto"),
            auto_id_value=(params.get("offset") or 0) + 1
        )
        result: Dict = {
            "list": data,
            "page": params.get("page"),
            "pageSize": params.get("limit"),
            "total": await self.salary_dtalk_message_curd.count(self.db)
        }
        return SuccessStatus(data=result)

    async def detail(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            query_id=md5, query_type="message", response_type="dict")
        return data if not __flag else SuccessStatus(data=data)

    async def update(self, rtx_id: str, params: Dict) -> Status:
        __flag, model = await self.__get_alive_message(params.get("md5"))
        if not __flag: return model

        name: str = params.get("name") or f"{get_now()}.xlsx" # 加上默认文件名称
        if os.path.splitext(name)[-1].lower() not in EXCEL_FORMAT:
            return FailureStatus(
                code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR.value,
                message=f"文件格式只支持{EXCEL_FORMAT}"
            )
        set_sheet: List = params.get("set_sheet") or []
        if not isinstance(set_sheet, list) or not set_sheet:
            return FailureStatus(
                code=status_code.CODE_403_REQUEST_PARAMETER_NOT_NULL.value,
                message="消息Sheet不允许为空"
            )
        column: List = params.get("column") or []
        if not isinstance(column, list) or len(column) < 2:
            return FailureStatus(
                code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR.value,
                message="消息列头至少选择2列"
            )
        cur_sheet: str = str(params.get("sheet") or "0")

        if name != model.file_name:
            # 重命名本地文件
            new_local = rename_local_file(local_file=model.file_local_url, new_file_name=name)
            if new_local:
                model.file_local_url = new_local
            model.file_name = name
        model.set_sheet = ";".join([str(i) for i in set_sheet])
        model.cur_sheet = cur_sheet
        titles: Dict = self.__json_dict(model.set_title)
        titles[cur_sheet] = params.get("title") or ""
        model.set_title = json.dumps(titles, ensure_ascii=False)
        set_columns: Dict = self.__json_dict(model.set_column)
        set_columns[cur_sheet] = [str(i) for i in column]
        model.set_column = json.dumps(set_columns, ensure_ascii=False)
        model.update_rtx = rtx_id
        model.update_time = get_now()
        await self.salary_dtalk_message_curd.update(db=self.db, model=model)
        return SuccessStatus(data={"md5": model.md5})

    async def change_sheet(self, rtx_id: str, md5: str, sheet: str) -> Status:
        __flag, model = await self.__get_alive_message(md5)
        if not __flag: return model
        cur_sheet: str = str(sheet or "0")
        titles: Dict = self.__json_dict(model.set_title)
        all_columns: Dict = self.__json_dict(model.sheet_columns)
        set_columns: Dict = self.__json_dict(model.set_column)
        return SuccessStatus(data={
            "md5": model.md5,
            "setTitle": titles.get(cur_sheet) or "",
            "setSelectColumn": [str(i) for i in (set_columns.get(cur_sheet) or [])],
            "setColumns": all_columns.get(cur_sheet) or []
        })

    async def delete(self, rtx_id: str, md5: str) -> Status:
        __flag, model = await self.__get_alive_message(md5)
        if not __flag: return model
        model.status = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        await self.salary_dtalk_message_curd.update(db=self.db, model=model)
        return SuccessStatus(data={"md5": md5})

    async def delete_batch(self, rtx_id: str, md5_list: List[str]) -> Status:
        if not md5_list:
            return FailureStatus(code=status_code.CODE_403_REQUEST_PARAMETER_NOT_NULL.value)
        await self.salary_dtalk_message_curd.batch_soft_delete(
            db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus()

    async def download(self, rtx_id: str, params: Dict) -> List[Dict]:
        models = await self.salary_dtalk_message_curd.list_all(
            db=self.db, md5_list=(params or {}).get("list"))
        fields: Dict = await self.system_config_report_service.report_column_by_xtbb(
            rtx_id=rtx_id,
            xtbb=XtbReportKey.SalaryNotifyDtalk.value,
            type_="export",
            is_md5=False
        )
        if not fields:
            raise ReportNotColumnException(detail="[钉钉消息通知]未配置导出表头")

        __auto_id_name: Any = xtbb_field_id_value(options=fields.get("column"))
        data: List | None = await many_model_converter_dict(
            models=models,
            fields=fields.get("column"),
            default_value=TABLE_DEFAULT_NULL,
            auto_id=fields.get("id_auto"),
            auto_id_name=__auto_id_name if __auto_id_name else TABLE_DEFAULT_DB_ID,
            auto_id_value=1,
        )
        return data

    # - - - - - - - - - - - - - - - - - - - - 机器人 - - - - - - - - - - - - - - - - - - - -
    @staticmethod
    async def __robot_dict(model: SalaryDtalkRobotModel) -> Dict:
        # DTO字段转换
        return await model_converter_dict(
            model=model,
            fields=salary_dtalk_robot_detail_fields,
            default_value="****"
        )

    async def robot_list(self, rtx_id: str) -> Status:
        models = await self.salary_dtalk_robot_curd.option(db=self.db)
        __list: List[Dict] = []
        for index, model in enumerate(models or [], start=1):
            item = await self.__robot_dict(model)
            item["id"] = index
            __list.append(item)
        return SuccessStatus(data={"list": __list, "total": len(__list)})

    async def robot_add(self, rtx_id: str, params: Dict) -> Status:
        key: str = params.get("key") or ""
        secret: str = params.get("secret") or ""
        agent_id: str = str(params.get("agent_id") or "")
        if await self.salary_dtalk_robot_curd.get_by_key_secret(
                db=self.db, key=key, secret=secret, agent_id=agent_id):
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD.value)

        if params.get("select"):
            await self.salary_dtalk_robot_curd.clear_select(db=self.db)

        model: SalaryDtalkRobotModel = await self.salary_dtalk_robot_curd.new_model()
        model.md5 = generator_md5(v=f"{rtx_id}-{key}-{secret}-{agent_id}-{get_now()}")
        model.name = params.get("name") or ""
        model.key = key
        model.secret = secret
        model.agent_id = agent_id
        model.select = True if params.get("select") else False
        model.description = params.get("description") or ""
        model.create_rtx = rtx_id
        model.create_time = get_now()
        model.status = False
        await self.salary_dtalk_robot_curd.add(db=self.db, model=model)
        # 显式提交，保证接口响应前数据已落库（否则前端紧随的列表刷新会读到旧数据）
        await self.db.commit()
        return SuccessStatus(data={"md5": model.md5})

    async def robot_detail(self, rtx_id: str, md5: str) -> Status:
        __flag, data = await self.__valid_model_by_md5(
            query_id=md5, query_type="robot", response_type="dict")
        if not __flag:
            return data
        return SuccessStatus(data=data)

    async def robot_update(self, rtx_id: str, params: Dict) -> Status:
        __flag, model = await self.__get_alive_robot(params.get("md5"))
        if not __flag:
            return model
        if params.get("select"):
            await self.salary_dtalk_robot_curd.clear_select(db=self.db)
            await self.db.refresh(model)
        model.name = params.get("name") or ""
        model.key = params.get("key") or ""
        model.secret = params.get("secret") or ""
        model.agent_id = str(params.get("agent_id") or "")
        model.description = params.get("description") or ""
        model.select = True if params.get("select") else False
        model.update_rtx = rtx_id
        model.update_time = get_now()
        await self.salary_dtalk_robot_curd.update(db=self.db, model=model)
        # 显式提交，保证接口响应前数据已落库（否则前端紧随的列表刷新会读到旧数据）
        await self.db.commit()
        return SuccessStatus(data={"md5": model.md5})

    async def robot_select(self, rtx_id: str, md5: str, select: bool) -> Status:
        __flag, model = await self.__get_alive_robot(md5)
        if not __flag:
            return model
        await self.salary_dtalk_robot_curd.clear_select(db=self.db)
        await self.db.refresh(model)
        model.select = bool(select)
        model.update_rtx = rtx_id
        model.update_time = get_now()
        await self.salary_dtalk_robot_curd.update(db=self.db, model=model)
        # 显式提交，保证接口响应前数据已落库（否则前端紧随的列表刷新会读到旧数据）
        await self.db.commit()
        return SuccessStatus(data={"md5": md5})

    async def robot_delete(self, rtx_id: str, md5: str) -> Status:
        __flag, model = await self.__get_alive_robot(md5)
        if not __flag:
            return model
        model.status = True
        model.delete_rtx = rtx_id
        model.delete_time = get_now()
        await self.salary_dtalk_robot_curd.update(db=self.db, model=model)
        # 显式提交，保证接口响应前数据已落库（否则前端紧随的列表刷新会读到旧数据）
        await self.db.commit()
        return SuccessStatus(data={"md5": md5})

    async def robot_delete_batch(self, rtx_id: str, md5_list: List[str]) -> Status:
        if not md5_list:
            return FailureStatus(code=status_code.CODE_403_REQUEST_PARAMETER_NOT_NULL.value)
        await self.salary_dtalk_robot_curd.batch_soft_delete(
            db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        # 显式提交，保证接口响应前数据已落库（否则前端紧随的列表刷新会读到旧数据）
        await self.db.commit()
        return SuccessStatus()

    async def robot_ping(self, rtx_id: str, md5: str) -> Status:
        __flag, model = await self.__get_alive_robot(md5)
        if not __flag: return model
        if not model.key or not model.secret:
            return FailureStatus(
                code=status_code.CODE_505_DATA_INCOMPLETE.value,
                message="缺少key或者secret，请完善机器人配置信息"
            )
        __ok: bool = await run_in_threadpool(self.__ping_robot, model.key, model.secret)
        if not __ok:
            return FailureStatus(
                code=status_code.CODE_903_OTHER_THREE_API_TOKEN_FAILURE.value,
                message="PING失败，请检查KEY或SECRET是否配置正确"
            )
        return SuccessStatus(data={"md5": md5})

    # - - - - - - - - - - - - - - - - - - - - 发送 - - - - - - - - - - - - - - - - - - - -
    async def send_init(self, rtx_id: str, md5: str) -> Status:
        __flag, model = await self.__get_alive_message(md5)
        if not __flag: return model
        robots = await self.salary_dtalk_robot_curd.option(db=self.db)
        robot_index: str = ""
        robot_enums: List[Dict] = []
        for robot in robots or []:
            robot_enums.append({"key": robot.md5, "value": robot.name})
            if robot.select:
                robot_index = robot.md5
        return SuccessStatus(data={
            "sheetIndex": self.__set_sheet_index(model),
            "sheetNames": self.__sheet_options(model),
            "robotIndex": robot_index,
            "robotEnums": robot_enums
        })

    async def resend_init(self, rtx_id: str, md5: str) -> Status:
        """重发初始化：加载配置中的 Sheet、各 Sheet 失败名单及机器人选项"""
        __flag, model = await self.__get_alive_message(md5)
        if not __flag: return model
        robots = await self.salary_dtalk_robot_curd.option(db=self.db)
        robot_index: str = ""
        robot_enums: List[Dict] = []
        for robot in robots or []:
            robot_enums.append({"key": robot.md5, "value": robot.name})
            if robot.md5 == (model.robot or "") or (not model.robot and robot.select):
                robot_index = robot.md5
        sheet_names: Dict = self.__sheet_names(model)
        failure_map: Dict[str, List[str]] = self.__parse_user_map(model.failure)
        sheets: List[str] = self.__set_sheet_index(model)
        failure_users: Dict[str, List[str]] = {
            sheet: list(failure_map.get(sheet) or []) for sheet in sheets
        }
        failure_groups: List[Dict] = [
            {
                "sheet": sheet,
                "sheetName": sheet_names.get(sheet, ""),
                "users": failure_users[sheet]
            }
            for sheet in sheets
        ]
        return SuccessStatus(data={
            "sheetIndex": sheets,
            "sheetNames": self.__sheet_options(model),
            "failureUsers": failure_users,
            "failureGroups": failure_groups,
            "robotIndex": robot_index,
            "robotEnums": robot_enums
        })

    async def send(self, rtx_id: str, params: Dict) -> Status:
        __flag, message_model = await self.__get_alive_message(params.get("md5"))
        if not __flag:
            return message_model
        __flag, robot_model = await self.__get_alive_robot(params.get("robot"))
        if not __flag:
            return robot_model
        if not robot_model.key or not robot_model.secret:
            return FailureStatus(
                code=status_code.CODE_505_DATA_INCOMPLETE.value,
                message="缺少key或者secret，请完善机器人配置信息")
        file_path: str = message_model.file_local_url or ""
        if not file_path or not os.path.exists(file_path):
            return FailureStatus(
                code=status_code.CODE_451_REQUEST_FILE_NOT_EXIST.value,
                message="文件不存在，请重新上传")
        sheet_list: List = params.get("sheet") or []
        if not sheet_list:
            return FailureStatus(code=status_code.CODE_403_REQUEST_PARAMETER_NOT_NULL.value, message="请选择发送的Sheet，并配置列和标题")

        set_columns: Dict = self.__json_dict(message_model.set_column)
        set_titles: Dict = self.__json_dict(message_model.set_title)
        sheet_names: Dict = self.__sheet_names(message_model)

        __results: List[Dict] = []
        __number: int = 0
        # 按 Sheet 索引分组存储，解决多 Sheet 重复人员无法区分的问题
        __success_map: Dict[str, List[str]] = {}
        __failure_map: Dict[str, List[str]] = {}
        for sheet in sheet_list:
            __sheet: str = str(sheet)
            item: Dict = {"sheet": __sheet, "sheetName": sheet_names.get(__sheet, "")}
            rows = self.__read_sheet_rows(
                file_path=file_path,
                sheet_index=int(__sheet),
                columns=set_columns.get(__sheet) or []
            )
            if not rows:
                item["ok"] = False
                item["message"] = f"文件第{int(__sheet) + 1}Sheet无数据"
                __results.append(item)
                continue
            success_list, failure_list = await run_in_threadpool(
                self.__send_by_robot,
                robot_model.key,
                robot_model.secret,
                rows,
                set_titles.get(__sheet) or ""
            )
            if success_list == -1:
                return FailureStatus(
                    code=status_code.CODE_903_OTHER_THREE_API_TOKEN_FAILURE.value,
                    message="钉钉Token初始化失败，请检查KEY或SECRET是否配置正确"
                )
            success_count, failure_count = len(success_list), len(failure_list)
            __number += success_count + failure_count
            __success_map[__sheet] = list(success_list)
            __failure_map[__sheet] = list(failure_list)
            item["ok"] = failure_count == 0
            item["message"] = f"成功：{success_count}，失败：{failure_count}"
            item["data"] = {
                "success": success_count,
                "failure": failure_count,
                "total": __number,
                "successList": success_list,
                "failureList": failure_list
            }
            __results.append(item)

        message_model.count = (message_model.count or 0) + 1
        message_model.number = (message_model.number or 0) + __number
        message_model.robot = robot_model.md5
        message_model.success = json.dumps(__success_map, ensure_ascii=False)
        message_model.failure = json.dumps(__failure_map, ensure_ascii=False)
        message_model.update_rtx = rtx_id
        message_model.update_time = get_now()
        await self.salary_dtalk_message_curd.update(db=self.db, model=message_model)
        
        return SuccessStatus(data=__results)

    async def resend(self, rtx_id: str, params: Dict) -> Status:
        """按 Sheet + 人员重发失败名单，并更新分组成功/失败记录"""
        __flag, message_model = await self.__get_alive_message(params.get("md5"))
        if not __flag: return message_model
        __flag, robot_model = await self.__get_alive_robot(params.get("robot"))
        if not __flag: return robot_model
        if not robot_model.key or not robot_model.secret:
            return FailureStatus(code=status_code.CODE_505_DATA_INCOMPLETE.value,
                                 message="缺少key或secret，请完善机器人配置信息")

        sheets: List[str] = self.__set_sheet_index(message_model)
        success_map: Dict[str, List[str]] = self.__parse_user_map(message_model.success)
        failure_map: Dict[str, List[str]] = self.__parse_user_map(message_model.failure)
        if not any(failure_map.get(sheet) for sheet in sheets):
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value,
                                 message="暂无失败人员可重发")
        target_map: Dict[str, List[str]] = self.__resend_target_map(
            users=params.get("users"), failure_map=failure_map, sheets=sheets)
        if not target_map:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value,
                                 message="所选人员不在对应Sheet的失败名单中")

        file_path: str = message_model.file_local_url or ""
        if not file_path or not os.path.exists(file_path):
            return FailureStatus(code=status_code.CODE_451_REQUEST_FILE_NOT_EXIST.value,
                                 message="文件不存在，请重新上传")

        set_columns: Dict = self.__json_dict(message_model.set_column)
        set_titles: Dict = self.__json_dict(message_model.set_title)
        sheet_names: Dict = self.__sheet_names(message_model)

        rows_by_sheet: Dict[str, List[Dict]] = {}
        for sheet_key, target_ids in target_map.items():
            try:
                sheet_index = int(sheet_key)
            except Exception:
                continue
            rows = self.__read_sheet_rows(
                file_path=file_path, sheet_index=sheet_index,
                columns=set_columns.get(sheet_key) or []
            )
            id_set = set(target_ids)
            matched = [row for row in rows if str(row.get("id")) in id_set]
            if matched:
                rows_by_sheet[sheet_key] = matched
        if not rows_by_sheet:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value,
                                 message="未在文件中找到失败人员对应的数据行")

        __results: List[Dict] = []
        resent_ok: List[str] = []
        resent_fail: List[str] = []
        __number: int = 0
        for sheet_key, rows in rows_by_sheet.items():
            success_list, failure_list = await run_in_threadpool(
                self.__send_by_robot, robot_model.key, robot_model.secret,
                rows, set_titles.get(sheet_key) or ""
            )
            if success_list == -1:
                return FailureStatus(
                    code=status_code.CODE_903_OTHER_THREE_API_TOKEN_FAILURE.value,
                    message="钉钉Token初始化失败，请检查配置"
                )
            resent_ok.extend(success_list)
            resent_fail.extend(failure_list)
            __number += len(success_list) + len(failure_list)

            ok_set = {str(uid) for uid in success_list}
            fail_set = {str(uid) for uid in failure_list}
            old_success = list(success_map.get(sheet_key) or [])
            old_failure = list(failure_map.get(sheet_key) or [])
            success_map[sheet_key] = list(dict.fromkeys(
                old_success + [str(uid) for uid in success_list]
            ))
            failure_map[sheet_key] = [
                uid for uid in old_failure if uid not in ok_set
            ]
            for uid in old_failure:
                if uid in fail_set and uid not in failure_map[sheet_key]:
                    failure_map[sheet_key].append(uid)

            __results.append({
                "sheet": sheet_key,
                "sheetName": sheet_names.get(sheet_key, ""),
                "ok": len(failure_list) == 0,
                "message": f"成功：{len(success_list)}，失败：{len(failure_list)}",
                "data": {
                    "success": len(success_list),
                    "failure": len(failure_list),
                    "total": __number,
                    "successList": success_list,
                    "failureList": failure_list
                }
            })

        message_model.success = json.dumps(success_map, ensure_ascii=False)
        message_model.failure = json.dumps(failure_map, ensure_ascii=False)
        message_model.robot = robot_model.md5
        message_model.number = (message_model.number or 0) + __number
        message_model.update_rtx = rtx_id
        message_model.update_time = get_now()
        await self.salary_dtalk_message_curd.update(db=self.db, model=message_model)

        return SuccessStatus(
            message=f"重发完成，成功 {len(resent_ok)} 人，仍失败 {len(resent_fail)} 人",
            data=__results
        )