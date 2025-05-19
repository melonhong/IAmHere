from models import FingerprintDAO

class FingerprintController:
    def __init__(self):
        self.fingerprint_dao = FingerprintDAO()

    def register_enrollment(self, user_id, fingerprint_template):
        return bool(self.fingerprint_dao.add_fingerprint(user_id, fingerprint_template))
