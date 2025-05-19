import tkinter as tk
from tkinter import messagebox
from controllers.bluetooth_device_controller import BluetoothDeviceController
from view.components.labeled_form import LabeledForm
from bluetooth import *

def open_bluetooth_device_register_window(root):
    controller = BluetoothDeviceController()
    window = tk.Toplevel(root)
    window.title("강의자의 블루투스 기기 페어링")

    # 라벨과 입력 필드 리스트 (요일 제외)
    labels = ["강의 ID"]
    form = LabeledForm(window, labels)
    form.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # 제출
    def submit():
        values = form.get_values()
        mac_addr = controller.get_mac_addr(values["강의 ID"])

        if mac_addr:
            result = pair_device(mac_addr)
            if result:
                messagebox.showinfo("성공", "블루투스 기기 페어링 완료")
            else:
                messagebox.showerror("실패", "블루투스 기기 페어링 실패")
        else:
            messagebox.showerror("실패", "블루투스 기기 페어링 실패")

    # 등록 버튼
    tk.Button(window, text="페어링", command=submit).grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
