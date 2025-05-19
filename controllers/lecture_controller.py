from models import LectureDAO

class LectureController:
    def __init__(self):
        self.lecture_dao = LectureDAO()

    def register_lecture(title, day, professor_id, start_time, end_time, start_date, end_date):
        lecture_id = self.lecture_dao.add_lecture(title, day, professor_id, start_time, end_time, start_date, end_date)
        return bool(lecture_id)