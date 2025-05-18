import pymysql
from db import get_db_connection

# 사용자 추가
def add_user(login_id, password, name, role):
    """
    users 테이블에 사용자 추가
    - login_id: 로그인 ID
    - password: 비밀번호
    - name: 사용자 이름
    - role: 'student' 또는 'professor'
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (login_id, password, name, role)
            VALUES (%s, %s, %s, %s)
        """, (login_id, password, name, role))
        conn.commit()
        print(f"✅ 사용자 {name}이(가) 추가되었습니다.")
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        print(f"❌ 사용자 추가 실패: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# 학생 추가
def add_student(user_id, major, student_number):
    """
    students 테이블에 학생 정보 추가
    - user_id: users 테이블의 PK
    - major: 전공
    - student_number: 학번
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (student_id, major, student_number)
            VALUES (%s, %s, %s)
        """, (user_id, major, student_number))
        conn.commit()
        print("✅ 학생 정보가 추가되었습니다.")
    except Exception as e:
        conn.rollback()
        print(f"❌ 학생 정보 추가 실패: {e}")
    finally:
        cursor.close()
        conn.close()

# 교수 추가
def add_professor(user_id, department):
    """
    professors 테이블에 교수 정보 추가
    - user_id: users 테이블의 PK
    - department: 소속 학과
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO professors (professor_id, department)
            VALUES (%s, %s)
        """, (user_id, department))
        conn.commit()
        print("✅ 교수 정보가 추가되었습니다.")
    except Exception as e:
        conn.rollback()
        print(f"❌ 교수 정보 추가 실패: {e}")
    finally:
        cursor.close()
        conn.close()

# 사용자 조회 (user_id 기준)
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return cursor.fetchone()
    except pymysql.Error as e:
        print(f"❌ 사용자 조회 실패: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# 사용자 조회 (student_id 기준)
def get_user_by_student_id(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        return cursor.fetchone()
    except pymysql.Error as e:
        print(f"❌ 사용자 조회 실패: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

# 전체 사용자 조회
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except pymysql.Error as e:
        print(f"❌ 사용자 전체 조회 실패: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# 사용자 삭제
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount:
            print(f"🗑 사용자 {user_id} 삭제 완료")
            return True
        else:
            print("⚠️ 해당 ID의 사용자가 존재하지 않습니다.")
            return False
    except pymysql.Error as e:
        print(f"❌ 사용자 삭제 실패: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

