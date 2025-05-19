import pymysql
from config import DB_CONFIG

class DBManager:
    def __init__(self):
        self.conn = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"],
            cursorclass=pymysql.cursors.DictCursor
        )

    # 쿼리 실행 후 기본 키를 반환(기본 키는 자동 증가 해야 함)
    def execute(self, sql, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                self.conn.commit()
                return cursor.lastrowid # 자동 증가하는 기본 키를 반환
        except Exception as e:
            print(f"❌ DB 실행 오류: {e}")
            return None

    # 쿼리 실행 후 성공 여부를 반환
    def execute_bool(self, sql, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                self.conn.commit()
                return True
        except Exception as e:
            print(f"❌ DB 실행 오류: {e}")
            return False

    def fetch_one(self, sql, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        except Exception as e:
            print(f"❌ DB 조회 중 오류 발생: {e}")
            return None

    def fetch_all(self, sql, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"❌ DB 조회 중 오류 발생: {e}")
            return []

