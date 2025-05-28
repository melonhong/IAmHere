import tkinter as tk
from tkinter import messagebox
from controllers.enrollment_controller import EnrollmentController
from views.components.labeled_form import LabeledForm

def open_enrollment_register_window(root):
    controller = EnrollmentController()
    window = tk.Toplevel(root)
    window.title("수강신청")

    # 라벨과 입력 필드 리스트 (요일 제외)
    labels = ["학생 ID", "강의 ID"]
    form = LabeledForm(window, labels)
    form.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # 제출
    def submit():
        # 사용자 입력값 수집
        values = form.get_values()

        success = controller.register_enrollment(
            values["학생 ID"], 
            values["강의 ID"],
        )

        if success:
            messagebox.showinfo("성공", "수강신청 완료")
        else:
            messagebox.showerror("실패", "수강신청 실패")

    # 등록 버튼
    tk.Button(window, text="등록", command=submit).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
