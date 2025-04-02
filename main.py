from bluetooth import scan_bluetooth_devices, update_detected_time, add_device
from fingerprint import register_fingerprint, verify_fingerprint
from db import get_db_connection, initialize_database

def main():
    initialize_database()

    while True:
        print("\n===== 메인 메뉴 =====")
        print("1. 블루투스 장치 탐색 및 업데이트")
        print("2. 블루투스 장치 추가")
        print("3. 지문 인식")
        print("4. 지문 등록")
        print("0. 종료")

        choice = input("선택 (0-4): ").strip()

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
            if verify_fingerprint(user_id):
                print("✅ 지문 인증 성공! 시스템 접근 허용")
            else:
                print("❌ 지문 인증 실패! 접근 거부")

        elif choice == "4":
            user_id = input("등록할 사용자 ID: ").strip()
            if register_fingerprint(user_id):
                print("✅ 지문 등록 성공!")

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다. 다시 선택해주세요.")

if __name__ == "__main__":
    main()

