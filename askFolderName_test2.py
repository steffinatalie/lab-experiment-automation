import tkinter as tk
from tkinter import messagebox
import datetime
from communicate_v2 import Communicate as com
import os
import utils

class InputDialog(tk.Toplevel):
    def __init__(self, parent, default_text):
        super().__init__(parent)
        self.title("Input")
        self.geometry("300x150")
        self.default_text = default_text

        label = tk.Label(self, text="Enter experiment directory name\n(The datas will be saved in this directory):")
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
        print(self.result)
        
        
        # create path to the folder
        path = utils.create_path(self.result)
        
        # check if file already exist
        if os.path.exists(path) != False:
            # update folder name
            com.publish_experiment_folder_name(self.result)
            
            self.destroy()
        else:
            # if the previous input already exist
            # popup change or override
            self.messageWindow()
            # pass

    def cancel(self):
        self.destroy()
        
    def messageWindow(self):
        win = tk.Toplevel()
        win.title('Warning')
        message = "Experiment directory already exist\nDo you want to override it?"
        tk.Label(win, text=message).pack()
        tk.Button(win, text='Delete', command=win.destroy).pack()

def ask_for_text(root):
    default_text = f"Experiment({datetime.datetime.now()})"
    dialog = InputDialog(root, default_text)
    root.wait_window(dialog)
    text = dialog.result
    if text is not None:
        print("You entered:", text)
        

