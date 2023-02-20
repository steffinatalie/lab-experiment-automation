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
        # bind
        # bind
        # bind
        
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
        # bind
        # bind
        