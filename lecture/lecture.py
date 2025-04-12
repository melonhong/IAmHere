import pymysql
from db import get_db_connection

def add_lecture(title, day, start_time, end_time, start_date, end_date):
    """
    새로운 강의를 추가합니다.
    - title: 강의 제목 (문자열)
    - day: 요일 ('월', '화', '수', '목', '금')
    - start_time, end_time: 시간 문자열 (예: '09:00:00')
    - start_date, end_date: 날짜 문자열 (예: '2025-03-01')
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO lectures (title, day, start_time, end_time, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, day, start_time, end_time, start_date, end_date))

        conn.commit()
        print(f"✅ 강의가 추가되었습니다: {title}")
        return True
    except pymysql.Error as e:
        print(f"❌ 강의 추가 중 오류 발생: {e}")
        return False
    finally:
        if conn:
            conn.close()

