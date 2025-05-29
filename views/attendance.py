import tkinter as tk
from tkinter import messagebox
from controllers.attendance_controller import AttendanceController
from bluetooth import is_connected
import threading
import time

def open_attendance_window(root):
    # 출석 창 생성
    window = tk.Toplevel(root)
    window.title("출석 시작")
    window.geometry("500x400")

    # 강의 ID 입력 UI
    tk.Label(window, text="강의 ID를 입력하세요:").pack(pady=10)
    lecture_entry = tk.Entry(window)
    lecture_entry.pack()

    # 출력 로그 박스
    output = tk.Text(window, height=12)
    output.pack(pady=10)

    # 로그 출력 함수
    def log(message):
        output.insert(tk.END, message + "\n")
        output.see(tk.END)

    # 출석 전체 프로세스 실행 함수 (스레드에서 호출됨)
    def run_attendance_process(lecture_id):
        controller = AttendanceController()
        try:
            # 출석 준비 단계: 강의 정보 조회
            log("⏳ 강의 정보 불러오는 중...")
            lecture_id, lecture_title, mac_addr, enrolled_students, user_mac_map = controller.get_attendance_context(lecture_id)

            # 블루투스 주소가 없을 경우
            if not mac_addr:
                log("❌ 교수님의 블루투스 주소를 찾을 수 없습니다.")
                messagebox.showerror("주소 오류", "교수님의 블루투스 주소를 찾을 수 없습니다.")
                return

            # 강의 정보 출력
            log(f"📡 교수 블루투스 주소: {mac_addr}")
            log(f"📚 강의 제목: {lecture_title}")
            log(f"👨‍🎓 출석 대상 학생 수: {len(enrolled_students)}")
            log(f"👨‍🎓 출석 대상 학생 목록: {enrolled_students}")
            log("⏳ 블루투스 연결 시도 중...")

            # 블루투스 연결 시도 (최대 10초)
            start_time = time.time()
            connected = False
            while time.time() - start_time < 10:
                if is_connected(mac_addr):
                    connected = True
                    break
                time.sleep(1)

            # 연결 실패 시 종료
            if not connected:
                log("❌ 블루투스 연결 실패")
                messagebox.showerror("연결 실패", "교수님의 블루투스 장치 연결에 실패했습니다.")
                return

            log("✅ 연결 성공! 블루투스 출석을 시작합니다.")
        except Exception as e:
            log(f"[출석 준비 중 오류] {str(e)}")
            return

        try:
            misbehaving_students = []  # 블루투스 출석 실패자 목록

            # 출석 루프 시작
            while True:
                if is_connected(mac_addr):
                    # 블루투스 연결된 경우: 1차 출석 처리
                    log("📡 블루투스 연결 상태 확인됨. 1차 블루투스 출석 시작...")
                    misbehaving_students = controller.process_attendance(
                        lecture_id, mac_addr, enrolled_students, user_mac_map
                    )
                    log(f"⚠️ 출석 실패자: {list(misbehaving_students)}")

                    if not misbehaving_students:
                        # 모든 학생 출석 완료 시 루프 종료
                        log("🎉 모든 학생이 출석을 완료했습니다!")
                        break
                else:
                    # 연결이 끊긴 경우: 강의 종료 여부 확인
                    log("🔌 강의자의 블루투스 연결이 끊어졌습니다.")
                    result = messagebox.askyesno("강의 종료 확인", "블루투스 연결이 끊어졌습니다. 강의를 종료하시겠습니까?")

                    if result:
                        # 강의 종료 시: 2차 지문 출석 포함한 전체 출석 마무리
                        log("🛑 출석 종료, 지문 출석 시작...")
                        controller.finalize_attendance(enrolled_students, misbehaving_students, lecture_id, lecture_title, log)
                        log("✅ 전체 출석 처리 완료")
                        break
                    else:
                        # 다시 블루투스 출석 시도
                        log("🔄 출석 루프 계속, 10초 후 재시도...")

                time.sleep(10)

        except Exception as e:
            log(f"[출석 처리 중 오류] {str(e)}")

    # 출석 시작 버튼 클릭 시 호출
    def start_attendance():
        lecture_id = lecture_entry.get().strip()
        if not lecture_id:
            messagebox.showwarning("입력 오류", "강의 ID를 입력하세요.")
            return
        # 출석 프로세스를 백그라운드 스레드에서 실행
        threading.Thread(target=run_attendance_process, args=(lecture_id,), daemon=True).start()

    # 출석 시작 버튼
    start_button = tk.Button(window, text="출석 시작", command=start_attendance)
    start_button.pack(pady=10)
