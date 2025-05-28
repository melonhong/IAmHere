import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
from views.components.labeled_form import LabeledForm

def open_user_register_window(root):
    controller = UserController()

    window = tk.Toplevel(root)  # 새 창 생성
    window.title("사용자 등록")

    labels = ["아이디", "비밀번호", "이름"] # 라벨 리스트
    form = LabeledForm(window, labels)
    form.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # 역할 선택 (학생 또는 교수)
    role_var = tk.StringVar(value='student')  # 기본값: student
    tk.Radiobutton(window, text="학생", variable=role_var, value='student').grid(row=3, column=0)
    tk.Radiobutton(window, text="교수", variable=role_var, value='professor').grid(row=3, column=1)

    # 역할에 따라 달라지는 추가 입력 필드 (학과/학번 또는 담당 학과)
    entry_student = tk.Entry(window) # 학생
    entry_professor = tk.Entry(window) # 교수

    # 역할 변경 시 필드 업데이트
    def update_fields(*args):
        # 기존에 추가된 행(4, 5) 제거
        for widget in window.grid_slaves():
            if int(widget.grid_info()["row"]) in [4, 5]:
                widget.grid_forget()

        # 학생일 경우: 학과 + 학번
        if role_var.get() == "student":
            tk.Label(window, text="학과").grid(row=4, column=0, sticky="e")
            entry_student.grid(row=4, column=1)
            tk.Label(window, text="학번").grid(row=5, column=0, sticky="e")
            entry_professor.grid(row=5, column=1)
        # 교수일 경우: 담당 학과만
        else:
            tk.Label(window, text="담당 학과").grid(row=4, column=0, sticky="e")
            entry_student.grid(row=4, column=1)

    # 역할이 변경될 때 update_fields 실행
    role_var.trace("w", update_fields)
    update_fields()  # 초기 호출

    # 제출
    def submit():
        # 사용자 입력값 수집
        values = form.get_values()
        role = role_var.get()

        # 역할에 따라 다른 메서드 호출
        if role == "student":
            major = entry_student.get().strip()
            student_number = entry_professor.get().strip()
            success = controller.register_student(
                values["아이디"],
                values["비밀번호"],
                values["이름"],
                major, student_number
            )
            if success:
                messagebox.showinfo("성공", "학생 등록 완료")
            else:
                messagebox.showerror("실패", "학생 등록 실패")

        elif role == "professor":
            department = entry_student.get().strip()
            success = controller.register_professor(
                values["아이디"],
                values["비밀번호"],
                values["이름"], 
                department
            )
            if success:
                messagebox.showinfo("성공", "교수 등록 완료")
            else:
                messagebox.showerror("실패", "교수 등록 실패")

    # 등록 버튼
    tk.Button(window, text="등록", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
