from bluetooth import scan_bluetooth_devices, update_detected_time, add_device
from fingerprint import register_fingerprint, verify_fingerprint
from db import get_db_connection, initialize_database
from datetime import datetime
import pytz

# 오늘 요일에 해당하는 강의 정보를 DB에서 불러오기
def get_current_lectures():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 오늘 요일 추출 (ex 월,화 ...)
    today = datetime.now(pytz.timezone("Asia/Seoul")).strftime('%a')
    kor_day_map = {
        'Mon': '월', 'Tue': '화', 'Wed': '수',
        'Thu': '목', 'Fri': '금'
    }
    kor_day = kor_day_map.get(today)

    cursor.execute("""
        SELECT lecture_id, start_time, end_time 
        FROM lecture 
        WHERE day = %s
    """, (kor_day,))

    current_time = datetime.now(pytz.timezone("Asia/Seoul")).time()
    valid_lectures = []

    for lecture_id, start_time, end_time in cursor.fetchall():
        if start_time <= current_time <= end_time:
            valid_lectures.append(lecture_id)

    cursor.close()
    conn.close()
    return valid_lectures

# 출석 정보 저장
def check_attendance(user_id, lecture_id, method, mac_address=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if method == "fingerprint":
            cursor.execute("""
                INSERT INTO attendance (user_id, lecture_id) 
            """, (user_id, lecture_id))
        elif method == "bluetooth":
            cursor.execute("""
                INSERT INTO bt_attendance (user_id, mac_address, lecture_id) 
            """, (user_id, mac_address, lecture_id))

        conn.commit()
        print(f"✅ 출석 처리 완료 ({method}) - 사용자 ID: {user_id}, 강의 ID: {lecture_id}")
    except Exception as e:
        print(f"❌ 출석 처리 실패: {e}")
    finally:
        if conn:
            conn.close()

# 현재 수업 출석 가능한지 확인 (블루투스용)
def check_possible(lecture_id):
    now = datetime.now().time()
    start, end = lecture_id.get(lecture_id, (None, None))
    return start is not None and start <= now <= end

# 블루투스 출석 처리
def bluetooth_attendance(lecture_id):
    print("블루투스 출석 스캔 중...")
    if not check_possible(lecture_id):
        print("현재는 출석 가능한 시간이 아닙니다.")
        return

    devices = scan_bluetooth_devices()
    conn = get_db_connection()
    cursor = conn.cursor()

    for mac, name in devices:
        cursor.execute("SELECT user_id FROM devices WHERE mac_address = %s", (mac,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            update_detected_time(mac)
            check_attendance(user_id, lecture_id, method="bluetooth", mac_address=mac)
        else:
            print(f"❌ 등록되지 않은 기기: {name} ({mac})")

    cursor.close()
    conn.close()

# 지문 출석 처리
def fingerprint_attendance():
    user_id = input("사용자 ID를 입력하세요: ").strip()
    if verify_fingerprint(user_id):
        check_attendance(user_id, method="fingerprint")
    else:
        print("❌ 지문 인증 실패")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 현재 요일 및 시간
        now = datetime.now()
        weekday_kor = ['월', '화', '수', '목', '금'][now.weekday()]
        now_time = now.time()

        # 가장 최근 블루투스 출석 기록
        cursor.execute("""
                SELECT mac_address, timestamp FROM bt_attendance 
                WHERE user_id = %s AND DATE(timestamp) = CURDATE()
                ORDER BY timestamp DESC LIMIT 1
            """, (user_id,))
        recent_bt = cursor.fetchone()

        if not recent_bt:
            print("오늘 블루투스 출석 기록이 없습니다.")
            return

        bt_time = recent_bt[1]

        # 해당 시간에 진행 중인 강의 찾기
        cursor.execute("""
                SELECT lecture_id FROM lecture 
                WHERE day = %s AND start_time <= %s AND end_time >= %s
                  AND start_date <= CURDATE() AND end_date >= CURDATE()
            """, (weekday_kor, bt_time, bt_time))
        lecture = cursor.fetchone()

        if not lecture:
            print("블루투스 출석 시간에 해당하는 강의를 찾을 수 없습니다.")
            return

        lecture_id = lecture[0]

        # 지문 출석 등록
        cursor.execute("""
                INSERT INTO attendance (user_id, lecture_id, timestamp)
                VALUES (%s, %s, NOW())
            """, (user_id, lecture_id))
        conn.commit()
        print(f"✅ 지문 출석 완료! (사용자: {user_id}, 강의 ID: {lecture_id})")

    except Exception as e:
        print(f"❌ 지문 출석 처리 실패: {e}")
    finally:
        if conn:
            conn.close()

# 메인 메뉴
def main():
    initialize_database()

    while True:
        print("\n===== 메인 메뉴 =====")
        print("1. 블루투스 장치 탐색 및 업데이트")
        print("2. 블루투스 장치 추가")
        print("3. 지문 인식")
        print("4. 지문 등록")
        print("5. 블루투스 출석")
        print("0. 종료")

        choice = input("선택 (0-5): ").strip()

        if choice == "1":
            print("=== 블루투스 기기 스캔 시작 ===")
            devices = scan_bluetooth_devices()

            for mac, name in devices:
                if add_device(mac, name):
                    print(f"✅ 추가됨: {name} ({mac})")
                update_detected_time(mac)

        elif choice == "2":
            mac_address = input("추가할 블루투스 장치의 MAC 주소: ").strip()
            name = input("블루투스 장치 이름: ").strip()
            if add_device(mac_address, name):
                print(f"✅ 블루투스 장치 추가 완료: {name} ({mac_address})")

        elif choice == "3":
            user_id = input("인증할 사용자 ID: ").strip()
            fingerprint_attendance() # 지문 출석 연결
            if verify_fingerprint(user_id):
                print("✅ 지문 인증 성공!!! 시스템 접근 허용")
            else:
                print("❌ 지문 인증 실패! 접근 거부")

        elif choice == "4":
            user_id = input("등록할 사용자 ID: ").strip()
            if register_fingerprint(user_id):
                print("✅ 지문 등록 성공!")

        elif choice == "5":
            # 현재 수업 불러와서 하나라도 있으면 출석 시도
            current_lectures = get_current_lectures()
            if current_lectures:
                for lecture_id in current_lectures:
                    bluetooth_attendance(lecture_id)  #출석 함수 호출
            else:
                print("현재 출석 가능한 강의가 없습니다.")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()