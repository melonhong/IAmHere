from bluetooth import *
from fingerprint import register_fingerprint, verify_fingerprint
from db import initialize_database
from notifier import *
from db_manager import DBManager
import time

def main():
    initialize_database()
    db = DBManager()

    while True:
        print("\n===== 메인 메뉴 =====")
        print("6. 블루투스 페어링")
        print("7. 강의를 시작합니까?")
        print("0. 종료")

        choice = input("선택 (0-7): ").strip()

        if choice == "6":
            mac_addr = input("페어링 할 맥 주소: ")
            pair_device(mac_addr)

        elif choice == "7":
            mac_addr = input("맥 주소: ")
            lecture_id = input("출석 처리할 강의 ID: ").strip()
            print("블루투스가 연결되면 강의를 시작합니다...\n")

            start_time = time.time()
            connected = False

            while time.time() - start_time < 10:
                if is_connected(mac_addr):
                    connected = True
                    break
                time.sleep(1)

            if not connected:
                print("⏰ 10초 내에 연결되지 않았습니다. 강의를 시작할 수 없습니다.\n")
                continue

            print("✍️ 강의를 시작합니다. 모두 자리에 착석해주세요!")
            misbehaving_students = set()
            enrolled_users = db.get_enrolled_user_ids(lecture_id)
            user_mac_map = db.get_mac_addresses_by_user_ids(enrolled_users)

            try:
                while connected:
                    if not is_connected(mac_addr):
                        print(f"🔨 {mac_addr} 연결이 끊어졌습니다. 강의를 종료합니다.")
                        break
                    else:
                        print("========= 블루투스 기기 스캔 시작 =========")
                        scanned_devices = scan_bluetooth_devices()
                        print(scanned_devices)

                        for user_id in enrolled_users:
                            mac = user_mac_map.get(user_id)
                            if mac in scanned_devices:
                                result = db.add_attendance(user_id, lecture_id, method="Bluetooth", status="1차출석완료")
                                print(f"✅ 사용자 {user_id} 출석 처리됨") if result else print(f"❌ 사용자 {user_id} 출석 실패")
                            else:
                                result = db.add_attendance(user_id, lecture_id, method="Bluetooth", status="1차출석실패")
                                print(f"❌ 사용자 {user_id} 결석 처리됨") if result else print(f"⚠️ 사용자 {user_id} 결석 기록 실패")
                                misbehaving_students.add(user_id)
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n모니터링을 수동으로 종료했습니다.")

            print(f"블루투스 출석을 실패한 학생들! 😡 지문 출석을 하세요!")
            misbehaving_students_list = list(misbehaving_students)
            print(f"블루투스 출석에 실패한 학생들: {misbehaving_students_list}\n")

            for user_id in misbehaving_students_list:
                if user_id not in enrolled_users:
                    print(f"❌ 사용자 {user_id}는 이 강의에 수강 신청되어 있지 않습니다.")
                    return
                print(f"{user_id}번 학생의 지문 인식을 시작합니다...")
                send_notification("테스트", "테스트 강의")
                if verify_fingerprint(user_id):
                    if db.add_attendance(user_id, lecture_id, method="Both", status="2차출석완료"):
                        print(f"✅ 사용자 {user_id}의 출석 처리 완료")
                    else:
                        print(f"❌ 사용자 {user_id}의 출석 기록 실패")
                else:
                    db.add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석실패")
                    print(f"❌ 사용자 {user_id} 지문 인증 실패 (출석 실패 처리됨)")

            not_verified_users = [user_id for user_id in enrolled_users if user_id not in misbehaving_students]
            for user_id in not_verified_users:
                db.add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석제외")
                print(f"⚠️ 사용자 {user_id}는 지문 인증 대상이 아니므로 2차출석제외 처리됨")

        elif choice == "9":
            send_notification("테스트", "테스트 강의")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()

