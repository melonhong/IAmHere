import time
from bluetooth import scan_bluetooth_devices
import pymysql

# DB 연결
conn = pymysql.connect(
    host='localhost',
    user='test',
    password='test1234',
    database='fingerprint_db_test'
)
cursor = conn.cursor()

print("블루투스 출석 시작...")

try:
    while True:
        devices = scan_bluetooth_devices()

        for mac_address, name in devices:
            # 등록된 기기인지 확인하고, 사용자 ID 가져오기
            cursor.execute("SELECT user_id FROM devices WHERE mac_address = %s", (mac_address,))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                # 오늘 출석했는지 확인
                cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND DATE(timestamp) = CURDATE()", (user_id,))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user_id,))
                    conn.commit()
                    print(f"출석 완료 (Bluetooth): {user_id} - {name}")
                else:
                    print(f"이미 출석 처리됨: {user_id} - {name}")
            else:
                print(f"❌ 등록되지 않은 기기: {name} ({mac_address})")

        time.sleep(5)  # 5초 간격으로 반복 스캔
except KeyboardInterrupt:
    print("블루투스 출석 종료")
finally:
    cursor.close()
    conn.close()