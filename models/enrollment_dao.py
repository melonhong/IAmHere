from .db_manager import DBManager

class EnrollmentDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_enrollment(self, user_id, lecture_id):
        sql = """
            INSERT INTO enrollments (user_id, lecture_id)
            VALUES (%s, %s)
        """
        params = (user_id, lecture_id)
        return self.execute(sql, params)

    def get_enrollments_by_user(self, user_id):
        sql = """
            SELECT lecture_id FROM enrollments WHERE user_id = %s
        """
        return self.fetch_all(sql, (user_id,))

    def get_enrollments_by_lecture(self, lecture_id):
        sql = """
            SELECT user_id FROM enrollments WHERE lecture_id = %s
        """
        return self.fetch_all(sql, (lecture_id,))

    def is_enrolled(self, user_id, lecture_id):
        sql = """
            SELECT * FROM enrollments WHERE user_id = %s AND lecture_id = %s
        """
        return self.fetch_one(sql, (user_id, lecture_id)) is not None

