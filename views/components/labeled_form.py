import tkinter as tk

class LabeledForm(tk.Frame):
    def __init__(self, master, labels, **kwargs):
        super().__init__(master, **kwargs)
        self.entries = {}  # {라벨: Entry 위젯}

        for i, label in enumerate(labels):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="e")
            entry = tk.Entry(self)
            entry.grid(row=i, column=1)
            self.entries[label] = entry

    # 모든 입력 필드의 값을 딕셔너리로 반환
    def get_values(self):
        return {label: entry.get().strip() for label, entry in self.entries.items()}

    # 모든 입력 필드 초기화
    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
