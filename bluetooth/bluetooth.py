import subprocess
import re
import datetime
from db import get_db_connection

# 블루투스 기기 스캔 후 MAC 주소와 이름 리스트 반환
def scan_bluetooth_devices():
    try:
        subprocess.run(["bluetoothctl", "--timeout", "5", "scan", "on"], check=True)
        result = subprocess.run(["bluetoothctl", "devices"], capture_output=True, text=True)
        devices = result.stdout.strip().split('\n')

        device_list = []
        for device in devices:
            match = re.match(r"Device ([0-9A-Fa-f:]+) (.+)", device)
            if match:
                mac_address, name = match.groups()
                device_list.append((mac_address, name))
        return device_list
    except subprocess.CalledProcessError as e:
        print(f"❌ 블루투스 스캔 실패: {e}")
        return []

# 새로운 기기를 bluetooth_device 테이블에 추가
def add_device(user_id, mac_address, device_name):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bluetooth_devices (user_id, mac_address, device_name, registered_at)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE device_name = VALUES(device_name)
        """, (user_id, mac_address, device_name, datetime.datetime.now()))

        conn.commit()
        return True
    except Exception as e:
        print(f"❌ 기기 추가 실패: {e}")
        return False
    finally:
        if conn:
            conn.close()

# 유저의 아이디들을 토대로 맥 주소들을 반환 
def get_mac_addresses_by_user_ids(user_ids):
    """여러 사용자 ID에 대한 블루투스 MAC 주소 맵 조회 (user_id -> mac_address)"""
    if not user_ids:
        return {}

    placeholders = ','.join(['%s'] * len(user_ids))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT user_id, mac_address FROM bluetooth_devices
        WHERE user_id IN ({placeholders})
    """, tuple(user_ids))
    rows = cursor.fetchall()
    conn.close()
    
    return {row['user_id']: row['mac_address'] for row in rows}
