from models import UserDAO, StudentDAO, ProfessorDAO

class UserController:
    def __init__(self):
        self.user_dao = UserDAO()
        self.student_dao = StudentDAO()
        self.professor_dao = ProfessorDAO()

    def register_student(self, login_id, password, name, major, student_number):
        user_id = self.user_dao.add_user(login_id, password, name, "student")
        if not user_id:
            return False
        return self.student_dao.add_student(user_id, major, student_number)

    def register_professor(self, login_id, password, name, department):
        user_id = self.user_dao.add_user(login_id, password, name, "professor")
        if not user_id:
            return False
        return self.professor_dao.add_professor(user_id, department)
