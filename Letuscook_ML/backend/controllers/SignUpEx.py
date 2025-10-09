# backend/signup_backend_pymysql.py
import base64, hashlib, os, re
from typing import Optional, Tuple
import pymysql

from backend.controllers.function import (
    MySQLBase,
    SignupValidationError, DuplicateFieldError,  # DuplicateFieldError vẫn import, nhưng bạn không dùng nữa cũng không sao
)
from backend.database.Connectors.User_Connector import UserConnector


class SignUpBackendEx(MySQLBase):
    def __init__(self, **kw):
        super().__init__(**kw)

    @staticmethod
    def _generate_salt(n_bytes: int = 16) -> str:
        return base64.b64encode(os.urandom(n_bytes)).decode("ascii")

    @staticmethod
    def _hash(password: str, salt: str) -> str:
        return hashlib.sha256(f"{password}{salt}".encode("utf-8")).hexdigest()

    @staticmethod
    def _load_avatar_as_base64_bytes(photo_path: Optional[str]) -> Optional[bytes]:
        if not photo_path:
            return None
        try:
            with open(photo_path, "rb") as f:
                return base64.b64encode(f.read())
        except Exception:
            return None  # hoặc raise SignupValidationError("Invalid photo file.")

    @staticmethod
    def _validate(full_name, email, username, password, confirm_password,
                  phone_number: Optional[str], bio: Optional[str]) -> None:
        # NẾU muốn khớp DB (PhoneNumber cho phép NULL) thì KHÔNG bắt buộc phone:
        if not all([full_name, email, username, password, confirm_password]):
            raise SignupValidationError("Please fill in all required fields.")

        if len(full_name.strip()) == 0 or len(full_name) > 100:  # DB VARCHAR(100)
            raise SignupValidationError("Invalid full name.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""):
            raise SignupValidationError("Invalid email address.")
        if not re.fullmatch(r"[a-zA-Z0-9._-]{3,60}", username or ""):
            raise SignupValidationError("Username must be 3–60 chars (letters, digits, . _ -).")
        if len(password) < 8:
            raise SignupValidationError("Password must be at least 8 characters long.")
        if password != confirm_password:
            raise SignupValidationError("Password confirmation does not match.")
        # PhoneNumber: chỉ kiểm tra định dạng khi có nhập
        if phone_number and not re.fullmatch(r"\+?\d{8,15}", phone_number):
            raise SignupValidationError("Invalid phone number.")
        if bio and len(bio) > 65535:  # TEXT
            raise SignupValidationError("Bio is too long.")

    def _check_duplicate(self, email: str, username: str) -> None:
        self.connectMySQL()
        sql = "SELECT Email, Username FROM Users WHERE Email=%s OR Username=%s LIMIT 1"
        self.cursor.execute(sql, (email, username))
        row = self.cursor.fetchone()

        # <-- FIX: nếu không có bản ghi trùng, thoát sớm
        if not row:
            return

        # an toàn hơn: gán ra biến, phòng cột có thể NULL
        db_email, db_username = row[0], row[1]

        if db_email == email and db_username == username:
            raise SignupValidationError("Email and Username already exist.")
        elif db_email == email:
            raise SignupValidationError("Email already exists.")
        elif db_username == username:
            raise SignupValidationError("Username already exists.")

    def register(
            self, *,
            full_name,
            email,
            username,
            password,
            confirm_password,
            phone_number: Optional[str] = None,
            bio: Optional[str] = None,
            photo_path: Optional[str] = None
    ) -> Tuple[bool, int]:
        """
        Trả về (ok, new_user_id). Ném ra:
          - SignupValidationError
          - pymysql.MySQLError
        """
        self.connectMySQL()

        # 1) validate: KHÔNG truyền photo_path vào đây (vì bio/photo không bắt buộc)
        self._validate(full_name, email, username, password, confirm_password, phone_number, bio)

        # 2) trùng email/username
        self._check_duplicate(email, username)

        # 3) hash
        salt = self._generate_salt()
        pwd_hash = self._hash(password, salt)

        # 4) ảnh (optional) -> base64 bytes hoặc None
        #avatar_bytes = self._load_avatar_as_base64_bytes(photo_path)

        # 5) insert
        # sql = """INSERT INTO Users
        #          (full_name, email, username, password_hash, password_salt, phone_number, bio)
        #          VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        # vals = (full_name, email, username, pwd_hash, salt, phone_number, bio)
        # self.cursor.execute(sql, vals)
        # self.conn.commit()
        # new_id = self.cursor.lastrowid

        user_connector = UserConnector()
        resutl = user_connector.saveNewUser(full_name, email, username, pwd_hash, salt, phone_number, bio, photo_path)
        return True, resutl

