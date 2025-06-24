import json
from pyfingerprint.pyfingerprint import PyFingerprint
from models.db_manager import DBManager
from AES256 import *
from config.config import AES_KEY

class FingerprintDAO(DBManager):
    def __init__(self):
        super().__init__()
        self.aes_cipher = AES256(AES_KEY) # AES 객체 생성

    def add_fingerprint(self, user_id, fingerprint_template):
        encrypted_fingerprint_data = self.aes_cipher.encrypt(fingerprint_template) # 지문 데이터 암호화
        sql = """
            INSERT INTO fingerprints (user_id, fingerprint_template)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE fingerprint_template = VALUES(fingerprint_template)
        """
        params = (user_id, encrypted_fingerprint_data)
        return self.execute_bool(sql, params)

    def get_fingerprint_by_user_id(self, user_id):
        sql = "SELECT fingerprint_template FROM fingerprints WHERE user_id = %s"
        params = (user_id,)
        sql_result = self.fetch_one(sql, params)

        if sql_result is None:
            return None

        else:
            encrypted_fingerprint_data = sql_result['fingerprint_template']
            decrypted_fingerprint_data = self.aes_cipher.decrypt(encrypted_fingerprint_data)
            sql_result['fingerprint_template'] = decrypted_fingerprint_data
            return sql_result

    def delete_fingerprint(self, user_id):
        sql = "DELETE FROM fingerprints WHERE user_id = %s"
        params = (user_id,)
        return self.execute(sql, params)

