import json
import pymysql
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from db import get_db_connection

# ✅ 지문 센서 초기화
def initialize_sensor():
    start_time = time.time()
    sensor = None
    
    while time.time() - start_time < 5:  # 5초 동안 시도
        try:
            sensor = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
            if sensor.verifyPassword():
                return sensor
        except Exception:
            pass
        time.sleep(0.1)  # CPU 부하 줄이기
    
    print("❌ 지문 센서 응답 시간 초과 (5초)")
    return None

# ✅ 지문 등록
def register_fingerprint(user_id):
    sensor = initialize_sensor()
    if not sensor:
        return False

    print("🖐 손가락을 센서에 올려주세요...")

    while not sensor.readImage():
        pass

    sensor.convertImage(0x01)
    fingerprint_data = sensor.downloadCharacteristics(0x01)
    fingerprint_json = json.dumps(fingerprint_data)

    # 데이터베이스 저장
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO fingerprints (user_id, fingerprint) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE fingerprint = VALUES(fingerprint)
        """, (user_id, fingerprint_json))
        conn.commit()
        print(f"✅ 사용자 {user_id}의 지문이 저장되었습니다.")
        return True
    except pymysql.Error as e:
        print("❌ 데이터베이스 오류:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# ✅ 지문 인증
def verify_fingerprint(user_id):
    """저장된 지문과 사용자의 지문을 비교하여 인증을 수행"""
    sensor = initialize_sensor()
    if not sensor:
        return False

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT fingerprint FROM fingerprints WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        # ✅ 데이터가 없는 경우 예외 처리
        if not result:
            print("❌ 해당 사용자 ID의 지문 데이터가 없습니다.")
            return False

        stored_fingerprint = json.loads(result['fingerprint']) 

        print("지문을 센서에 올려주세요...")
        while not sensor.readImage():
            pass

        sensor.convertImage(0x01)  
        sensor.uploadCharacteristics(0x02, stored_fingerprint)  
        score = sensor.compareCharacteristics()  

        if score >= 60:
            print("✅ 지문 인증 성공!")
            return True
        else:
            print("❌ 지문이 일치하지 않습니다.")
            return False

    except pymysql.Error as e:
        print("데이터베이스 오류:", e)
        return False

    finally:
        cursor.close()
        conn.close()

