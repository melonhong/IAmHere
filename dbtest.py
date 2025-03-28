# 이 코드는 mariadb에 지문 데이터를 저장하고 불러오는 코드입니다
# 리포지토리 변경
import pymysql
import json
import time
from pyfingerprint.pyfingerprint import PyFingerprint

# ✅ 지문 인식 센서 초기화
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError("지문 센서의 비밀번호가 잘못되었습니다.")
except Exception as e:
    print("지문 센서를 초기화하는 동안 오류 발생:", str(e))
    exit(1)

# ✅ 데이터베이스 연결
try:
    conn = pymysql.connect(host='localhost', user='test', password='test1234', database='fingerprint_db_test')
    cursor = conn.cursor()

    # ✅ fingerprints 테이블 생성 (없으면 생성)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fingerprints (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            fingerprint TEXT NOT NULL
        )
    ''')
    conn.commit()

    # ✅ 지문을 읽어 저장
    print('지문을 저장합니다... 손가락을 대주세요...')
    while not f.readImage():
        pass

    f.convertImage(0x01)  # 지문을 버퍼에 저장
    fingerprint_data = f.downloadCharacteristics(0x01)  # 지문 특징점 가져오기
    fingerprint_json = json.dumps(fingerprint_data)  # JSON 문자열로 변환

    # ✅ 데이터베이스에 저장
    cursor.execute("INSERT INTO fingerprints (user_id, fingerprint) VALUES (%s, %s)", (1, fingerprint_json))
    conn.commit()
    print("지문이 데이터베이스에 저장되었습니다.")

    time.sleep(1)  # 잠시 대기

    # ✅ 저장된 지문 불러오기
    cursor.execute("SELECT fingerprint FROM fingerprints WHERE user_id=%s", (1,))
    result = cursor.fetchone()

    if result:
        stored_fingerprint = json.loads(result[0])  # JSON 문자열을 리스트로 변환

        print('저장된 지문과 대조해봅니다... 손가락을 대주세요...')
        while not f.readImage():
            pass

        f.convertImage(0x01)  # 새로운 지문을 버퍼에 저장
        f.uploadCharacteristics(0x02, stored_fingerprint)  # 저장된 지문을 0x02에 업로드
        score = f.compareCharacteristics()  # 비교 수행

        if score >= 60:
            print("✅ 지문이 일치합니다!")
        else:
            print("❌ 지문이 일치하지 않습니다!")
        print("📝 일치율:", score)
    else:
        print("❌ 저장된 지문이 없습니다.")

except Exception as e:
    print("오류 발생:", str(e))

finally:
    # ✅ 연결 종료
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()

