from db.db_manager import DBManager

class AttendanceDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_attendance(self, user_id, lecture_id, method, status):
        sql = """
            INSERT INTO attendances (user_id, lecture_id, method, status)
            VALUES (%s, %s, %s, %s)
        """
        params = (user_id, lecture_id, method, status)
        return self.execute(sql, params)

    def get_attendance_by_user_and_lecture(self, user_id, lecture_id):
        sql = """
            SELECT * FROM attendances WHERE user_id = %s AND lecture_id = %s
        """
        params = (user_id, lecture_id)
        return self.fetch_one(sql, params)

    def get_all_attendances(self):
        sql = "SELECT * FROM attendances"
        return self.fetch_all(sql)

    def delete_attendance(self, attendance_id):
        sql = "DELETE FROM attendances WHERE attendance_id = %s"
        params = (attendance_id,)
        return self.execute(sql, params)

