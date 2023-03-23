import tkinter as tk
import datetime
from communicate_v2 import Communicate as com

class InputDialog(tk.Toplevel):
    def __init__(self, parent, default_text):
        super().__init__(parent)
        self.title("Input")
        self.geometry("300x100")
        self.default_text = default_text

        label = tk.Label(self, text="Enter some text:")
        label.pack(pady=10)

        self.entry = tk.Entry(self, width=30)
        self.entry.pack(pady=5)
        self.entry.insert(0, self.default_text)

        button_ok = tk.Button(self, text="OK", command=self.ok)
        button_ok.pack(side="left", padx=10, pady=10)

        button_cancel = tk.Button(self, text="Cancel", command=self.cancel)
        button_cancel.pack(side="right", padx=10, pady=10)

        self.result = None

    def ok(self):
        self.result = self.entry.get()
        self.destroy()
        
        # update folder name
        com.publish_experiment_folder_name(self.result)

    def cancel(self):
        self.destroy()

def ask_for_text(root):
    default_text = f"Experiment({datetime.datetime.now()})"
    dialog = InputDialog(root, default_text)
    root.wait_window(dialog)
    text = dialog.result
    if text is not None:
        print("You entered:", text)

