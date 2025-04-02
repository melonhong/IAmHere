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

# 데이터베이스에서 해당 MAC 주소의 last_detected 필드 업데이트
def update_detected_time(mac_address):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            UPDATE devices 
            SET last_detected = %s 
            WHERE mac_address = %s
        """, (current_time, mac_address))
        
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ DB 업데이트 실패: {e}")
        return False
    finally:
        if conn:
            conn.close()

# 새로운 기기를 데이터베이스에 추가
def add_device(mac_address, name, device_type="bluetooth"):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO devices (mac_address, name, added_at, last_detected)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
        """, (mac_address, name, datetime.datetime.now(), datetime.datetime.now())) 
        
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ 기기 추가 실패: {e}")
        return False
    finally:
        if conn:
            conn.close()
