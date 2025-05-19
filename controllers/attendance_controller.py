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
        lecture_data = self.lecture_dao.get_lecture_by_id(lecture_id)
        if not lecture_data:
            raise ValueError("강의 정보를 찾을 수 없습니다.")
        
        print(lecture_data)

        professor_id = lecture_data['professor_id']
        lecture_title = lecture_data['title']
        mac_addr = (self.bluetooth_dao.get_mac_by_user_id(professor_id) or (None,))[0]

        enrolled_dict = (self.enrollment_dao.get_enrollments_by_lecture(lecture_id) or {})
        enrolled_students = [entry['user_id'] for entry in enrolled_dict]
        user_mac_map = self.bluetooth_dao.get_mac_addresses_by_user_ids(enrolled_students)

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
    def finalize_attendance(self, enrolled_students, misbehaving_students, lecture_id, lecture_title):
        # 블루투스 출석이 실패한 학생들에 대해 지문 인식으로 2차 출석 체크
        for user_id in misbehaving_students:
            user_data = self.user_dao.get_user_by_id(user_id)
            if not user_data:
                continue

            student_name = user_data['name']
            send_check(student_name, lecture_title)
            fingerprint_data = self.fingerprint_dao.get_fingerprint_by_user_id(user_id)
            success = False

            # 3회 지문 인식 후 결과를 학생에게 전송
            for attempt in range(3):
                if verify_fingerprint(fingerprint_data):
                    self.attendance_dao.add_attendance(user_id, lecture_id, method="Both", status="2차출석완료")
                    success = True
                    break
                time.sleep(1)
            if not success:
                self.attendance_dao.add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석실패")
            send_result(student_name, success)

        # 블루투스 출석이 성공한 학생들에 대해 2차 출석 제외 처리
        not_verified_users = [uid for uid in enrolled_students if uid not in misbehaving_students]
        for user_id in not_verified_users:
            self.attendance_dao.add_attendance(user_id, lecture_id, method="Fingerprint", status="2차출석제외")