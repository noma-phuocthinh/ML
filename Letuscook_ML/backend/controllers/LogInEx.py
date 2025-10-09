import hashlib
from backend.controllers.function import MySQLBase, LoginValidationError, UnregisteredAccountError, WrongPasswordError

class LogInEx(MySQLBase):
    def __init__(self, **kw):
        super().__init__(**kw)

    @staticmethod
    def _hash(password: str, salt: str) -> str:
        return hashlib.sha256(f"{password}{salt}".encode("utf-8")).hexdigest()

    def _fetch_user_for_login(self, identifier: str):
        self.connectMySQL()
        sql = """
            SELECT user_id, username, email, password_hash, password_salt, full_name
            FROM Users
            WHERE username=%s OR email=%s
            LIMIT 1
        """
        self.cursor.execute(sql, (identifier, identifier))
        return self.cursor.fetchone()

    def login(self, identifier: str, password: str) -> dict:
        identifier = (identifier or "").strip()
        password   = (password or "")

        if not identifier or not password:
            raise LoginValidationError("Please enter both username and password.")

        row = self._fetch_user_for_login(identifier)
        if not row:
            raise UnregisteredAccountError("This account is not registered.")

        user_id, username, email, pwd_hash, salt, full_name = row
        if self._hash(password, salt) != pwd_hash:
            raise WrongPasswordError("Incorrect password.")

        return {"userId": user_id, "username": username, "email": email, "fullName": full_name}
