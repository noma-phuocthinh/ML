from backend.database.Connectors.S3Connector import S3Connector
from backend.database.Connectors.SQLConnector import SQLConnector
from backend.models.User import User


class UserConnector(SQLConnector):
    def fetch_user_for_login(self, identifier: str):
        sql = """
            SELECT user_id, username, email, password_hash, passwordsalt, full_name
            FROM Users
            WHERE username=%s OR email=%s
            LIMIT 1
        """
        result = self.fetchOne(sql, identifier)
        if result:
            user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9])
            return user
        return None

    def saveImageUrl(self, avatar_url, user_id):
        sql = "UPDATE Users SET photo_url = %s WHERE user_id = %s"
        var = (avatar_url, user_id)
        affected_row = self.deleteOrUpdateRow(sql, var)
        return affected_row

    def saveNewUser(self, full_name, email, username, password_hash, password_salt, phone_number, bio, photo_url):
        sql = """INSERT INTO Users
                 (full_name, email, username, password_hash, password_salt, phone_number, bio, is_admin)
                 VALUES (%s,%s,%s,%s,%s,%s,%s, %s)"""
        var = (full_name, email, username, password_hash, password_salt, phone_number, bio, 0)
        user_id = self.insertRow(sql, var)
        if photo_url:
            s3 = S3Connector()
            photo_url_s3 = s3.upload_avatar(photo_url, user_id)

            affected_row = self.saveImageUrl(photo_url_s3, user_id)
            return user_id, affected_row
        return user_id, 0


