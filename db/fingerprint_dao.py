import json
from pyfingerprint.pyfingerprint import PyFingerprint
from db.db_manager import DBManager

class FingerprintDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_fingerprint(self, user_id, fingerprint_template):
        sql = """
            INSERT INTO fingerprints (user_id, fingerprint_template)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE fingerprint_template = VALUES(fingerprint_template)
        """
        params = (user_id, fingerprint_template)
        return self.execute_bool(sql, params)

    def get_fingerprint_by_user_id(self, user_id):
        sql = "SELECT fingerprint_template FROM fingerprints WHERE user_id = %s"
        params = (user_id,)
        return self.fetch_one(sql, params)

    def delete_fingerprint(self, user_id):
        sql = "DELETE FROM fingerprints WHERE user_id = %s"
        params = (user_id,)
        return self.execute(sql, params)

