from tkinter import Button, Text, Label
import settings
import threads
from communicate import PublishToThreads as pub
from communicate import GUIUpdate as update
from communicate_v2 import Communicate as com

"""
TODO:
display how many executions executed
create n minutes n seconds left until the next reading
display reading countdown
create serial monitor
create experiment time estimation
create warning before closing window during experiment
what if you 'modularized' all the write and read ahshahs


when window destroyed, kill the other process, but make sure all the files are already flushed 
"""

class LeftFrame:
    def __init__(self, location):
        self.location = location
        self.is_running = False
        
        
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
        
        
       
        
        
        
        
        
    # create error input handling
    # create error input handling
    # create error input handling
        
        
    def start(self, event):
        self.start_button.config(
            state="disabled"
        )
        

        com.publish_experiment_state(settings.START)
        
        time_config = [self.input_time_interval.get(1.0, "end-1c") + '\n', 
                       self.input_read_duration.get(1.0, "end-1c") + '\n',
                       self.input_executions.get(1.0, "end-1c") + '\n']
        
        com.publish_time_config(time_config)
        
        
        
        # run threads.py
        threads.main()
        
        self.stop_button.config(
            state="normal"
        )
        
        self.is_running = True
        
    def stop(self, event):
        self.stop_button.config(
            state="disabled"
        )
        # with open(settings.FILE_EXPERIMENT_STATE, 'w') as f:
        #     f.write("stop")
        # pub.experiment_state(settings.STOP)
        com.publish_experiment_state(settings.STOP)
        
        self.start_button.config(
            state="normal"
        )
        
        