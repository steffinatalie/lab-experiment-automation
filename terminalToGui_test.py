import tkinter as tk
import sys

"""
perhaps write the logs to file
"""

# --- classes ---

def main():

    class Redirect():

        def __init__(self, widget, autoscroll=True):
            self.widget = widget
            self.autoscroll = autoscroll

        def write(self, text):
            self.widget.insert('end', text)
            if self.autoscroll:
                self.widget.see("end")  # autoscroll
            
        def flush(self):
           pass


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