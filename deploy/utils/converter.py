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


__all__ = [
    "model_converter_dict",
    "many_model_converter_dict",
    "option_converter_dict",
    "menu_converter_dict",
]


async def model_converter_dict(
        model: Any,
        fields: List[Dict] = None,
        default_value: str = "-"
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
        default_value (str): 当模型属性为空时使用的默认值，默认为 "-".

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
        raw_value = getattr(model, field_key, "")
        # 显式判断 None 来决定是否使用默认值
        field_value = raw_value if raw_value is not None or field_null \
            else default_value
        if field_value is None: field_value = ""
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
                    model_dict[field_name] = "是" if bool(field_value) else "否"
                case "user_status_text":
                    model_dict[field_name] = "注销" if bool(field_value) else "启用"
                case "lock_text":
                    model_dict[field_name] = "锁定" if bool(field_value) else "正常"
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


async def many_model_converter_dict(
        models: Any,
        fields: List[Dict] = None,
        default_value: str = "-",
        auto_id: bool = True,
        auto_id_value: int = 1,
        *args,
        **kwargs
) -> Optional[List[Dict]]:
    """
    批量数据模型转Dict，新增了自增id满足是否添加ID序号需求
    """
    if (not models
            or not fields):
        return None

    _model_list = list()
    if auto_id:
        for model in models:
            if not model: continue
            model_dict = await model_converter_dict(
                model=model,
                fields=fields,
                default_value=default_value
            )
            if not model_dict: continue
            model_dict["id"] = auto_id_value
            auto_id_value += 1
            _model_list.append(model_dict)
        else:
            return _model_list
    else:
        for model in models:
            if not model: continue
            model_dict = await model_converter_dict(
                model=model,
                fields=fields,
                default_value=default_value
            )
            if not model_dict: continue
            _model_list.append(model_dict)
        else:
            return _model_list


async def option_converter_dict(
        models: Any,
        key_trans_int: bool = False,
        lock_view: bool = False,
        *args,
        **kwargs
) -> Optional[List[Dict]]:
    """
    csb_enum_value数据模型对象转换为Select-Option格式
    [
        {"label": x, "value": y, "disabled": z},
    ]
    :param models: model list
    :param key_trans_int: 是否key为整型，默认False
    :param lock_view: 是否key为整型，默认False
    :return: list
    """
    if not models: return None

    _res: List = []
    for item in models:
        if not item: continue
        if not lock_view and getattr(item, "lock", None) : continue  # 锁定不显示

        key = int(getattr(item, "key")) if key_trans_int else getattr(item, "key")
        _res.append({
            "label": getattr(item, "value"),
            "value": key,
            "disabled": getattr(item, "lock")
        })
    else:
        return _res


def menu_converter_dict(model, type_: str = 'base', format_: str = "tree") -> dict:
    """
    菜单字典化
    :param model: model
    :param type_:
    :param format_: tree：菜单树格式 flat：扁平化菜单
    :return: dict
    """
    if not model:
        return {}

    __xtb_menu_base_attrs = ['id', 'name', 'path', 'pid', 'level', 'md5', 'component', 'type', 'link', 'redirect', 'order_id']
    __xtb_menu_meta_attrs = ['title', 'icon', 'cache', 'affix', 'full', 'hidden', 'tag', 'breadcrumb']
    __xtb_menu_extend_attrs = ['create_time', 'create_rtx', 'delete_time', 'delete_rtx', 'status']
    __xtb_menu_extend_attrs = ['create_time', 'create_rtx', 'delete_time', 'delete_rtx', 'status']

    if type_ == 'base':
        attrs = __xtb_menu_base_attrs
    elif type_ == 'list':
        attrs = __xtb_menu_base_attrs + __xtb_menu_extend_attrs
    elif type_ == 'detail':
        attrs = __xtb_menu_base_attrs + __xtb_menu_meta_attrs
    elif type_ == 'all':
        attrs = __xtb_menu_base_attrs + __xtb_menu_meta_attrs + __xtb_menu_extend_attrs
    else:
        attrs = __xtb_menu_base_attrs
    # 去重
    attrs = list(set(attrs))

    _res = dict()
    _meta = dict()

    def __tree():
        for attr in attrs:
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
                _res["md5"] = model.md5
            elif attr == 'order_id':
                _res[attr] = model.order_id
            elif attr == 'component':
                _res[attr] = model.component
            elif attr == 'redirect':
                _res[attr] = model.redirect
            # > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
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
        else:
            _res['meta'] = _meta
            return _res

    def __flat():
        for attr in attrs:
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
                _res["md5"] = model.md5
            elif attr == 'order_id':
                _res[attr] = model.order_id
            elif attr == 'component':
                _res[attr] = model.component
            elif attr == 'redirect':
                _res[attr] = model.redirect
            # > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > >
            elif attr == 'type':
                # 此菜单类型，MENU=菜单，LINK=外链，BUTTON=按钮
                _res[attr] = model.type or "MENU"
            elif attr == 'title':
                # 菜单标题
                _res[attr] = model.title
            elif attr == 'icon':
                # 菜单图标
                _res[attr] = model.icon
            elif attr == 'cache':
                # 是否缓存路由
                _res["isKeepAlive"] = True if model.cache else False
            elif attr == 'affix':
                # 菜单是否固定在标签页中 (首页通常是固定项)
                _res["isAffix"] = True if model.affix else False
            elif attr == 'full':
                # 菜单是否全屏 (示例：数据大屏页面)
                _res["isFull"] = True if model.full else False
            elif attr == 'hidden':
                # 是否在菜单中隐藏
                _res["isHide"] = True if model.hidden else False
            elif attr == 'breadcrumb':
                # 是否在面包屑菜单中显示
                _res["isBreadcrumb"] = True if model.breadcrumb else False
            elif attr == 'tag':
                _res[attr] = model.tag
        else:
            return _res

    return __tree() if format_ == "tree" else __flat()
