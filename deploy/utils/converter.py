# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    转换器

base_info:
    __author__ = PyGo
    __time__ = 2025/12/17 22:04
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = converter.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import datetime
from typing import Any, List, Dict, Optional


async def model_converter_dict(
        model: Any,
        fields: List[Dict] = None,
        default_value: Any = "-"
) -> Optional[Dict[str, Any]]:
    """
    异步函数：将模型对象根据字段定义转换为字典格式。

    参数:
        model (Any): 要转换的模型对象，通常是一个包含属性的对象实例。
        fields (List[Dict], optional): 字段配置列表，每个元素是包含 'key'、'type'、'name' 和 'null' 键的字典。
                                       - key: 模型中的属性名
                                       - type: 属性的数据类型（如 "str", "int", "datetime" 等）
                                       - name: 输出字典中对应的键名
                                       - null: 是否允许为空，默认设置False，值为空自动会添加默认值
        demo：
            xtb_user_list_fields = [
                {"key": "id", "type": "int", "name": "id", "null": False},
                {"key": "rtx_id", "type": "str", "name": "rtxId", "null": False},
                {"key": "md5_id", "type": "str", "name": "md5Id", "null": False},
            ]
        default_value (Any, optional): 当模型属性为空时使用的默认值，默认为 "-".

    返回:
        Dict[str, Any]: 转换后的字典，键为字段定义中的 name，值为对应类型的转换结果。
    """
    if (not model
            or not fields):
        return None


    # 验证字段有效性
    valid_fields: List = []
    for field in fields:
        key: str = field.get("key")
        type_: str = field.get("type")
        name: str = field.get("name")
        null: bool = field.get("null")

        if not key: continue  # 忽略无效字段定义
        __name: str = key if not name else name  # 为空默认取key
        __type: str = type_ if type_ else "str"  # 为空默认为字符串格式
        __null: bool = True if null else False   # True允许为空 False不允许为空
        valid_fields.append((key, __type, __name, __null))

    model_dict: Dict = {}
    for field_key, field_type, field_name, field_null in valid_fields:
        raw_value = getattr(model, field_key, None)
        # 显式判断 None 来决定是否使用默认值
        field_value = raw_value if raw_value is not None or field_null \
            else default_value
        try:
            match field_type:
                case "str":
                    model_dict[field_name] = str(field_value)
                case "int":
                    model_dict[field_name] = int(field_value)
                case "float":
                    model_dict[field_name] = float(field_value)
                case "bool":
                    model_dict[field_name] = bool(field_value)
                case "bool_text":
                    # field_name保留原有字段信息，新增field_name+TEXT存储对应的布尔中文值
                    model_dict[field_name] = bool(field_value)
                    model_dict[f"{field_name}Text"] = "是" if bool(field_value) else "否"
                case "datetime" | "date" | "time" if isinstance(field_value, (datetime.datetime, datetime.date)):
                    fmt_map = {
                        "datetime": "%Y-%m-%d %H:%M:%S",
                        "date": "%Y-%m-%d",
                        "time": "%H:%M:%S"
                    }
                    model_dict[field_name] = field_value.strftime(fmt_map[field_type])
                case "timestamp" if hasattr(field_value, 'timestamp'):
                    model_dict[field_name] = field_value.timestamp()
                case "list":
                    model_dict[field_name] = list(field_value)
                case "dict":
                    model_dict[field_name] = dict(field_value)
                case "split_list":
                    model_dict[field_name] = [str(x) for x in field_value.split(",")] if field_value else []
                case _:
                    model_dict[field_name] = str(field_value)
        except:
            model_dict[field_name] = str(field_value)

    return model_dict
