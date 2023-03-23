import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()

def ask_for_text():
    default_text = "Hello, World!"
    text = simpledialog.askstring("Input", "Enter some text:", initialvalue=default_text)
    print("You entered:", text)

button = tk.Button(root, text="Click me!", command=ask_for_text)
button.pack()

root.mainloop()
