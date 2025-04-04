import pymysql

# MySQl 데이터베이스 연결
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='idontknow...',
    database='fingerprint_db'
)
cursor = conn.cursor()

# 출석 테이블 생성
cursor.execute('''
    CREATE TABLE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
cursor.close()
conn.close()
print("출석 테이블 생성 완료")