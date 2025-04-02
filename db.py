import pymysql
from config import DB_CONFIG  # config.py에서 DB 설정 불러오기

# ✅ 데이터베이스 연결 함수
def get_db_connection():
    """ MySQL 데이터베이스 연결을 반환하는 함수 """
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        charset=DB_CONFIG["charset"],
        cursorclass=pymysql.cursors.DictCursor
    )

# ✅ 테이블 생성 함수
def initialize_database():
    """ 블루투스 및 지문 테이블을 생성하는 함수 (최초 1회 실행) """
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ 블루투스 기기 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mac_address VARCHAR(17) UNIQUE NOT NULL,
            name VARCHAR(255),
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_detected DATETIME
        )
    """)

    # ✅ 지문 데이터 테이블 생성
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fingerprints (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE NOT NULL,
            fingerprint TEXT NOT NULL,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("🔧 데이터베이스를 초기화합니다...")
    initialize_database()
    print("✅ 데이터베이스가 준비되었습니다.")

