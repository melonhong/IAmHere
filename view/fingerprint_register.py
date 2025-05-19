import tkinter as tk
from tkinter import messagebox
from controllers.fingerprint_controller import FingerprintController
from fingerprint import *

def open_fingerprint_register_window(root):
    controller = FingerprintController()
    window = tk.Toplevel(root)
    window.title("지문 등록")

    tk.Label(window, text="학생 ID").grid(row=0, column=0, sticky="e")
    entry = tk.Entry(window)
    entry.grid(row=0, column=1)

    def on_scan():
        fingerprint_data = scan_fingerprint()
        if fingerprint_data:
            # 지문 스캔 성공
            messagebox.showinfo("성공", "지문 스캔 성공")
            return fingerprint_data
        else:
            # 지문 스캔 실패
            messagebox.showerror("실패", "지문 스캔 실패")
    tk.Button(window, text="지문 스캔", command=on_scan).grid(row=1, column=0, columnspan=2, pady=10)


    # 제출
    def submit():
        success = controller.register_enrollment(
            entry.get().strip(),  # 학생 ID
            on_scan(),  # 지문 데이터
        )

        if success:
            messagebox.showinfo("성공", "지문 등록 완료")
        else:
            messagebox.showerror("실패", "지문 등록 실패")

    # 등록 버튼
    tk.Button(window, text="등록", command=submit).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
