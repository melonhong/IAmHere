from model.db_manager import DBManager

class LectureDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_lecture(self, title, day, professor_id, start_time, end_time, start_date, end_date):
        sql = """
            INSERT INTO lectures (title, day, professor_id, start_time, end_time, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (title, day, professor_id, start_time, end_time, start_date, end_date)
        return self.execute(sql, params)

    def get_lecture_by_id(self, lecture_id):
        sql = "SELECT * FROM lectures WHERE lecture_id = %s"
        params = (lecture_id,)
        return self.fetch_one(sql, params)

    def get_professor_by_id(self, lecture_id):
        sql = "SELECT professor_id FROM lectures WHERE lecture_id = %s"
        params = (lecture_id,)
        return self.fetch_one(sql, params)

    def get_all_lectures(self):
        sql = "SELECT * FROM lectures"
        return self.fetch_all(sql)

    def delete_lecture(self, lecture_id):
        sql = "DELETE FROM lectures WHERE lecture_id = %s"
        params = (lecture_id,)
        return self.execute(sql, params)

