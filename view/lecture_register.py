import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controllers.lecture_controller import LectureController

def open_lecture_register_window(root):
    controller = LectureController()
    window = tk.Toplevel(root)
    window.title("강의 등록")

    # 라벨과 입력 필드 리스트 (요일 제외)
    labels = [
        "강의명", "강의자 ID",
        "시작 시간 (HH:MM:SS)", "종료 시간 (HH:MM:SS)",
        "시작 날짜 (YYYY-MM-DD)", "종료 날짜 (YYYY-MM-DD)"
    ]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(window, text=label_text).grid(row=i, column=0, sticky="e") # 라벨 만들기
        entry = tk.Entry(window) # 입력 필드 만들기
        entry.grid(row=i, column=1)
        entries.append(entry) # 입력 필드 리스트에 생성한 입력 필드 추가

    # 요일 콤보박스 별도 추가
    tk.Label(window, text="요일 (월~금)").grid(row=len(labels), column=0, sticky="e")
    day_var = tk.StringVar()
    day_combobox = ttk.Combobox(window, textvariable=day_var, state="readonly")
    day_combobox['values'] = ("월", "화", "수", "목", "금")
    day_combobox.grid(row=len(labels), column=1)
    day_combobox.current(0)  # 기본값 '월' 설정

    # 제출
    def submit():
        # 사용자 입력값 수집
        title = entries[0].get().strip()
        professor_id = entries[1].get().strip()
        start_time = entries[2].get().strip()
        end_time = entries[3].get().strip()
        start_date = entries[4].get().strip()
        end_date = entries[5].get().strip()
        day = day_var.get()

        success = controller.register_lecture(title, day, professor_id, start_time, end_time, start_date, end_date)

        if success:
            messagebox.showinfo("성공", "강의 등록 완료")
        else:
            messagebox.showerror("실패", "강의 등록 실패")

    # 등록 버튼
    tk.Button(window, text="등록", command=submit).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
