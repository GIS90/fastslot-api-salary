# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    企业微信消息通知（应用消息 API 封装）

base_info:
    __author__ = PyGo
    __time__ = 2025/12/7 22:01
    __version__ = v.1.0.1
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo.space
    __project__ = fastslot-api-salary
    __file_name__ = qywx_lib.py

usage:
    qywx_lib = QYWXMessageLib(corp_id=企业号标识, secret=应用凭证密钥, agent_id=应用ID)
    qywx_lib.send(to_user=['userid1'], content={'data': '消息内容'}, stype='markdown')

    初始化必须的参数：
        - corp_id:  企业号标识（CorpID）
        - secret:   应用凭证密钥（Secret）
        - agent_id: 企业应用ID（AgentId）

design:
    基于 requests 模拟 API 请求，主要实现：
        - ACCESS TOKEN：认证 token 获取（带缓存，有效期内复用）
        - SEND MESSAGE：发送应用消息
        - RECALL MESSAGE：撤回消息
        - TEMP MEDIA：临时素材上传

reference urls:
    - ACCESS TOKEN：https://developer.work.weixin.qq.com/document/path/91039
    - 发送应用消息：https://developer.work.weixin.qq.com/document/path/90236
    - 全局错误码：https://developer.work.weixin.qq.com/document/path/90313
    - 上传临时素材：https://developer.work.weixin.qq.com/document/path/90253
    - MARKDOWN语法：https://developer.work.weixin.qq.com/document/path/90236

    企业微信 API response：
    {
      "errcode": 0, "errmsg": "ok",
      "invaliduser": "userid1|userid2",
      "invalidparty": "partyid1|partyid2",
      "invalidtag": "tagid1|tagid2",
      "unlicenseduser": "userid3|userid4",
      "msgid": "xxxx", "response_code": "xyzxyz"
    }

python version:
    python3

------------------------------------------------
"""
import os
import time
import threading
from typing import Any, ClassVar, Dict, List, Optional, Tuple
from urllib.parse import quote

from deploy.delib.http_lib import HttpLibApi
from deploy.utils.status import SuccessStatus, FailureStatus
from deploy.config import (qywx_base, qywx_token_api, qywx_send_api,
                           qywx_recall_api, qywx_upload_api, qywx_temp_api)
from deploy.utils.utils import get_file_size
from deploy.utils.logger import logger as LOG


QYWX_BASE_URL: str = qywx_base
QYWX_ACCESS_TOKEN: str = qywx_token_api
QYWX_SEND_MESSAGE: str = qywx_send_api
QYWX_SEND_BACK: str = qywx_recall_api
QYWX_TEMP_UPLOAD: str = qywx_upload_api
QYWX_TEMP_GET: str = qywx_temp_api


class QYWXMessageLib:
    """企业微信应用消息客户端"""

    types: ClassVar[List[str]] = [
        'text',         # 文本
        'image',        # 图片消息
        'voice',        # 语音消息
        'video',        # 视频消息
        'file',         # 文件消息
        'textcard',     # 文本卡片消息
        'news',         # 图文消息
        'mpnews',       # 多图文消息
        'markdown',     # markdown消息
        'miniprogram_notice',                     # 小程序通知消息
        'template_card@text_notice',              # 模板卡片 > 文本通知型
        'template_card@news_notice',              # 模板卡片 > 图文展示型
        'template_card@button_interaction',       # 模板卡片 > 按钮交互型
        'template_card@vote_interaction',         # 模板卡片 > 投票选择型
        'template_card@multiple_interaction',     # 模板卡片 > 多项选择型
    ]

    safe_kwargs_types: ClassVar[List[str]] = [
        'text', 'image', 'video', 'file', 'mpnews'
    ]

    enable_id_trans_kwargs_types: ClassVar[List[str]] = [
        'text', 'textcard', 'news', 'mpnews', 'miniprogram_notice',
        'template_card@text_notice', 'template_card@news_notice',
        'template_card@button_interaction', 'template_card@vote_interaction',
        'template_card@multiple_interaction',
    ]

    content_types: ClassVar[List[str]] = ['text', 'markdown']

    temp_upload_types: ClassVar[List[str]] = ['image', 'voice', 'video', 'file']

    temp_upload_types_verify: ClassVar[Dict[str, Dict[str, Any]]] = {
        'image': {
            'suffix': ['.jpg', '.jpeg', '.png'],
            'size': 10 * 1024 * 1024
        },
        'voice': {
            'suffix': ['.amr'],
            'size': 2 * 1024 * 1024
        },
        'video': {
            'suffix': [
                '.wmv', '.asf', '.asx',       # 微软视频
                '.rm', '.rmvb',               # Real Player
                '.mp4',                       # MPEG视频
                '.3gp',                       # 手机视频
                '.m4v', '.mov',               # Apple视频
                '.mpg', '.mpeg', '.mpe',      # MPEG视频
                '.avi', '.dat', '.mkv', '.flv', '.vob'
            ],
            'size': 10 * 1024 * 1024
        },
        'file': {
            'suffix': [],
            'size': 20 * 1024 * 1024
        }
    }

    # access_token 缓存：{ corp_id + secret: (token, 过期时间戳) }
    _token_cache: ClassVar[Dict[str, Tuple[str, float]]] = {}
    _token_lock: ClassVar[threading.Lock] = threading.Lock()
    # 提前 5 分钟过期，避免边界时刻 token 失效
    TOKEN_EXPIRE_BUFFER: ClassVar[int] = 300

    def __init__(self, corp_id: str, secret: str, agent_id: str) -> None:
        """
        :param corp_id: 企业号标识
        :param secret: 应用凭证密钥
        :param agent_id: 企业应用ID
        """
        self.CORP_ID: str = corp_id
        self.SECRET: str = secret
        # 企业微信 API 要求 agentid 为整型，兼容字符串配置
        try:
            self.AGENT_ID: Any = int(agent_id)
        except (TypeError, ValueError):
            self.AGENT_ID = agent_id
        self.http = HttpLibApi(QYWX_BASE_URL)
        self.token: Optional[str] = self.__init_token()

    def __str__(self) -> str:
        return f"[QYWXMessageLib] corp_id: {self.CORP_ID}, agent_id: {self.AGENT_ID}"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def clear_token_cache(cls, corp_id: Optional[str] = None, secret: Optional[str] = None) -> None:
        """清除 token 缓存；不传参数时清空全部，传参时只清除对应应用"""
        with cls._token_lock:
            if corp_id is None:
                cls._token_cache.clear()
            else:
                cls._token_cache.pop(f"{corp_id}:{secret or ''}", None)

    def __init_token(self) -> Optional[str]:
        """获取 access_token，有效期内复用缓存避免频繁请求

        GET https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
        """
        cache_key = f"{self.CORP_ID}:{self.SECRET}"
        with self._token_lock:
            cached = self._token_cache.get(cache_key)
            if cached and cached[1] > time.time():
                return cached[0]

        params: Dict = {"corpid": self.CORP_ID, "corpsecret": self.SECRET}
        try:
            status, response = self.http.get_json(url=QYWX_ACCESS_TOKEN, params=params)
        except Exception as error:
            LOG.error(f"[QYWXMessageLib]获取token异常：{error}")
            return None

        if not status or not isinstance(response, dict):
            LOG.warning("[QYWXMessageLib]获取token请求失败")
            return None
        if response.get("errcode") != 0 or response.get("errmsg") != "ok":
            LOG.warning(f"[QYWXMessageLib]获取token失败：{response.get('errmsg')}")
            return None

        token = response.get("access_token")
        if not token:
            return None

        try:
            expires_in = int(response.get("expires_in") or 7200)
        except (TypeError, ValueError):
            expires_in = 7200
        with self._token_lock:
            self._token_cache[cache_key] = (
                token,
                time.time() + max(expires_in - self.TOKEN_EXPIRE_BUFFER, 60)
            )
        return token

    def check_token(self) -> bool:
        """access_token 是否可用"""
        return bool(self.token)

    def format_content(self, ftype: str = 'text', content: Optional[Dict] = None) -> Dict:
        """按消息类型格式化消息体内容"""
        if not content or ftype not in self.types:
            return {}
        data = content.get('data')
        if data is None or data == "":
            return {}
        if ftype in self.content_types:
            # text/markdown 的 content 必须是字符串；
            # 兼容误传 {"title":..., "text":...} 的情况（钉钉消息体格式）
            if isinstance(data, dict):
                data = data.get('text') or data.get('content') or ''
            return {'content': str(data)}
        if ftype in self.temp_upload_types:
            return {'media_id': data}
        return {}

    @staticmethod
    def _validate_switch(kwargs: Dict, key: str, default: int = 0) -> Tuple[Optional[int], str]:
        """校验只允许 0/1 的开关参数"""
        value = kwargs.get(key, default)
        if value is None:
            value = default
        if value not in (0, 1):
            return None, f'[QYWXMessageLib]{key}参数值不合法，只允许0或者1'
        return value, ''

    def send(self, to_user: Optional[List] = None, to_party: Optional[List] = None,
             to_tag: Optional[List] = None, content: Optional[Dict] = None,
             stype: str = 'text', **kwargs) -> str:
        """发送应用消息

        :param to_user: 成员ID列表，最多100个；"@all"表示全部成员
        :param to_party: 部门ID列表，最多100个
        :param to_tag: 标签ID列表，最多100个
        :param content: 消息体内容，形如 {'data': '...'}
        :param stype: 消息类型，默认 text
        :return: Status.json() 序列化字符串
        """
        if not self.token:
            return FailureStatus(903, '[QYWXMessageLib]TOKEN初始化失败', {}).json()
        if not any([to_user, to_party, to_tag]):
            return FailureStatus(400, '[QYWXMessageLib]缺少接收用户/部门列表', {}).json()
        if not content:
            return FailureStatus(400, '[QYWXMessageLib]缺少消息内容', {}).json()
        if stype not in self.types:
            return FailureStatus(404, '[QYWXMessageLib]消息类型错误', {}).json()

        switches: Dict[str, int] = {}
        for key in ('safe', 'enable_id_trans', 'enable_duplicate_check'):
            value, error = self._validate_switch(kwargs, key)
            if error:
                return FailureStatus(404, error, {}).json()
            switches[key] = value

        duplicate_check_interval = kwargs.get('duplicate_check_interval', 1800)
        if duplicate_check_interval is None:
            duplicate_check_interval = 1800
        if not isinstance(duplicate_check_interval, int) \
                or duplicate_check_interval < 1 or duplicate_check_interval > 4 * 60 * 60:
            return FailureStatus(
                404, '[QYWXMessageLib]duplicate_check_interval参数值不合法，只允许1秒至4小时之间', {}
            ).json()

        body = self.format_content(ftype=stype, content=content)
        if not body:
            return FailureStatus(404, '[QYWXMessageLib]格式化的消息体为空', {}).json()

        data = {
            "agentid": self.AGENT_ID,
            "msgtype": stype,
            stype: body,
            "enable_duplicate_check": switches['enable_duplicate_check'],
            "duplicate_check_interval": duplicate_check_interval
        }
        if to_user:
            data['touser'] = "|".join(to_user)
        if to_party:
            data['toparty'] = "|".join(to_party)
        if to_tag:
            data['totag'] = "|".join(to_tag)
        if stype in self.safe_kwargs_types:
            data['safe'] = switches['safe']
        if stype in self.enable_id_trans_kwargs_types:
            data['enable_id_trans'] = switches['enable_id_trans']

        try:
            url = "%s?access_token=%s" % (QYWX_SEND_MESSAGE, self.token)
            status, response = self.http.post_json(url=url, data=data)
            if not status or not isinstance(response, dict):
                return FailureStatus(902, '[QYWXMessageLib]发送消息请求失败', {}).json()
            if response.get("errcode") == 0 and response.get("errmsg") == "ok":
                return SuccessStatus(data=response).json()
            return FailureStatus(902, response.get('errmsg'), response).json()
        except Exception as error:
            LOG.error(f"[QYWXMessageLib]发送消息异常：{error}")
            return FailureStatus(902, "[QYWXMessageLib]发送消息异常，请稍后重试", {}).json()

    def sendback(self, message_id: str) -> str:
        """撤回 24 小时内发送的应用消息（仅企业微信端）"""
        if not self.token:
            return FailureStatus(903, '[QYWXMessageLib]TOKEN初始化失败', {}).json()
        if not message_id:
            return FailureStatus(400, '[QYWXMessageLib]缺少message_id参数', {}).json()

        try:
            url = "%s?access_token=%s" % (QYWX_SEND_BACK, self.token)
            status, response = self.http.post_json(url=url, data={"msgid": message_id})
            if not status or not isinstance(response, dict):
                return FailureStatus(902, '[QYWXMessageLib]撤回消息请求失败', {}).json()
            if response.get("errcode") == 0 and response.get("errmsg") == "ok":
                return SuccessStatus(data=response).json()
            return FailureStatus(902, response.get('errmsg'), response).json()
        except Exception as error:
            LOG.error(f"[QYWXMessageLib]撤回消息异常：{error}")
            return FailureStatus(902, "[QYWXMessageLib]撤回消息异常，请稍后重试", {}).json()

    def _verify_temp_upload_file(self, upload_type: str, upload_name: str, upload_file: str) -> Tuple[bool, str]:
        """校验临时素材的类型、后缀与大小"""
        rule = self.temp_upload_types_verify.get(upload_type)
        if not rule:
            return False, '无此类型文件校验'

        if not upload_name:
            upload_name = os.path.split(upload_file)[-1]
        if os.path.splitext(upload_name)[-1].lower() not in rule.get('suffix', []):
            return False, '文件格式不支持'
        if get_file_size(path=upload_file, unit='B') > rule.get('size', 0):
            return False, '文件超出大小限制'
        return True, ''

    def temp_upload(self, upload_type: str, upload_name: str, upload_file: str) -> str:
        """上传临时素材，返回 media_id（三天内有效）

        大小限制：图片10MB / 语音2MB / 视频10MB / 普通文件20MB
        """
        if not self.token:
            return FailureStatus(903, '[QYWXMessageLib]TOKEN初始化失败', {}).json()
        if not upload_type or upload_type not in self.temp_upload_types:
            return FailureStatus(404, '[QYWXMessageLib]upload_type参数不支持请求类型', {}).json()
        if not upload_file or not os.path.isfile(upload_file):
            return FailureStatus(450, '[QYWXMessageLib]缺少上传文件', {}).json()

        if not upload_name:
            upload_name = os.path.split(upload_file)[-1]
        verified, message = self._verify_temp_upload_file(upload_type, upload_name, upload_file)
        if not verified:
            return FailureStatus(454, message, {}).json()

        try:
            with open(upload_file, 'rb') as f:
                files_body = {'media': (upload_name, f.read(), 'text/plain')}
            url = "{}?access_token={}&type={}".format(QYWX_TEMP_UPLOAD, self.token, upload_type)
            headers = {
                'filename': quote(upload_name),
                'Content-type': 'multipart/form-data;'
            }
            status, response = self.http.post_form(url=url, headers=headers, files=files_body)
            if not status or not isinstance(response, dict):
                return FailureStatus(902, '[QYWXMessageLib]上传素材请求失败', {}).json()
            if response.get("errcode") == 0 and response.get("errmsg") == "ok":
                response['url'] = "{}{}?access_token={}&media_id={}".format(
                    QYWX_BASE_URL, QYWX_TEMP_GET, self.token, response.get('media_id')
                )
                return SuccessStatus(data=response).json()
            return FailureStatus(902, response.get('errmsg'), response).json()
        except Exception as error:
            LOG.error(f"[QYWXMessageLib]上传素材异常：{error}")
            return FailureStatus(902, "[QYWXMessageLib]文件上传异常，请稍后重试", {}).json()
