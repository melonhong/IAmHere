import pymysql
import json
import time
from pyfingerprint.pyfingerprint import PyFingerprint

# 지문 센서 초기화
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError("지문 센서 비밀번호 오류")
except Exception as e:
    print(f"지문 센서 초기화 실패: {e}")
    exit()

# 데이터베이스 연결
conn = pymysql.connect(
    host='localhost',
    user='test',
    password='test1234',
    database='fingerprint_db_test'
)
cursor = conn.cursor()
print("출석 시작! 손가락을 대주세요...")

try:
    while True: # 계속해서 지문 인식하는 루프
        if f.readImage():
            f.convertImage(0x01)
            fingerprint_data = f.downloadCharacteristics(0x01)
            # fingerprints 테이블에서의 지문 비교
            cursor.execute("SELECT user_id, fingerprint FROM fingerprints") # fingerprints 테이블이 있다고 가정했음
            fingerprints = cursor.fetchall()

            for user_id, stored_fingerprint in fingerprints:
                stored_fingerprint = json.loads(stored_fingerprint)
                f.uploadCharacteristics(0x02, stored_fingerprint)
                score = f.compareCharacteristics()

                if score >= 60:  # 일치율
                    # 이미 출석한 경우 체크
                    cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND DATE(timestamp) = CURDATE()", (user_id,))
                    if cursor.fetchone() is None:
                        cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user_id,))
                        conn.commit()
                        print(f"출석 완료! : {user_id} (일치율 : {score})")
                    else:
                        print(f"이미 출석 처리됨 : {user_id}")

            time.sleep(2) # 너무 빠르게 반복되지 않도록 속도 조절
except KeyboardInterrupt:
    print("출석 종료")
finally:
    cursor.close()
    conn.close()
