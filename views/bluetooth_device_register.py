import tkinter as tk
from tkinter import messagebox
from controllers.bluetooth_device_controller import BluetoothDeviceController
from views.components.labeled_form import LabeledForm

def open_bluetooth_device_register_window(root):
    controller = BluetoothDeviceController()
    window = tk.Toplevel(root)
    window.title("강의자의 블루투스 기기 등록")

    # 라벨과 입력 필드 리스트 (요일 제외)
    labels = ["강의자 ID", "MAC 주소", "기기 이름"]
    form = LabeledForm(window, labels)
    form.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # 제출
    def submit():
        # 사용자 입력값 수집
        values = form.get_values()

        success = controller.register_enrollment(
            values["강의자 ID"], 
            values["MAC 주소"],
            values["기기 이름"]
        )

        if success:
            messagebox.showinfo("성공", "블루투스 기기 등록 완료")
        else:
            messagebox.showerror("실패", "블루투스 기기 등록 실패")

    # 등록 버튼
    tk.Button(window, text="등록", command=submit).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
