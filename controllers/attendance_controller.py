from models import AttendanceDAO, LectureDAO, EnrollmentDAO, UserDAO, FingerprintDAO, BluetoothDeviceDAO
from bluetooth import *
from fingerprint import *
from notifier import *
import time

class AttendanceController:
    def __init__(self):
        self.attendance_dao = AttendanceDAO()
        self.lecture_dao = LectureDAO()
        self.enrollment_dao = EnrollmentDAO()
        self.user_dao = UserDAO()
        self.bluetooth_dao = BluetoothDeviceDAO()
        self.fingerprint_dao = FingerprintDAO()

    # 강의 시작 전 필요한 정보들을 가져옴
    def get_attendance_context(self, lecture_id):
        print(f"[DEBUG] Fetching lecture info for ID: {lecture_id}")
        lecture_data = self.lecture_dao.get_lecture_by_id(lecture_id)
        print(f"[DEBUG] lecture_data: {lecture_data}")
        if not lecture_data:
            raise ValueError("강의 정보를 찾을 수 없습니다.")

        professor_id = lecture_data['professor_id']
        lecture_title = lecture_data['title']
        print(f"[DEBUG] professor_id: {professor_id}, title: {lecture_title}")

        result = self.bluetooth_dao.get_mac_by_user_id(professor_id)
        mac_addr = result['mac_address'] if result else None
        print(f"[DEBUG] MAC address: {mac_addr}")

        enrolled_dict = (self.enrollment_dao.get_enrollments_by_lecture(lecture_id) or [])
        print(f"[DEBUG] enrolled_dict: {enrolled_dict}")
        enrolled_students = [entry['user_id'] for entry in enrolled_dict]
        print(f"[DEBUG] enrolled_students: {enrolled_students}")

        user_mac_map = self.bluetooth_dao.get_mac_addresses_by_user_ids(enrolled_students)
        print(f"[DEBUG] user_mac_map: {user_mac_map}")

        return lecture_id, lecture_title, mac_addr, enrolled_students, user_mac_map


    # 강의 시작
    # 블루투스 연결 확인 후 출석 체크 시작
    def process_attendance(self, lecture_id, mac_addr, enrolled_students, user_mac_map):
        if not is_connected(mac_addr):
            raise ConnectionError(f"{mac_addr} 연결이 끊어졌습니다. 강의를 종료합니다.")

        misbehaving_students = set()
        scanned_devices = scan_bluetooth_devices()

        for user_id in enrolled_students:
            mac = user_mac_map.get(user_id)
            if mac in scanned_devices:
                self.attendance_dao.add_attendance(user_id, lecture_id, method="Bluetooth", status="1차출석완료")
            else:
                self.attendance_dao.add_attendance(user_id, lecture_id, method="Bluetooth", status="1차출석실패")
                misbehaving_students.add(user_id)
        
        return misbehaving_students

    # 강의 종료 후 학생들에 대한 2차 출석 체크
    def finalize_attendance(self, enrolled_students, misbehaving_students, lecture_id, lecture_title, logger=print):
        for user_id in misbehaving_students:
            user_data = self.user_dao.get_user_by_id(user_id)
            if not user_data:
                logger(f"⚠️ 사용자 ID {user_id} 정보를 찾을 수 없습니다.")
                continue

            student_name = user_data['name']
            fingerprint_data = self.fingerprint_dao.get_fingerprint_by_user_id(user_id)
            success = False

            sensor = initialize_sensor()
            if sensor is None:
                logger("⚠️ 지문 센서가 초기화 되지 않았습니다. 10초 후 다시 시도합니다.")
                time.sleep(10)  # 10초 대기

            for attempt in range(3):
                logger(f"{student_name} 학생의 지문 인식을 시작합니다.")
                send_check(student_name, lecture_title)

                if verify_fingerprint(fingerprint_data):
                    self.attendance_dao.add_attendance(user_id, lecture_id, method="Both", status="2차출석완료")
                    logger(f"✅ {student_name} 지문 인식 성공 (시도 {attempt + 1}/3)")
                    success = True
                    send_result(student_name, success)
                    break
                else:
                    logger("❌ 지문이 일치하지 않습니다. 5초 후 다시 시도해주세요.")
                    send_result(student_name, success)
                    time.sleep(5)  # 5초 대기

            if not success:
                self.attendance_dao.add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석실패")
                logger(f"❌ {student_name} 지문 인식 실패")

        # 2차 출석을 하지 않은 학생들을 처리
        not_verified_users = [uid for uid in enrolled_students if uid not in misbehaving_students]
        for user_id in not_verified_users:
            self.attendance_dao.add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석제외")
