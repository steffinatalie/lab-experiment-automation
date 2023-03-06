from tkinter import Button, Text, Label, messagebox
import settings
import threads
from communicate_v2 import Communicate as com

"""
TODO:
- display how many executions executed
- create n minutes n seconds left until the next reading
- display reading countdown
- create serial monitor
- create experiment time estimation
- create warning before closing window during experiment
- create warning if experiment stopped when sensors are still below the heater
- create pause and continue
- make sure all csv flushed before program terminated
- error input handing
- connect this to discord bot so it would call bang normen during emergency wkwkwwk
- handling when started without time config
- save previous time config
- pop up window when start pressed for making sure about experiment configurations
"""

class LeftFrame:
    def __init__(self, root, location):
        self.root = root
        self.location = location
        self.is_running = False
        
        
        
        # START BUTTON
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
        
        
        
        # STOP BUTTON
        self.stop_button = Button(
            self.location,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.stop_button.grid(
            column=0, row=2
        )
        self.stop_button.configure(
            text="Stop"
        )
        self.stop_button.config(
            state="disabled"
        )
        # bind
        self.stop_button.bind("<Button-1>", self.stop)
        
        
        
        
        # PAUSE BUTTON
        self.pause_button = Button(
            self.location,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.pause_button.grid(
            column=0, row=1
        )
        self.pause_button.configure(
            text="Pause"
        )
        self.pause_button.config(
            state="disabled"
        )
        #bind
        self.pause_button.bind("<Button-1>", self.pause)
        
        
        
        # TIME CONFIGS
        self.label_time_interval = Label(
            self.location,
            text="Time Interval (m)  "
        )
        self.label_time_interval.grid(
            column=1, row=1, sticky='e'
        )
        
        self.input_time_interval = Text(
            self.location,
            width=settings.INPUT_TEXT_WIDTH,
            height=settings.INPUT_TEXT_HEIGHT
        )
        self.input_time_interval.grid(
            column=2, row=1
        )
        
        
        self.label_read_duration = Label(
            self.location,
            text="Read Duration (s)  "
        )
        self.label_read_duration.grid(
            column=1, row=2, sticky='e'
        )
        
        self.input_read_duration = Text(
            self.location,
            width=settings.INPUT_TEXT_WIDTH,
            height=settings.INPUT_TEXT_HEIGHT
        )
        self.input_read_duration.grid(
            column=2, row=2
        )
        
        
        self.label_executions = Label(
            self.location,
            text="                       Executions (n times)  "
        )
        self.label_executions.grid(
            column=1, row=3
        )
        
        self.input_executions = Text(
            self.location,
            width=settings.INPUT_TEXT_WIDTH,
            height=settings.INPUT_TEXT_HEIGHT
        )
        self.input_executions.grid(
            column=2, row=3
        )
        
        
        
    def start(self, event):
        
        try:
        
            time_config = [int(float(self.input_time_interval.get(1.0, "end-1c"))), 
                        int(float(self.input_read_duration.get(1.0, "end-1c"))),
                        int(float(self.input_executions.get(1.0, "end-1c")))]
        
            com.publish_experiment_state(settings.START)
            com.publish_time_config(time_config)
            
            # run threads.py
            threads.main()
            
            self.start_button.config(
                state="disabled"
            )
            
            self.stop_button.config(
                state="normal"
            )
            
            self.is_running = True
        
        except:
            # pop up
            self.root.after(3000, self.empty_time_config_popup())
        
    def stop(self, event):
        self.stop_button.config(
            state="disabled"
        )

        com.publish_experiment_state(settings.STOP)
        
        self.start_button.config(
            state="normal"
        )
        
    def pause(self, event):
        pass
        
    def empty_time_config_popup(self):
        messagebox.showerror(
            title="Error",
            message="Empty time configurations"
        )
        