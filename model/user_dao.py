from model.db_manager import DBManager

class UserDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_user(self, login_id, password, name, role):
        query = """
            INSERT INTO users (login_id, password, name, role)
            VALUES (%s, %s, %s, %s)
        """
        user_id = self.execute(query, (login_id, password, name, role))
        if user_id:
            print(f"✅ 사용자 {name}이(가) 추가되었습니다.")
            return user_id
        return None

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        return self.fetch_one(query, (user_id,))

    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.fetch_all(query)

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        _, rowcount = self.execute(query, (user_id,))
        return rowcount > 0


class StudentDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_student(self, user_id, major, student_number):
        query = """
            INSERT INTO students (student_id, major, student_number)
            VALUES (%s, %s, %s)
        """
        lastrowid = self.execute(query, (user_id, major, student_number))
        return lastrowid is not None

    def get_student_by_id(self, student_id):
        query = "SELECT * FROM students WHERE student_id = %s"
        return self.fetch_one(query, (student_id,))


class ProfessorDAO(DBManager):
    def __init__(self):
        super().__init__()

    def add_professor(self, user_id, department):
        query = """
            INSERT INTO professors (professor_id, department)
            VALUES (%s, %s)
        """
        lastrowid = self.execute(query, (user_id, department))
        return lastrowid is not None

    def get_professor_by_id(self, professor_id):
        query = "SELECT * FROM professors WHERE professor_id = %s"
        return self.fetch_one(query, (professor_id,))

