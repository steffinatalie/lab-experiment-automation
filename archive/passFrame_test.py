import tkinter as tk

class Frame1(tk.Frame):
    def __init__(self, master, frame2):
        super().__init__(master)
        self.frame2 = frame2  # pass a reference to Frame2 as an argument
        self.button = tk.Button(self, text="Click me", command=self.disable_button)
        self.button.pack()

    def disable_button(self):
        self.frame2.button.config(state="disabled")

class Frame2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.button = tk.Button(self, text="I'm here")
        self.button.pack()

root = tk.Tk()
frame2 = Frame2(root)
frame1 = Frame1(root, frame2)
frame1.pack()
frame2.pack()

root.mainloop()
