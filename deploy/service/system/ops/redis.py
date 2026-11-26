# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    service of system ops redis

base_info:
    __author__ = PyGo
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = redis.py

usage:

design:
    清理规则由后台数据库配置，前端只传递规则MD5；
    匹配方式取自系统枚举 redis-match，后端读取规则与Redis连接配置后执行预览/清理。

reference urls:

python version:
    python3


Enjoy the good life every day！！！
Life is short, I use python.

------------------------------------------------
"""
import re
from types import SimpleNamespace
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from sqlalchemy.ext.asyncio import AsyncSession

from deploy.curd.xtb_redis_config import XtbRedisConfigCurd
from deploy.curd.xtb_redis_rule import XtbRedisRuleCurd
from deploy.curd.csb_enum_value import CsbEnumValueCurd
from deploy.delib.redis_lib import RedisClientLib
from deploy.schema.dao.xtb_redis_config import XtbRedisConfigModel
from deploy.schema.dao.xtb_redis_rule import XtbRedisRuleModel
from deploy.schema.dto.xtb_redis import (
    xtb_redis_config_list_fields,
    xtb_redis_config_detail_fields,
    xtb_redis_rule_list_fields,
    xtb_redis_rule_detail_fields,
)
from deploy.service.system.config.report import SystemConfigReportService
from deploy.service.system.config.dict import SystemConfigDictService
from deploy.utils.status import Status, SuccessStatus, FailureStatus
from deploy.utils.status_value import StatusCode as status_code
from deploy.utils.converter import model_converter_dict, many_model_converter_dict
from deploy.utils.enumeration import XtbReportKey, CsbEnumKEY
from deploy.utils.logger import logger as LOG
from deploy.utils.utils import get_now, d2s, md5 as generator_md5
from deploy.config import table_default_null as TABLE_DEFAULT_NULL


__all__ = ["SystemOpsRedisService"]


# 匹配方式可选值（枚举 redis-match 的 key）
MATCH_KEYS: Tuple = ("prefix", "pattern", "regex")


class SystemOpsRedisService:

    def __init__(self, db_connection: AsyncSession):
        self.db: AsyncSession = db_connection
        self.config_curd: XtbRedisConfigCurd = XtbRedisConfigCurd()
        self.rule_curd: XtbRedisRuleCurd = XtbRedisRuleCurd()
        self.enum_curd: CsbEnumValueCurd = CsbEnumValueCurd()
        self.report_service: SystemConfigReportService = SystemConfigReportService(db_connection=db_connection)
        self.dict_service: SystemConfigDictService = SystemConfigDictService(db_connection=db_connection)

    def __str__(self):
        return "SystemOpsRedisService class."

    def __repr__(self):
        return self.__str__()

    # ======================== 公共方法 ========================

    async def __config_map(self) -> Dict[str, XtbRedisConfigModel]:
        models = await self.config_curd.list_all(db=self.db) or []
        return {m.md5: m for m in models}

    async def __valid_rule(self, md5: str, status_check: bool = True) -> Tuple[bool, Any]:
        if not md5:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少规则MD5参数")
        model = await self.rule_curd.get_by_md5(db=self.db, md5=md5)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if status_check and model.status:
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT)
        return True, model

    async def __valid_config(self, md5: str, status_check: bool = True) -> Tuple[bool, Any]:
        if not md5:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="缺少配置MD5参数")
        model = await self.config_curd.get_by_md5(db=self.db, md5=md5)
        if not model:
            return False, FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST, message="Redis连接配置不存在")
        if status_check and model.status:
            return False, FailureStatus(code=status_code.CODE_503_DATA_DELETE_NOT_EDIT.value)
        return True, model

    @staticmethod
    def __client(config: XtbRedisConfigModel) -> RedisClientLib:
        return RedisClientLib(
            host=config.host,
            port=int(config.port or 6379),
            db=int(config.db or 0),
            password=config.password or None,
            socket_timeout=5,
            socket_connect_timeout=5,
            decode_responses=True,
        )

    def __build_scan(self, rule: XtbRedisRuleModel) -> Tuple[bool, Any]:
        """根据后台规则生成扫描条件，返回 (是否合法, (匹配表达式, 正则对象, 最大数量))"""
        match_value = (getattr(rule, "match", None) or "prefix").lower()
        pattern = (rule.pattern or "").strip()

        if match_value not in MATCH_KEYS:
            return False, FailureStatus(code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR, message="不支持的匹配方式")
        if not pattern:
            return False, FailureStatus(code=status_code.CODE_400_REQUEST_PARAMETER_MISS, message="规则未配置键匹配内容")

        # 禁止无范围的全库扫描/清理
        if match_value in ("prefix", "pattern") and pattern in ("*", "**", ":*"):
            return False, FailureStatus(code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR, message="禁止清理全库缓存，请配置具体的键前缀或匹配表达式")
        if match_value == "regex" and pattern in (".*", "^.*$", ".+"):
            return False, FailureStatus(code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR, message="禁止使用匹配全部键的正则表达式")

        regex = None
        if match_value == "regex":
            try:
                regex = re.compile(pattern)
            except re.error as e:
                return False, FailureStatus(code=status_code.CODE_404_REQUEST_PARAMETER_VALUE_ERROR, message=f"正则表达式不合法：{e}")
            scan_pattern = "*"
        elif match_value == "prefix":
            scan_pattern = f"{pattern}*"
        else:
            scan_pattern = pattern

        max_keys = max(1, min(int(rule.max_keys or 1000), 100000))
        return True, (scan_pattern, regex, max_keys)

    @staticmethod
    def __match_key(key: str, regex) -> bool:
        return True if regex is None else bool(regex.search(key))

    @staticmethod
    def __collect_keys(conn, scan_pattern: str, regex, max_keys: int) -> List[str]:
        keys: List[str] = []
        for key in conn.scan_iter(match=scan_pattern, count=500):
            if not SystemOpsRedisService.__match_key(key, regex):
                continue
            keys.append(key)
            if len(keys) >= max_keys:
                break
        return keys

    # ======================== Redis配置 ========================

    async def config_list(self, content: str = None) -> Status:
        """
        不分页，直接获取全部数据
        """
        models = await self.config_curd.list_all(db=self.db, content=content) or []
        data = await many_model_converter_dict(
            models=models, fields=xtb_redis_config_list_fields,
            default_value=TABLE_DEFAULT_NULL, auto_id=False,
        )
        return SuccessStatus(data={"list": data or [], "total": len(models)})

    async def config_options(self) -> Status:
        return SuccessStatus(data=await self.__redis_config_options())

    async def config_one(self, md5: str) -> Status:
        flag, data = await self.__valid_config(md5=md5, status_check=False)
        if not flag: return data
        result = await model_converter_dict(
            model=data, fields=xtb_redis_config_detail_fields, default_value=TABLE_DEFAULT_NULL
        )
        return SuccessStatus(data=result)

    async def config_add(self, rtx_id: str, model: Dict) -> Status:
        if await self.config_curd.get_by_name(db=self.db, name=model.get("name")):
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD, message="配置名称已存在，请更换")
        new_model = await self.config_curd.new_model()
        now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('name')}-{d2s(now)}-{rtx_id}")
        new_model.create_time = now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.config_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def config_update(self, rtx_id: str, model: Dict) -> Status:
        flag, data = await self.__valid_config(md5=model.get("md5"))
        if not flag: return data
        model.pop("md5", None)
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.config_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def config_delete(self, rtx_id: str, md5: str) -> Status:
        flag, data = await self.__valid_config(md5=md5)
        if not flag: return data
        rules = await self.rule_curd.pagination(db=self.db, filter_={"redisMd5": md5}, limit=1)
        if rules:
            return FailureStatus(code=status_code.CODE_510_DATA_CONTAIN_SUB_DATA_NOT_DELETE, message="该配置已被清理规则引用，请先删除相关规则")
        data.status = True
        data.delete_rtx = rtx_id
        data.delete_time = get_now()
        await self.config_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def config_test(self, model: Dict) -> Status:
        """测试连接：使用前端提交的连接参数（不落库）"""
        config: XtbRedisConfigModel = XtbRedisConfigModel()
        for key in ("host", "port", "db", "password"):
            setattr(config, key, model.get(key))
        try:
            client = self.__client(config)
            if not client.ping():
                return FailureStatus(code=status_code.CODE_902_OTHER_THREE_API_EXCEPTION, message="Redis连接失败")
            with client.get_connection() as conn:
                dbsize = conn.dbsize()
            return SuccessStatus(data={"dbsize": dbsize, "host": config.host, "port": config.port, "db": config.db})
        except Exception as e:
            LOG.error(f"[SystemOpsRedisService*测试连接]{e}")
            return FailureStatus(code=status_code.CODE_902_OTHER_THREE_API_EXCEPTION, message=f"Redis连接失败：{e}")

    async def ping(self, md5: str = None) -> Status:
        """PING检测：指定配置或全部启用配置，逐项返回连通结果"""
        if md5:
            flag, data = await self.__valid_config(md5=md5, status_check=False)
            if not flag: return data
            configs: list[Any] = [data]
        else:
            configs: list[Any] = [
                m for m in (await self.config_curd.list_all(db=self.db) or [])
                if not m.lock
            ]

        results: List[Dict] = []
        for config in configs:
            item: Dict = {
                "md5": config.md5, "name": config.name, "host": config.host,
                "port": config.port, "db": config.db, "ok": False,
                "dbsize": 0, "message": ""
            }
            try:
                client: RedisClientLib = self.__client(config)
                ok: bool = bool(client.ping())
                with client.get_connection() as conn:
                    dbsize = conn.dbsize()
                item.update(ok=ok, dbsize=dbsize, message="PONG" if ok else "PING无响应")
            except Exception as e:
                item["message"] = str(e)
            results.append(item)

        success = sum(1 for item in results if item["ok"])
        return SuccessStatus(data={
            "list": results, "total": len(results), "success": success,
            "failed": len(results) - success,
        })

    # ======================== 清理规则 ========================

    async def __redis_config_options(self) -> List:
        models: List[XtbRedisConfigModel] = await self.config_curd.list_all(db=self.db) or []
        __res: list[Dict] = []
        for m in models:
            if not m or getattr(m, "lock", False): continue
            __res.append({"label": m.name, "value": m.md5, "disabled": bool(m.lock)})
        else:
            return __res

    async def filter_(self) -> Status:
        return SuccessStatus(data={
            "config": await self.__redis_config_options(),
            "match": await self.dict_service.dict_value_by_name_money(
                name=CsbEnumKEY.REDIS_MATCH.value,
                response_="option",
                filter_lock=True
            ) or [],
        })

    async def pagination(self, rtx_id: str, params: Dict) -> Status:
        offset = (int(params.get("page", 1)) - 1) * int(params.get("pageSize", 15))
        limit = int(params.get("pageSize", 15))
        filter_ = params.get("filter") or {}
        models = await self.rule_curd.pagination(db=self.db, offset=offset, limit=limit, filter_=filter_) or []
        default_data = {"list": [], "page": params.get("page"), "pageSize": params.get("pageSize"), "total": 0}
        if not models:
            return FailureStatus(code=status_code.CODE_101_SUCCESS_NO_DATA.value, data=default_data)

        fields = await self.report_service.report_column_by_xtbb(
            rtx_id=rtx_id, xtbb=XtbReportKey.SystemOpsRedis.value, type_="list", is_md5=True
        )
        if fields:
            columns = fields.get("column")
            auto_id = fields.get("id_auto")
        else:
            # 未配置报表时仍可正常使用（与后台报表配置解耦）
            columns = xtb_redis_rule_list_fields
            auto_id = False

        # 联表查询返回 RowMapping，转换为支持属性访问的对象供转换器使用
        models = [SimpleNamespace(**dict(row)) for row in models]
        config_map = await self.__config_map()
        for model in models:
            config = config_map.get(model.redis_md5)
            setattr(model, "config_name", config.name if config else "配置已删除")

        data = await many_model_converter_dict(
            models=models, fields=columns, default_value=TABLE_DEFAULT_NULL,
            auto_id=auto_id, auto_id_value=offset + 1,
        )
        result = {
            "list": data or [],
            "page": params.get("page"),
            "pageSize": params.get("pageSize"),
            "total": await self.rule_curd.count(db=self.db, filter_=filter_),
        }
        return SuccessStatus(data=result)

    async def rule_one(self, md5: str) -> Status:
        flag, data = await self.__valid_rule(md5=md5, status_check=False)
        if not flag: return data
        config_map = await self.__config_map()
        config = config_map.get(data.redis_md5)
        setattr(data, "config_name", config.name if config else "配置已删除")
        result = await model_converter_dict(model=data, fields=xtb_redis_rule_detail_fields)
        return SuccessStatus(data=result)

    async def rule_add(self, rtx_id: str, model: Dict) -> Status:
        if await self.rule_curd.get_by_name(db=self.db, name=model.get("name")):
            return FailureStatus(code=status_code.CODE_502_DATA_EXIST_NOT_ADD, message="规则名称已存在，请更换")
        flag, config = await self.__valid_config(md5=model.get("redis_md5"))
        if not flag: return config
        new_model = await self.rule_curd.new_model()
        now = datetime.now()
        new_model.md5 = generator_md5(v=f"{model.get('name')}-{d2s(now)}-{rtx_id}")
        new_model.create_time = now
        new_model.create_rtx = rtx_id
        new_model.status = False
        for k, v in model.items():
            setattr(new_model, k, v)
        await self.rule_curd.add(db=self.db, model=new_model)
        return SuccessStatus()

    async def rule_update(self, rtx_id: str, model: Dict) -> Status:
        flag, data = await self.__valid_rule(md5=model.get("md5"))
        if not flag: return data
        conf_flag, config = await self.__valid_config(md5=model.get("redis_md5"))
        if not conf_flag: return config
        model.pop("md5", None)
        model["update_rtx"] = rtx_id
        model["update_time"] = get_now()
        for k, v in model.items():
            setattr(data, k, v)
        await self.rule_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def rule_delete(self, rtx_id: str, md5: str) -> Status:
        flag, data = await self.__valid_rule(md5=md5)
        if not flag: return data
        data.status = True
        data.delete_rtx = rtx_id
        data.delete_time = get_now()
        await self.rule_curd.update(db=self.db, model=data)
        return SuccessStatus()

    async def rule_batch_delete(self, rtx_id: str, md5_list: List[str]) -> Status:
        models = await self.rule_curd.get_models_by_md5_list(db=self.db, md5_list=md5_list) or []
        if not models:
            return FailureStatus(code=status_code.CODE_501_DATA_NOT_EXIST)
        if len(models) != len(md5_list):
            return FailureStatus(code=status_code.CODE_508_DATA_PART_DELETE,
                                 message=f"总数{len(md5_list)}，实际删除{len(models)}")
        await self.rule_curd.batch_soft_delete_update(db=self.db, md5_list=md5_list, rtx_id=rtx_id)
        return SuccessStatus()

    async def rule_lock(self, rtx_id: str, params: Dict) -> Status:
        flag, data = await self.__valid_rule(md5=params.get("md5"))
        if not flag: return data
        data.lock = bool(params.get("value"))
        data.update_rtx = rtx_id
        data.update_time = get_now()
        await self.rule_curd.update(db=self.db, model=data)
        return SuccessStatus()

    # ======================== 预览与清理 ========================

    async def __prepare(self, md5: str) -> Tuple[bool, Any]:
        flag, rule = await self.__valid_rule(md5=md5)
        if not flag: return flag, rule
        if rule.lock:
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT, message="规则已停用，请先启用后再操作")
        conf_flag, config = await self.__valid_config(md5=rule.redis_md5)
        if not conf_flag: return conf_flag, config
        if config.lock:
            return False, FailureStatus(code=status_code.CODE_511_DATA_LOCKED_NOT_EDIT, message="Redis连接配置已停用，请先启用")
        valid, scan = self.__build_scan(rule)
        if not valid: return valid, scan
        return True, (rule, config, scan)

    async def preview(self, md5: str) -> Status:
        flag, data = await self.__prepare(md5)
        if not flag: return data
        rule, config, (scan_pattern, regex, max_keys) = data
        try:
            client = self.__client(config)
            with client.get_connection() as conn:
                keys = self.__collect_keys(conn, scan_pattern, regex, max_keys)
            return SuccessStatus(data={
                "rule": rule.name, "config": config.name, "count": len(keys),
                "match": scan_pattern, "sample": keys[:20], "maxKeys": max_keys,
            })
        except Exception as e:
            LOG.error(f"[SystemOpsRedisService*预览]{e}")
            return FailureStatus(code=status_code.CODE_902_OTHER_THREE_API_EXCEPTION, message=f"Redis预览失败：{e}")

    async def clean(self, rtx_id: str, md5: str) -> Status:
        flag, data = await self.__prepare(md5)
        if not flag: return data
        rule, config, (scan_pattern, regex, max_keys) = data
        try:
            client = self.__client(config)
            affected = 0
            sample: List[str] = []
            with client.get_connection() as conn:
                keys = self.__collect_keys(conn, scan_pattern, regex, max_keys)
                sample = keys[:20]
                if keys:
                    with client.pipeline(transaction=False) as pipe:
                        for i in range(0, len(keys), 100):
                            pipe.delete(*keys[i:i + 100])
                        results = pipe.execute()
                        affected = sum(int(r or 0) for r in results)

            rule.last_clean_time = get_now()
            rule.last_clean_count = affected
            rule.update_rtx = rtx_id
            rule.update_time = get_now()
            await self.rule_curd.update(db=self.db, model=rule)
            LOG.info(f"[SystemOpsRedisService*清理] 规则[{rule.name}] 键数[{affected}] 操作人[{rtx_id}]")
            return SuccessStatus(data={
                "rule": rule.name, "config": config.name, "count": affected, "sample": sample,
            })
        except Exception as e:
            LOG.error(f"[SystemOpsRedisService*清理]{e}")
            return FailureStatus(code=status_code.CODE_902_OTHER_THREE_API_EXCEPTION, message=f"Redis清理失败：{e}")
