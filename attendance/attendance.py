import pymysql
from db import get_db_connection
import datetime

# 출석 추가
def add_attendance(user_id, lecture_id, method, mac_address=None, status='1차출석실패'):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO attendances (user_id, lecture_id, method, mac_address, check_in, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id, lecture_id, method, mac_address,
            datetime.datetime.now(), status
        ))
        conn.commit()
        print(f"✅ 사용자 {user_id} 출석이 기록되었습니다.")
        return True
    except pymysql.Error as e:
        print(f"❌ 출석 기록 실패: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
