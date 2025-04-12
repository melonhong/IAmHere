import pymysql
from db import get_db_connection

def add_enrollment(user_id, lecture_id):
    """
    사용자를 강의에 수강 등록합니다.
    - user_id: 사용자 ID (int)
    - lecture_id: 강의 ID (int)
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 중복 등록 방지
        cursor.execute("""
            INSERT INTO enrollments (user_id, lecture_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE user_id = user_id
        """, (user_id, lecture_id))

        conn.commit()
        print(f"✅ 사용자 {user_id}가 강의 {lecture_id}에 수강 등록되었습니다.")
        return True
    except pymysql.Error as e:
        print(f"❌ 수강 등록 오류: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_enrolled_user_ids(lecture_id):
    """특정 강의에 수강 등록된 모든 사용자 ID 조회"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id FROM enrollments
        WHERE lecture_id = %s
    """, (lecture_id,))
    result = cursor.fetchall()
    conn.close()
    return [row["user_id"] for row in result]
