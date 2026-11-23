# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe:
    SMTP 邮件发送封装

base_info:
    __author__ = PyGo
    __time__ = 2026/11/23 10:00
    __version__ = v.1.0.0
    __project__ = fastslot-api-salary
    __file_name__ = email_lib.py

python version:
    python3

------------------------------------------------
"""
import re
import smtplib
import ssl
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Dict, Optional, Tuple

from deploy.utils.logger import logger as LOG


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class EmailLib:
    """轻量 SMTP 客户端，按单个收件人发送以便统计成功/失败名单"""

    def __init__(self, smtp_server: str, password: str, sender: str):
        host, port = self.__parse_server(smtp_server)
        self.host: str = host
        self.port: int = port
        self.password: str = password or ""
        self.sender: str = sender or ""
        self.server: Optional[smtplib.SMTP] = None

    @staticmethod
    def __parse_server(value: str) -> Tuple[str, int]:
        raw = (value or "").strip()
        if ":" in raw:
            host, _, port_text = raw.rpartition(":")
            try:
                return host.strip(), int(port_text.strip())
            except Exception:
                return host.strip(), 465
        return raw, 465

    def connect(self) -> bool:
        if not self.host or not self.sender or not self.password:
            return False
        try:
            if self.port == 465:
                self.server = smtplib.SMTP_SSL(
                    self.host, self.port, timeout=30, context=ssl.create_default_context())
            else:
                self.server = smtplib.SMTP(self.host, self.port, timeout=30)
                self.server.starttls(context=ssl.create_default_context())
            self.server.login(self.sender, self.password)
            return True
        except Exception as e:
            LOG.error(f"[EmailLib]SMTP连接失败：{e}")
            self.close()
            return False

    @property
    def connected(self) -> bool:
        return self.server is not None

    def send_mail(self, to: str, subject: str, html: str) -> bool:
        recipient = (to or "").strip()
        if not _EMAIL_RE.match(recipient):
            LOG.warning(f"[EmailLib]收件邮箱格式不正确：{recipient}")
            return False
        if not self.server:
            return False
        try:
            message = MIMEText(html or "", "html", "utf-8")
            message["From"] = formataddr((str(Header("工资通知", "utf-8")), self.sender))
            message["To"] = recipient
            message["Subject"] = Header(subject or "工资通知", "utf-8")
            self.server.sendmail(self.sender, [recipient], message.as_string())
            return True
        except Exception as e:
            LOG.error(f"[EmailLib]邮件发送失败：to={recipient}, error={e}")
            return False

    def close(self) -> None:
        if not self.server:
            return
        try:
            self.server.quit()
        except Exception:
            try:
                self.server.close()
            except Exception:
                pass
        finally:
            self.server = None

    @staticmethod
    def build_html(title: str, content: Dict) -> str:
        rows = []
        for key, value in (content or {}).items():
            if key in ("id", "id_", "邮箱", "email", "Email") or value in (None, ""):
                continue
            if isinstance(value, float):
                value = round(value, 2)
            text = str(value).replace("\n", "<br/>")
            rows.append(
                '<tr><td style="padding:6px 10px;border:1px solid #e6e6e6;color:#666;">'
                f'{key}</td><td style="padding:6px 10px;border:1px solid #e6e6e6;color:#333;">{text}</td></tr>'
            )
        body = "".join(rows) or '<tr><td colspan="2" style="padding:10px;color:#999;">无内容</td></tr>'
        return (
            '<div style="font-family:Arial,\'Microsoft YaHei\';font-size:14px;color:#333;">'
            f'<h3 style="margin:0 0 12px;">{title}</h3>'
            f'<table style="border-collapse:collapse;width:100%;max-width:720px;">{body}</table>'
            '<p style="color:#999;font-size:12px;margin-top:12px;">本邮件由系统自动发送，请勿直接回复。</p>'
            '</div>'
        )
