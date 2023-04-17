from tkinter import Button, Text, Label, messagebox
import settings
import threads
from communicate_v2 import Communicate as com
import threading
import os

"""
TODO:
- display count executions
- button for actuator move 
- widget for changing com port
- try daemon thread
- create n minutes n seconds left until the next reading
- display reading countdown
- create serial monitor or graph ???
- create experiment time estimation
- create warning before closing window during experiment (experiment must be stopped first, if not stopped window can't be closed)
- create warning if experiment stopped when sensors are still below the heater
- create pause and continue
- connect this to discord bot so it would call bang normen during emergency wkwkwwk
- save latest time config
- create experiment log
"""

class LeftBottomFrame:
    def __init__(self, location):
        self.location = location
        
        self.section_title = Label(
            self.location,
            text="Log",
            font='Helvetica 9 bold',
            background="white"
        )
        self.section_title.grid(column=0, row=0)
        
        self.label_test = Label(
            self.location,
            text="Nothing is running                                                                                  \n\n\n\n\n\n\n\n\n",
            background="black",
            fg="white"    
        )
        self.label_test.grid(column=0, row=1, padx=5, pady=5, sticky='w'+'e')
        
        
        
        
        
        

class LeftMiddleFrame:
    def __init__(self, location):
        self.location = location
        
        self.section_title = Label(
            self.location,
            text="Status",
            font='Helvetica 9 bold'
        )
        self.section_title.grid(column=0, row=0, sticky='w')
        
        # self. = Label(
        #     self.location,
        #     text=""
        # )
    #     self.label_n = Label(
    #         self.location,
    #         text = f"Executed               :   0 times"
    #     )
    #     self.label_n.grid(column=0, row=1, sticky='w')
        
    #     self.label_estimation = Label(
    #         self.location,
    #         text = f"End time estimation    :          "
    #     )
    #     self.label_estimation.grid(column=0, row=2, sticky='w')
        
    #     self.label_sensors_position = Label(
    #         self.location,
    #         text="Sensors position           :          "
    #     )
    #     self.label_sensors_position.grid(column=0, row=3, sticky='w')
        
    #     th = threading.Thread(target=self.status_update)
    #     th.start()

    # def status_update(self):
    #     experiment_state = com.experiment_state
    #     while experiment_state != settings.KILLED:
    #         # print("status")
    #         n = com.count_executions
    #         if n == None:
    #             n = 0
            
    #         self.label_n["text"] = f"Executed :   {n} times"
    #         experiment_state = com.experiment_state
            
    #     print("hey i am dead")
        







class LeftTopFrame:
    def __init__(self, location):
        self.location = location
        
        
        
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
        
        # thr = threading.Thread(target=)
        
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
            
            # this sometimes can cause error jut because the main loop is closed
            # before this one is done, but it is fine
            # th = threading.Thread(target=self.experiment_state_callback)
            # th.start()

        
        except:
            # pop up
            th = threading.Thread(target=self.error_time_config_popup)
            th.start()

        
    def stop(self, event):

        com.publish_experiment_state(settings.STOP)
        
        self.start_button.config(
                state="normal"
            )
            
        self.stop_button.config(
            state="disabled"
        )

        
    def pause(self, event):
        pass
        
    def error_time_config_popup(self):
        messagebox.showerror(
            title="Error",
            message="Invalid time configurations"
        )
        
    def experiment_state_callback(self):
        experiment_state = com.experiment_state
        
        while experiment_state == settings.START:
            experiment_state = com.experiment_state
        
        self.start_button.config(
            state="normal"
        )
        self.stop_button.config(
            state="disabled"
        )
        
        
        
        

        
        
        
        