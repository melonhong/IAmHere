import tkinter as tk
from view.user_register import open_user_register_window
from view.lecture_register import open_lecture_register_window
from view.enrollment_register import open_enrollment_register_window
from view.bluetooth_device_register import open_bluetooth_device_register_window
from view.fingerprint_register import open_fingerprint_register_window
from view.bluetooth_device_pair import open_bluetooth_device_pair_window
from view.attendance import open_attendance_window

def run_gui():
    root = tk.Tk()
    root.title("출석 시스템 관리 프로그램")
    root.geometry("400x400")

    tk.Label(root, text="메인 메뉴", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="사용자 등록", command=lambda: open_user_register_window(root), width=30).pack(pady=5)
    tk.Button(root, text="강의 등록", command=lambda: open_lecture_register_window(root), width=30).pack(pady=5)
    tk.Button(root, text="수강신청", command=lambda: open_enrollment_register_window(root), width=30).pack(pady=5)
    tk.Button(root, text="블루투스 기기 등록", command=lambda: open_bluetooth_device_register_window(root), width=30).pack(pady=5)
    tk.Button(root, text="지문 등록", command=lambda: open_fingerprint_register_window(root), width=30).pack(pady=5)
    tk.Button(root, text="블루투스 기기 페어링", command=lambda: open_bluetooth_device_pair_window(root), width=30).pack(pady=5)
    tk.Button(root, text="출석 시작", command=lambda: open_attendance_window(root), width=30).pack(pady=5)
    tk.Button(root, text="종료", command=root.quit, width=30).pack(pady=5)

    root.mainloop()
