import tkinter as tk
from tkinter import messagebox
from controllers.attendance_controller import AttendanceController
from bluetooth import is_connected
import threading
import time
import traceback

def open_attendance_window(root):
    window = tk.Toplevel(root)
    window.title("📘 Start Attendance")
    window.geometry("500x400")

    tk.Label(window, text="Enter Lecture ID:").pack(pady=10)
    lecture_entry = tk.Entry(window)
    lecture_entry.pack()

    output = tk.Text(window, height=12)
    output.pack(pady=10)

    def log(message):
        output.insert(tk.END, message + "\n")
        output.see(tk.END)

    def run_attendance_process(lecture_id):
        controller = AttendanceController()
        try:
            log("Loading lecture information...")
            lecture_id, lecture_title, mac_addr, enrolled_students, user_mac_map = controller.get_attendance_context(lecture_id)

            if not mac_addr:
                log("❌ Could not find professor's Bluetooth address.")
                messagebox.showerror("Address Error", "Could not find professor's Bluetooth address.")
                return

            log(f"📡 Professor Bluetooth Address: {mac_addr}")
            log(f"📚 Lecture Title: {lecture_title}")
            log(f"👨‍🎓 Number of Enrolled Students: {len(enrolled_students)}")
            log(f"👨‍🎓 Enrolled Students: {enrolled_students}")
            log("⏳ Attempting to connect via Bluetooth...")

            start_time = time.time()
            connected = False
            while time.time() - start_time < 10:
                if is_connected(mac_addr):
                    connected = True
                    break
                time.sleep(1)

            if not connected:
                log("❌ Bluetooth connection failed")
                messagebox.showerror("Connection Failed", "Failed to connect to professor's Bluetooth device.")
                return

            log("✅ Connection successful! Starting Bluetooth attendance.")
            misbehaving_students = controller.process_attendance(
                lecture_id, mac_addr, enrolled_students, user_mac_map
            )

            log(f"⚠️ Attendance failed for: {list(misbehaving_students)}")
            log("🧪 Starting fingerprint verification...")
            controller.finalize_attendance(enrolled_students, misbehaving_students, lecture_id, lecture_title, logger=log)

            log("✅ Attendance process completed.")

        except Exception as e:
            log(f"[Error] {str(e)}")
            log(traceback.format_exc())
            messagebox.showerror("Error Occurred", str(e))

    def start_attendance():
        lecture_id = lecture_entry.get().strip()
        if not lecture_id:
            messagebox.showwarning("Input Error", "Please enter a Lecture ID.")
            return
        threading.Thread(target=run_attendance_process, args=(lecture_id,), daemon=True).start()

    start_button = tk.Button(window, text="Start Attendance", command=start_attendance)
    start_button.pack(pady=10)
