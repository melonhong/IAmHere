import tkinter as tk
from tkinter import messagebox
from controllers.attendance_controller import AttendanceController
from bluetooth import is_connected
import threading
import time

def open_attendance_window(root):
    window = tk.Toplevel(root)
    window.title("📘 출석 시작")
    window.geometry("500x400")

    tk.Label(window, text="강의 ID를 입력하세요:").pack(pady=10)
    lecture_entry = tk.Entry(window)
    lecture_entry.pack()

    output = tk.Text(window, height=12)
    output.pack(pady=10)

    def log(message):
        output.insert(tk.END, message + "\n")
        output.see(tk.END)

        def run_attendance_process(lecture_id):
        controller = AttendanceController()
        try:
            log("강의 정보 불러오는 중...")
            lecture_id, lecture_title, mac_addr, enrolled_students, user_mac_map = controller.get_attendance_context(lecture_id)

            if not mac_addr:
                log("❌ 교수님의 블루투스 주소를 찾을 수 없습니다.")
                messagebox.showerror("주소 오류", "교수님의 블루투스 주소를 찾을 수 없습니다.")
                return

            log(f"📡 교수 블루투스 주소: {mac_addr}")
            log(f"📚 강의 제목: {lecture_title}")
            log(f"👨‍🎓 출석 대상 학생 수: {len(enrolled_students)}")
            log(f"👨‍🎓 출석 대상 학생 목록: {enrolled_students}")
            log("⏳ 블루투스 연결 시도 중...")

            start_time = time.time()
            connected = False
            while time.time() - start_time < 10:
                if is_connected(mac_addr):
                    connected = True
                    break
                time.sleep(1)

            if not connected:
                log("❌ 블루투스 연결 실패")
                messagebox.showerror("연결 실패", "교수님의 블루투스 장치 연결에 실패했습니다.")
                return

            log("✅ 연결 성공! 블루투스 출석을 시작합니다.")
        except Exception as e:
            log(f"[출석 준비 중 오류] {str(e)}")
            return

        try:
            misbehaving_students = []
            while True:
                if is_connected(mac_addr):
                    log("📡 블루투스 연결 상태 확인됨. 출석 처리 중...")
                    misbehaving_students = controller.process_attendance(
                        lecture_id, mac_addr, enrolled_students, user_mac_map
                    )
                    log(f"⚠️ 출석 실패자: {list(misbehaving_students)}")

                    if not misbehaving_students:
                        log("🎉 모든 학생이 출석을 완료했습니다!")
                        break
                else:
                    log("🔌 블루투스 연결이 끊어졌습니다.")
                    result = messagebox.askyesno("강의 종료 확인", "블루투스 연결이 끊어졌습니다. 강의를 종료하시겠습니까?")
                    if result:
                        log("🛑 강의 출석을 종료합니다.")
                        controller.finalize_attendance(enrolled_students, misbehaving_students, lecture_id, lecture_title)
                        log("✅ 전체 출석 처리 완료")
                        break
                    else:
                        log("🔄 출석 루프를 계속합니다. 10초 후 재시도...")

                time.sleep(10)

            if misbehaving_students:
                log("🧪 2차 지문 출석을 시작합니다...")
                controller.finalize_attendance(enrolled_students, misbehaving_students, lecture_id, lecture_title)
                log("✅ 전체 출석 처리 완료")

        except Exception as e:
            log(f"[출석 처리 중 오류] {str(e)}")

    def start_attendance():
        lecture_id = lecture_entry.get().strip()
        if not lecture_id:
            messagebox.showwarning("입력 오류", "강의 ID를 입력하세요.")
            return
        threading.Thread(target=run_attendance_process, args=(lecture_id,), daemon=True).start()

    start_button = tk.Button(window, text="출석 시작", command=start_attendance)
    start_button.pack(pady=10)
