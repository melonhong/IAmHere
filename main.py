from bluetooth import scan_bluetooth_devices, add_device, get_mac_addresses_by_user_ids
from fingerprint import register_fingerprint, verify_fingerprint
from user import add_user
from lecture import add_lecture
from enrollment import add_enrollment, get_enrolled_user_ids
from attendance import add_attendance
from db import initialize_database

def main():
    initialize_database()

    while True:
        print("\n===== 메인 메뉴 =====")
        print("1. 사용자 등록")
        print("2. 강의 등록")
        print("3. 수강 신청")
        print("4. 블루투스 장치 수동 추가")
        print("5. 지문 등록")
        print("6. 1차 출석: 블루투스 자동 출석 처리")
        print("7. 2차 출석: 지문 인증 및 출석 기록")
        print("0. 종료")

        choice = input("선택 (0-7): ").strip()

        if choice == "1":
            student_id = input("학번 입력: ").strip()
            name = input("이름 입력: ").strip()
            major = input("전공 입력: ").strip()
            roles = {
                '1': '강의자',
                '2': '수강생'
            }
            role = None

            while role is None:
                num = input("1번: 강의자, 2번: 수강생\n번호를 입력하세요: ")
                role = roles.get(num)
                if role:
                    print(f"선택한 역할: {role}")
                else:
                    print(f"잘못된 입력입니다. 다시 선택해주세요.\n")
            if add_user(student_id, name, major, role.strip()):
                print("✅ 사용자 등록 완료")
            else:
                print("❌ 사용자 등록 실패")

        elif choice == "2":
            title = input("강의명: ").strip()
            day = input("요일 (월~금): ").strip()
            start_time = input("시작 시간 (HH:MM:SS): ").strip()
            end_time = input("종료 시간 (HH:MM:SS): ").strip()
            start_date = input("시작 날짜 (YYYY-MM-DD): ").strip()
            end_date = input("종료 날짜 (YYYY-MM-DD): ").strip()
            if add_lecture(title, day, start_time, end_time, start_date, end_date):
                print("✅ 강의 등록 완료")
            else:
                print("❌ 강의 등록 실패")

        elif choice == "3":
            user_id = input("사용자 ID: ").strip()
            lecture_id = input("강의 ID: ").strip()
            if add_enrollment(user_id, lecture_id):
                print("✅ 수강 신청 완료")
            else:
                print("❌ 수강 신청 실패")

        elif choice == "4":
            user_id = input("등록할 사용자 ID: ").strip()
            mac_address = input("블루투스 MAC 주소: ").strip()
            name = input("블루투스 장치 이름: ").strip()
            if add_device(user_id, mac_address, name):
                print(f"✅ 블루투스 장치 추가 완료: {name} ({mac_address})")
            else:
                print("❌ 블루투스 장치 추가 실패")

        elif choice == "5":
            user_id = input("지문 등록할 사용자 ID: ").strip()
            if register_fingerprint(user_id):
                print("✅ 지문 등록 완료")
            else:
                print("❌ 지문 등록 실패")

        elif choice == "6":
            lecture_id = input("출석 처리할 강의 ID: ").strip()

            print("=== 블루투스 기기 스캔 시작 ===")
            scanned_devices = scan_bluetooth_devices()
            scanned_macs = [mac for mac, _ in scanned_devices]
            print(scanned_macs)

            enrolled_users = get_enrolled_user_ids(lecture_id)
            user_mac_map = get_mac_addresses_by_user_ids(enrolled_users)

            for user_id in enrolled_users:
                mac = user_mac_map.get(user_id)
                if mac in scanned_macs:
                    result = add_attendance(user_id, lecture_id, method="Bluetooth", status="1차출석완료")
                    print(f"✅ 사용자 {user_id} 출석 처리됨") if result else print(f"❌ 사용자 {user_id} 출석 실패")
                else:
                    result = add_attendance(user_id, lecture_id, method="Bluetooth", status="1차출석실패")
                    print(f"❌ 사용자 {user_id} 결석 처리됨") if result else print(f"⚠️ 사용자 {user_id} 결석 기록 실패")


        elif choice == "7":
            selected_user_ids = input("지문 인증할 사용자 ID들 (띄어쓰기로 구분, 예: 1 2 3): ").strip().split()
            selected_user_ids = [int(uid) for uid in selected_user_ids]
            lecture_id = input("출석할 강의 ID: ").strip()
            enrolled_users = get_enrolled_user_ids(lecture_id)  # ['1', '2', '3', '4', '5']
            print(selected_user_ids)
            print(enrolled_users)

            for user_id in selected_user_ids:
                if user_id not in enrolled_users:
                    print(f"❌ 사용자 {user_id}는 이 강의에 수강 신청되어 있지 않습니다.")
                    return 

                if verify_fingerprint(user_id):
                    if add_attendance(user_id, lecture_id, method="Both", status="2차출석완료"):
                        print(f"✅ 사용자 {user_id}의 출석 처리 완료")
                    else:
                        print(f"❌ 사용자 {user_id}의 출석 기록 실패")
                else:
                    add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석실패")
                    print(f"❌ 사용자 {user_id} 지문 인증 실패 (출석 실패 처리됨)")

            # 인증하지 않은 학생들 처리
            not_verified_users = [user_id for user_id in enrolled_users if user_id not in selected_user_ids]
            for user_id in not_verified_users:
                add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석제외")
                print(f"⚠️ 사용자 {user_id}는 지문 인증 대상이 아니므로 2차출석제외 처리됨")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()

