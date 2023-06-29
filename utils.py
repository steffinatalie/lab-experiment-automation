import settings
import os
from communicate_v2 import Communicate as com
import tkinter as tk
from tkinter import messagebox
import datetime
import os
import threading
import sys


def width_prct(percentage):
    return (settings.WINDOW_WIDTH / 100) * percentage

def height_prct(percentage):
    return (settings.WINDOW_HEIGHT / 100) * percentage

def create_path(folder):
    # creates the string only
    cwd = os.getcwd()
    dir = f"{cwd}\{folder}"
    return dir
        
def create_folder(folder):
    # not only create the string
    # it creates the actual folder
    dir = create_path(folder)
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    return dir

def conversion(x):
    # remove spaces and convert to float
    try:
        return float(x.strip())
    except:
        return None 
    
def calc_avg(data, start_col, end_col):
    return data.iloc[:, start_col:end_col].mean().mean()

def dummy():
    pass

# def kill():
#     com.publish_experiment_state(settings.KILLED)


# TO ASK FOR THE EXPERIMENT DIRECTORY NAME

class InputDialog(tk.Toplevel):
    def __init__(self, parent, default_text):
        super().__init__(parent)
        self.title("Input")
        self.geometry("400x150")
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
        # print(self.result)
        
        
        # create path to the folder
        path = create_path(f"{settings.FOLDER_READINGS}\{self.result}")
        
        # print(os.path.exists(path))
        
        # check if file already exist
        if os.path.exists(path) == False:
            # update folder path
            com.publish_experiment_folder_path(path)
            print("Folder path published")
            
            # create the folder
            create_folder(f"{settings.FOLDER_READINGS}\{self.result}")
            
            # publish folder name to GUI
            com.publish_experiment_folder_display(self.result)
            
            self.destroy()
        else:
            # if the previous input already exist
            # popup change or override
            self.lift()
            
            th = threading.Thread(target=self.warning())
            th.start()
            
            self.lift()
            # pass

    def cancel(self):
        self.destroy()
        
        
    def warning(self):
        messagebox.showerror(
            title="Warning",
            message="Experiment directory already exist!"
        )      

def ask_for_text(root):
    format = "%Y-%m-%d %H-%M-%S"
    default_text = f"Experiment{datetime.datetime.now().strftime(format)}"
    dialog = InputDialog(root, default_text)
    root.wait_window(dialog)
    text = dialog.result
    if text is not None:
        print("You entered:", com.experiment_folder_path)
        




# SERIAL FASTER READING METHOD

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)
    

# TO DISPLAY TERMINAL


def terminal():

    class Redirect():

        def __init__(self, widget, autoscroll=True):
            self.widget = widget
            self.autoscroll = autoscroll

        def write(self, text):
            self.widget.insert('end', text)
            if self.autoscroll:
                self.widget.see("end")  # autoscroll


    # --- main ---    

    root = tk.Tk()


    # - Frame with Text and Scrollbar -

    frame = tk.Frame(root)
    frame.pack(expand=True, fill='both')

    text = tk.Text(frame)
    text.pack(side='left', fill='both', expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side='right', fill='y')

    text['yscrollcommand'] = scrollbar.set
    scrollbar['command'] = text.yview

    old_stdout = sys.stdout    
    sys.stdout = Redirect(text)
    

    # - rest -

    root.mainloop()

    # - after close window -

    sys.stdout = old_stdout
    





    
    