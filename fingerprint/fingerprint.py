import json
import time
from pyfingerprint.pyfingerprint import PyFingerprint

# 지문 센서 초기화
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

# 지문 등록
def scan_fingerprint():
    sensor = initialize_sensor()
    if not sensor:
        return False

    print("🖐 손가락을 센서에 올려주세요...")

    while not sensor.readImage():
        pass

    sensor.convertImage(0x01)
    fingerprint_data = sensor.downloadCharacteristics(0x01)
    fingerprint_json = json.dumps(fingerprint_data)

    return fingerprint_json

# 지문 인증
def verify_fingerprint(fingerprint_data):
    sensor = initialize_sensor()
    if not sensor:
        return False

    try:
        stored_fingerprint = json.loads(fingerprint_data['fingerprint_template'])

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

    except Exception as e:
        print(f"❌ 지문 인증 중 오류 발생: {e}")
        return False
