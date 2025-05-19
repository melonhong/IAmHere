from models import EnrollmentDAO

class EnrollmentController:
    def __init__(self):
        self.enrollment_dao = EnrollmentDAO()

    def register_enrollment(self, user_id, lecture_id):
        return bool(self.enrollment_dao.add_enrollment(user_id, lecture_id))
