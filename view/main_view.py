import tkinter as tk
from view.user_register_view import open_user_register_window

def run_gui():
    root = tk.Tk()
    root.title("출석 시스템 관리 프로그램")
    root.geometry("400x400")

    tk.Label(root, text="메인 메뉴", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="사용자 등록", command=lambda: open_user_register_window(root), width=30).pack(pady=5)
    tk.Button(root, text="종료", command=root.quit, width=30).pack(pady=5)

    root.mainloop()
