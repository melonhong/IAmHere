import tkinter as tk
from tkinter import messagebox
from models import UserDAO, StudentDAO, ProfessorDAO

user_dao = UserDAO()
student_dao = StudentDAO()
professor_dao = ProfessorDAO()

def open_user_register_window(root):
    window = tk.Toplevel(root) # 새로운 창 생성

    # 창 제목
    window.title("사용자 등록")

    # 아이디 섹션
    tk.Label(window, text="아이디").grid(row=0, column=0)
    entry_id = tk.Entry(window)
    entry_id.grid(row=0, column=1)

    # 비밀번호 섹션
    tk.Label(window, text="비밀번호").grid(row=1, column=0)
    entry_pw = tk.Entry(window, show="*")
    entry_pw.grid(row=1, column=1)

    # 이름 섹션
    tk.Label(window, text="이름").grid(row=2, column=0)
    entry_name = tk.Entry(window)
    entry_name.grid(row=2, column=1)

    # 학생 또는 교수 선택 섹션
    role_var = tk.StringVar(value='student')
    tk.Radiobutton(window, text="학생", variable=role_var, value='student').grid(row=3, column=0)
    tk.Radiobutton(window, text="교수", variable=role_var, value='professor').grid(row=3, column=1)

    entry_extra1 = tk.Entry(window)
    entry_extra2 = tk.Entry(window)

    def update_fields(*args): # 학생 또는 교수에 따라 선택 항목이 달라짐
        for widget in window.grid_slaves():
            if int(widget.grid_info()["row"]) in [4, 5]:
                widget.grid_forget()
        if role_var.get() == "student": # 학생을 선택할 경우
            tk.Label(window, text="학과").grid(row=4, column=0)
            entry_extra1.grid(row=4, column=1)
            tk.Label(window, text="학번").grid(row=5, column=0)
            entry_extra2.grid(row=5, column=1)
        else: # 교수를 선택할 경우
            tk.Label(window, text="담당 학과").grid(row=4, column=0)
            entry_extra1.grid(row=4, column=1)

    role_var.trace("w", update_fields)
    update_fields()

    def submit():
        login_id = entry_id.get().strip()
        password = entry_pw.get().strip()
        name = entry_name.get().strip()
        role = role_var.get()

        if role == 'student':
            user_id = user_dao.add_user(login_id, password, name, role)
            if user_id:
                major = entry_extra1.get().strip()
                student_number = entry_extra2.get().strip()
                if student_dao.add_student(user_id, major, student_number):
                    messagebox.showinfo("성공", "학생 등록 완료")
                else:
                    messagebox.showerror("실패", "학생 정보 등록 실패")
            else:
                messagebox.showerror("실패", "사용자 등록 실패")

        elif role == 'professor':
            user_id = user_dao.add_user(login_id, password, name, role)
            if user_id:
                department = entry_extra1.get().strip()
                if professor_dao.add_professor(user_id, department):
                    messagebox.showinfo("성공", "교수 등록 완료")
                else:
                    messagebox.showerror("실패", "교수 정보 등록 실패")
            else:
                messagebox.showerror("실패", "사용자 등록 실패")

    tk.Button(window, text="등록", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
