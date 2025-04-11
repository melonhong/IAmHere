import pymysql
from db import get_db_connection

# 사용자 추가
def add_user(student_id, name, major):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (student_id, name, major)
            VALUES (%s, %s, %s)
        """, (student_id, name, major))
        conn.commit()
        print(f"✅ 사용자 {name}이(가) 추가되었습니다.")
        return cursor.lastrowid  # 생성된 user_id 반환
    except pymysql.Error as e:
        print(f"❌ 사용자 추가 실패: {e}")
        return None
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
        cursor.execute("SELECT * FROM users WHERE student_id = %s", (student_id,))
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

