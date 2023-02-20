from tkinter import Button
import settings

class LeftFrame:
    def __init__(self, location):
        self.location = location
        self.start_button = Button(
            self.location,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.start_button.grid(
            column=0, row=0
        )
        self.start_button.configure(
            text="Start"
        )
        #bind
        self.start_button.bind("<Button-1>", self.start)
        
        self.stop_button = Button(
            self.location,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.stop_button.grid(
            column=0, row=1
        )
        self.stop_button.configure(
            text="Stop"
        )
        # bind
        self.stop_button.bind("<Button-1>", self.stop)
    
    def start(self, event):
        self.start_button.config(
            state="disabled"
        )
        with open(settings.FILE, 'w') as f:
            f.write("start")
        self.stop_button.config(
            state="normal"
        )
        
    def stop(self, event):
        self.stop_button.config(
            state="disabled"
        )
        with open(settings.FILE, 'w') as f:
            f.write("stop")
        self.start_button.config(
            state="normal"
        )
        