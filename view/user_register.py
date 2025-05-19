import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController  # 컨트롤러 클래스 import

def open_user_register_window(root):
    controller = UserController()
    window = tk.Toplevel(root)  # 새 창 생성
    window.title("사용자 등록")

    # 공통 입력 라벨과 입력 필드 리스트
    labels = ["아이디", "비밀번호", "이름"]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(window, text=label_text).grid(row=i, column=0, sticky="e") # 라벨 만들기
        entry = tk.Entry(window) # 입력 필드 만들기
        entry.grid(row=i, column=1)
        entries.append(entry) # 입력 필드 리스트에 생성한 입력 필드 추가

    # 역할 선택 (학생 또는 교수)
    role_var = tk.StringVar(value='student')  # 기본값: student
    tk.Radiobutton(window, text="학생", variable=role_var, value='student').grid(row=3, column=0)
    tk.Radiobutton(window, text="교수", variable=role_var, value='professor').grid(row=3, column=1)

    # 역할에 따라 달라지는 추가 입력 필드 (학과/학번 또는 담당 학과)
    entry_extra1 = tk.Entry(window) # 학생
    entry_extra2 = tk.Entry(window) # 교수

    # 역할 변경 시 필드 업데이트
    def update_fields(*args):
        # 기존에 추가된 행(4, 5) 제거
        for widget in window.grid_slaves():
            if int(widget.grid_info()["row"]) in [4, 5]:
                widget.grid_forget()

        # 학생일 경우: 학과 + 학번
        if role_var.get() == "student":
            tk.Label(window, text="학과").grid(row=4, column=0, sticky="e")
            entry_extra1.grid(row=4, column=1)
            tk.Label(window, text="학번").grid(row=5, column=0, sticky="e")
            entry_extra2.grid(row=5, column=1)
        # 교수일 경우: 담당 학과만
        else:
            tk.Label(window, text="담당 학과").grid(row=4, column=0, sticky="e")
            entry_extra1.grid(row=4, column=1)

    # 역할이 변경될 때 update_fields 실행
    role_var.trace("w", update_fields)
    update_fields()  # 초기 호출

    # 제출
    def submit():
        # 사용자 입력값 수집
        login_id = entries[0].get().strip()
        password = entries[1].get().strip()
        name = entries[2].get().strip()
        role = role_var.get()

        # 역할에 따라 다른 메서드 호출
        if role == "student":
            major = entry_extra1.get().strip()
            student_number = entry_extra2.get().strip()
            success = controller.register_student(login_id, password, name, major, student_number)
            if success:
                messagebox.showinfo("성공", "학생 등록 완료")
            else:
                messagebox.showerror("실패", "학생 등록 실패")

        elif role == "professor":
            department = entry_extra1.get().strip()
            success = controller.register_professor(login_id, password, name, department)
            if success:
                messagebox.showinfo("성공", "교수 등록 완료")
            else:
                messagebox.showerror("실패", "교수 등록 실패")

    # 등록 버튼
    tk.Button(window, text="등록", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
