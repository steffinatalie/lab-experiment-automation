from tkinter import Button, Text, Label, messagebox, StringVar, OptionMenu
import settings
import threads
from communicate_v2 import Communicate as com
import threading
import serial.tools.list_ports as port_list

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

    def pause():
        pass
        
    def error_time_config_popup(self):
        messagebox.showerror(
            title="Error",
            message="Invalid time configurations"
        )
        
    def experiment_state_callback(self):
        experiment_state = com.update_experiment_state()
        
        while experiment_state == settings.START:
            experiment_state = com.update_experiment_state()
        
        self.start_button.config(
            state="normal"
        )
        self.stop_button.config(
            state="disabled"
        )
        
        
class LeftTopFrame:
    def __init__(self, location):
        self.location = location
        
        
        
        
        self.label = Label(self.location, text="Select Port: ", font='Helvetica 10 bold', background="white")
        self.label.grid(
            column=0, row=0, columnspan=2
        )
        
        
        
        
        self.sensor_port_variable = StringVar()
        self.sensor_port_variable.set("SENS")
        
        self.sensor_port_option_menu = OptionMenu(self.location, self.sensor_port_variable, self.get_serial_ports)
        self.sensor_port_option_menu.grid(column=0, row=1)
        
        # self.apply_button = Button(self.location, 
        #                            text="Apply", 
        #                            command=self.sensor_apply_port, 
        #                            width=settings.BUTTON_WIDTH,
        #                            height=settings.BUTTON_HEIGHT,)
        # self.apply_button.grid(column=0, row=2)
        
        
        
        
        self.actuator_port_variable = StringVar()
        self.actuator_port_variable.set("ACTU")
        
        self.actuator_port_option_menu = OptionMenu(self.location, self.actuator_port_variable, self.get_serial_ports)
        self.actuator_port_option_menu.grid(column=1, row=1)
        
        # self.apply_button = Button(self.location, 
        #                            text="Apply", 
        #                            command=self.actuator_apply_port, 
        #                            width=settings.BUTTON_WIDTH,
        #                            height=settings.BUTTON_HEIGHT,)
        # self.apply_button.grid(column=1, row=2)
        
        """
        Publish the selected port when start clicked
        
        """
        
        
        
    @property
    def get_serial_ports(self):
        ports = []
        for port in port_list.comports():
            ports.append(port.device)
            print(port)
        return ports
        
    # def sensor_apply_port(self):
    #     pass
    
    # def actuator_apply_port(self):
    #     pass
        
        

        
        
        
        