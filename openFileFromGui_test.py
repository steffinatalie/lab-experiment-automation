import tkinter as tk
from tkinter import filedialog
import os

class FileExplorer:
    def __init__(self, master):
        self.master = master
        self.master.title("File Explorer")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.button = tk.Button(self.frame, text="Browse", command=self.browse_files)
        self.button.pack(side="left")

        self.label = tk.Label(self.frame, text="")
        self.label.pack(side="left")

    def browse_files(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label.config(text=file_path)
            self.open_file(file_path)

    def open_file(self, file_path):
        try:
            os.startfile(file_path)
        except AttributeError:
            try:
                os.system(f"open {file_path}")
            except:
                print("Unable to open file.")

if __name__ == '__main__':
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()
