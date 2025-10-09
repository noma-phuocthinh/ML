# backend/controllers/function.py
import pymysql
import hashlib
import base64
import os
import re
from typing import Optional

# ========= Base MySQL theo flow bạn dùng =========
class MySQLBase:
    def __init__(self,
                 host="obesityapp.c5qusgeo4spw.ap-southeast-2.rds.amazonaws.com", port=3306,
                 database="ObesityApp", username="root", password="3141592653589793.",
                 charset="utf8mb4"):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.charset = charset
        self.conn = None
        self.cursor = None

    def connectMySQL(self):
        if self.conn and self.cursor:
            return
        self.conn = pymysql.connect(
            host=self.host, port=self.port,
            user=self.username, password=self.password,
            database=self.database, charset=self.charset,
            cursorclass=pymysql.cursors.Cursor,
            autocommit = True,  # ✅ giảm chờ commit round-trip
            connect_timeout = 3,  # ✅ fail nhanh nếu mạng kém
            read_timeout = 5, write_timeout = 5  # ✅ tránh treo dài
        )
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
        finally:
            try:
                if self.conn:
                    self.conn.close()
            except:
                pass

# ========= Exceptions dùng chung =========
class AppError(Exception): ...
class SignupValidationError(AppError): ...
class DuplicateFieldError(AppError):
    def __init__(self, fields: list[str]): self.fields = fields

class LoginValidationError(AppError): ...
class UnregisteredAccountError(AppError): ...
class WrongPasswordError(AppError): ...

# ========= Helpers dùng chung =========
def generate_salt(n_bytes: int = 16) -> str:
    """Tạo muối ngẫu nhiên -> base64 string."""
    return base64.b64encode(os.urandom(n_bytes)).decode("ascii")

def hash_password(password: str, salt: str) -> str:
    """SHA-256(password + salt) -> hex 64 ký tự."""
    return hashlib.sha256(f"{password}{salt}".encode("utf-8")).hexdigest()

def load_avatar_as_base64_bytes(photo_path: Optional[str]) -> Optional[bytes]:
    """Đọc file ảnh và trả bytes đã base64-encode để lưu vào BLOB."""
    if not photo_path:
        return None
    with open(photo_path, "rb") as f:
        return base64.b64encode(f.read())

# Regex tiện dùng cho validate
EMAIL_RE = r"[^@\s]+@[^@\s]+\.[^@\s]+"
USERNAME_RE = r"[a-zA-Z0-9._-]{3,60}"
PHONE_RE = r"\+?\d{8,15}"

def is_email(s: str) -> bool: return re.fullmatch(EMAIL_RE, s or "") is not None
def is_username(s: str) -> bool: return re.fullmatch(USERNAME_RE, s or "") is not None
def is_phone(s: str) -> bool: return re.fullmatch(PHONE_RE, s or "") is not None

