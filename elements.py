from tkinter import Button, Text, Label, messagebox, StringVar, OptionMenu
import settings
import threads
from communicate_v2 import Communicate as com
import threading
import serial.tools.list_ports as port_list
import time

"""
TODO:
- disable manual when auto
- check the select port using two arduinos
- check whether port is flipped
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
            
        try:
            print(com.publish_port_state() + 1)
        
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
            
            th = threading.Thread(target=self.error_popup)
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

    def error_popup(self):
        msg = "Invalid time configurations"
        if com.update_actuator_port() == None or com.update_sensor_port() == None:
            msg = "Invalid ports \nand time configurations"
        messagebox.showerror(
            title="Error",
            message=msg
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
        
        
class LeftBottomFrame:
    def __init__(self, location):
        self.location = location
            
            
        self.manual_control_label = Label(
            self.location,
            text="MANUAL CONTROL",
            font='Helvetica 8 bold', 
            background="lightgrey"
        )
        self.manual_control_label.grid(
            column=2, row = 0, columnspan=2, padx=50, pady=7
            )
        
        self.start_read_button = Button(
            self.location,
            text="Start Read",
            command=self.dummy,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT
        )
        self.start_read_button.grid(
            column=3, row=1, rowspan=2, sticky='n'
        )
        
        self.save_read_button = Button(
            self.location,
            text="Save Data",
            command=self.dummy,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT
        )
        self.save_read_button.grid(
            column=3, row=2, rowspan=2, sticky='n', pady= 5
        )
        
        self.push_actuator_button = Button(
            self.location,
            text="Push", 
            command=self.push_actuator, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT
        )
        self.push_actuator_button.grid(
            column=2, row=1, rowspan=2, padx=10, sticky='n'
        )
        
        self.idle_actuator_button = Button(
            self.location,
            text="Idle", 
            command=self.idle_actuator, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT
        )
        self.idle_actuator_button.grid(
            column=2, row=2, rowspan=2, padx=10, pady= 5, sticky='n'
        )
        
        self.pull_actuator_button = Button(
            self.location,
            text="Pull", 
            command=self.pull_actuator, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT
        )
        self.pull_actuator_button.grid(
            column=2, row=3, rowspan=2, padx=10, sticky='n'
        )
        
        
        
        self.select_port_label = Label(
            self.location, 
            text="SELECT PORT", 
            font='Helvetica 8 bold', 
            background="lightgrey")
        self.select_port_label.grid(
            column=0, row=0, columnspan=2, padx=40, pady=7
        )
        
        self.sensor_label = Label(
            self.location,
            text="Sensor:",
            background="lightgrey"
        )
        self.sensor_label.grid(
            column=0, row=1
        )
        
        self.actuator_label = Label(
            self.location,
            text="Actuator:",
            background="lightgrey"
        )
        self.actuator_label.grid(
            column=1, row=1
        )
        
        
        self.sensor_port_variable = StringVar()
        self.sensor_port_variable.set("None")
        
        self.sensor_port_option_menu = OptionMenu(self.location, self.sensor_port_variable, self.get_ports)
        self.sensor_port_option_menu.grid(column=0, row=2, padx=3)
        
        
         
        self.actuator_port_variable = StringVar()
        self.actuator_port_variable.set("None")
        
        self.actuator_port_option_menu = OptionMenu(self.location, self.actuator_port_variable, self.get_ports)
        self.actuator_port_option_menu.grid(column=1, row=2, padx=3)
        
        self.apply_button = Button(
            self.location, 
            text="Apply", 
            command=self.apply_port, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT)
        self.apply_button.grid(column=0, row=3, columnspan=2, pady=2)
        
            
        self.refresh_button = Button(
            self.location,
            text="Refresh", 
            command=self.refresh_port, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT
        )
        self.refresh_button.grid(column=0, row=4, columnspan=2, pady=3)
        
    @property
    def get_ports(self):
        ports = []
        is_exist = False
        for port in port_list.comports():
            print("hey")
            is_exist = True
            ports.append(port.device)
            
        if is_exist == False:
            ports = ["None"]
            
        return ports
    
    def refresh_port(self):
        ports = self.get_ports
        for port in ports:
            print(port)
            
        if ports == ["None"]:
            self.sensor_port_variable.set("None")
            self.actuator_port_variable.set("None")
            
        menu1 = self.sensor_port_option_menu["menu"]
        menu2 = self.actuator_port_option_menu["menu"]
        menu1.delete(0, "end")
        menu2.delete(0, "end")
        
        for port in ports:
            menu1.add_command(label=port,
                              command=lambda value=port: self.sensor_port_variable.set(value))
            menu2.add_command(label=port,
                              command=lambda value=port: self.sensor_port_variable.set(value))
        
    
    def apply_port(self):
        sensor_port = self.sensor_port_variable.get()
        actuator_port = self.actuator_port_variable.get()
        
        if "COM" not in sensor_port and "COM" not in actuator_port:
            self.error_no_port()
        
        elif "COM" not in sensor_port: 
            # popup
            self.error_not_selected_Sensor_port()
        
        elif "COM" not in actuator_port: 
            # popup
            self.error_not_selected_Actuator_port()

        elif sensor_port == actuator_port:
            # popup
            self.error_same_port()
        
        else:
            com.publish_sensor_port(sensor_port)
            com.publish_actuator_port(actuator_port)
            com.publish_port_state(1)
            print("applied")
        
    
    def error_no_port(self):
        messagebox.showerror(
            title="Error",
            message="No port selected!"
        )
    
    def error_not_selected_Sensor_port(self):
        messagebox.showerror(
            title="Error",
            message="Sensor port not selected!"
        )
        
    def error_not_selected_Actuator_port(self):
        messagebox.showerror(
            title="Error",
            message="Actuator port not selected!"
        )
        
    def error_same_port(self):
        messagebox.showerror(
            title="Error",
            message="Sensor and actuator port cannot be the same!"
        )
        
    def push_actuator(self):
        pass
    
    def pull_actuator(self):
        pass
    
    def idle_actuator(self):
        pass
    
    def dummy(self):
        pass
        

        
        
        
        