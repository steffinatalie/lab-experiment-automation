from tkinter import Button, Text, Label, messagebox, StringVar, OptionMenu, Radiobutton, IntVar, RIGHT, BOTH, filedialog
import tools.settings as settings
import tools.threads as threads
from tools.communicate_v2 import Communicate as com
import threading
import serial.tools.list_ports as port_list
import tools.utils as utils
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os



"""
MAYBE:
- should there be a feature to continue an experiment...

BUG:
- multiple logs, bug or not depends on your perspective
- manual buttons

TODO:
- create warn to remind the starting position
- change push pull duration
- start stop button affect com.manual_control_state
- create popup for manual auto radio button if serial not established
- give more details in the error popup : ports not applied
- ask for the starting position ??
- open the log together with the main window
- refactor the tests
- check displays callback
- disable log button when log already opened
- close the log when main window closed
- check whether port is flipped
- display count executions
- create warning before closing window during experiment (experiment must be stopped first, if not stopped window can't be closed)
- create warning if experiment stopped when sensors are still below the heater
- create pause and continue
- connect this to discord bot so it would call bang normen during emergency wkwkwwk
- save latest time config
"""


class RightBottom1Frame:
    def __init__(self, location):
        self.location = location
        
        self.default_path = utils.create_folder(settings.FOLDER_READINGS)
        
        self.title_label = Label(
            self.location,
            text="OPEN FILES",
            font='Helvetica 8 bold'
        ).pack(side='left')
        
        self.button = Button(self.location, text="Browse", command=self.browse_files)
        self.button.pack(side="left")

        self.label = Label(self.location, text="")
        self.label.pack(side="left")
        
    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir=self.default_path)
        if file_path:
            # self.label.config(text=file_path)
            self.open_file(file_path)
        
    def open_file(self, file_path):
        try:
            os.startfile(file_path)
        except AttributeError:
            try:
                os.system(f"open {file_path}")
            except:
                print("Unable to open file.")
        
        
        
        
        

class RightTopFrame:
    def __init__(self, location):
        self.location = location
        
        """
        
        dataframe initiation depends on:
        the amount of executions
        but give it a default
        
        """

        self.data = {'Execution': [0 for i in range(1, 21)],
         'Average distance': [0 for i in range(1, 21)]
         }  
        self.df = pd.DataFrame(self.data)
        
        self.fig = plt.figure(figsize=(7, 6), dpi=70)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.location)
        self.canvas.get_tk_widget().pack()
        
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot(self.df['Average distance'], self.df['Execution'])
        
        

        # self.figure = plt.Figure(figsize=(7, 6), dpi=70)
        # self.ax = self.figure.add_subplot(111)
        # self.line = FigureCanvasTkAgg(self.figure, self.location)
        # self.line.get_tk_widget().pack(side=RIGHT, fill=BOTH)
        # self.df = self.df[['Execution', 'Average distance']].groupby('Execution').sum()
        # self.df.plot(kind='line', legend=True, ax=self.ax, color='r', marker='o', fontsize=7)
        # self.ax.set_title('Data Graph')




class LeftTopFrame:
    def __init__(self, root, location, leftBottomFrame, rightTopFrame):
        self.root = root
        self.location = location
        self.leftBottomFrame = leftBottomFrame
        self.rightTopFrame = rightTopFrame
        
        
        
        
        # DISPLAY EXPERIMENT FOLDER NAME
        self.experiment_folder_variable = StringVar()
        # self.experiment_folder_variable.set("test")
        self.experiment_folder_label = Label(
            self.location,
            text="",
            textvariable=self.experiment_folder_variable,
            font='Helvetica 8 bold'
        )
        self.experiment_folder_label.grid(
            column=1, row=0, sticky='e'
        )
        
        
        
        
        # DISPLAY READING EXECUTIONS COUNT
        self.executions_count_variable = IntVar()
        self.executions_count_variable.set(0)
        
        self.executed_label = Label(
            self.location,
            text="Executed (n times)                        :"
        ).grid(columnspan=2, column=0, row=4, pady=20, padx=10, sticky='sw')
        
        self.executions_count_label = Label(
            self.location,
            text="",
            textvariable=self.executions_count_variable
        ).grid(columnspan=2, column=1, row=4)
        
        
        
        
        # DISPLAY MINUTES COUNTDOWN UNTIL THE NEXT EXECUTION
        # self.time_left_until_next_execution_variable = IntVar()
        # self.time_left_until_next_execution_variable.set(0)
        
        # self.countdown_next_execution_label = Label(
        #     self.location,
        #     text="Countdown next execution (m) :"
        # ).grid(columnspan=2, column=0, row=4, rowspan=2, pady=3, padx=10, sticky='sw')
        
        # self.time_left_until_next_execution_label = Label(
        #     self.location,
        #     text="",
        #     textvariable=self.time_left_until_next_execution_variable
        # ).grid(columnspan=2, column=1, row=4, rowspan=2, sticky='s')
        
        
        
        
        # DISPLAY ACTUATOR STATE
        self.actuator_state_variable = StringVar()
        self.actuator_state_variable.set("IDLE")
        
        self.actuator_state_label = Label(
            self.location,
            text="Actuator state :"
        ).grid(columnspan=2, column=0, row=6, pady=20, padx=10, sticky='nw')
        
        self.actuator_state_value_label = Label(
            self.location,
            text="",
            textvariable=self.actuator_state_variable
        ).grid(columnspan=2, column=0, row=6, pady=20, padx=100, sticky='w')
        
        
        
        
        # DISPLAY READING STATE
        self.read_state_variable = StringVar()
        self.read_state_variable.set("False")
        
        self.read_state_label = Label(
            self.location,
            text="Read state        :"
        ).grid(columnspan=2, column=0, row=6, rowspan=2, padx=10, sticky='sw')
        
        self.read_state_value_label = Label(
            self.location,
            text="",
            textvariable=self.read_state_variable
        ).grid(columnspan=2, column=0, row=6, rowspan=2, padx=100, sticky='sw')
        
        
        
        
        
        # LOG BUTTON
        self.experiment_log_button = Button(
            self.location,
            text="Experiment Log"
        )
        self.experiment_log_button.grid(columnspan=2, column=0, row=8, rowspan= 2, sticky='sw', padx=12, pady=5)
        self.experiment_log_button.bind("<Button-1>", self.experiment_log_window)
        
        
        
        
        # CHANGE MODE AUTO MANUAL
        self.mode_label = Label(
            self.location,
            text="Mode :                  ",
            font=("Helvetica", 10)
        )
        self.mode_label.grid(
            column=0, row=10, columnspan=2, sticky='se', pady=40
        )
        
        self.auto_manual_variable = IntVar()
        self.auto_manual_variable.set(settings.MODE_MANUAL)
        
        self.enable_manual_radiobutton = Radiobutton(
            self.location,
            text="Manual",
            variable=self.auto_manual_variable,
            value=settings.MODE_AUTO,
            indicator=0,
            width=settings.BUTTON_WIDTH,
            pady= 5
        )
        self.enable_manual_radiobutton.grid(
            column=1, row=10, sticky='se', pady=40
        )
        
        self.enable_auto_radiobutton = Radiobutton(
            self.location,
            text="Auto",
            variable=self.auto_manual_variable,
            value=settings.MODE_MANUAL,
            indicator=0,
            width=settings.BUTTON_WIDTH,
            pady= 5
        )
        self.enable_auto_radiobutton.grid(
            column=2, row=10, sticky='se', pady=40
        )
        
        self.enable_manual_radiobutton.bind("<ButtonRelease-1>", lambda event: self.auto_manual_enable())
        self.enable_auto_radiobutton.bind("<ButtonRelease-1>", lambda event: self.auto_manual_enable())
        
        
        
        
        # START BUTTON
        self.start_button = Button(
            self.location,
            text="Start",
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.start_button.grid(
            column=0, row=0
        )
        #bind
        self.start_button.bind("<Button-1>", self.start)
        
        
        
        
        # STOP BUTTON
        self.stop_button = Button(
            self.location,
            text="Stop",
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.stop_button.grid(
            column=0, row=2
        )
        self.stop_button.config(
            state="disabled"
        )
        # bind
        self.stop_button.bind("<Button-1>", self.stop)
        
        
        
        
        # PAUSE BUTTON
        self.pause_button = Button(
            self.location,
            text="Pause",
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
        )
        self.pause_button.grid(
            column=0, row=1
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
        
        # self.label_read_duration = Label(
        #     self.location,
        #     text="Read Duration (s)  "
        # )
        # self.label_read_duration.grid(
        #     column=1, row=2, sticky='e'
        # )
        
        # self.input_read_duration = Text(
        #     self.location,
        #     width=settings.INPUT_TEXT_WIDTH,
        #     height=settings.INPUT_TEXT_HEIGHT
        # )
        # self.input_read_duration.grid(
        #     column=2, row=2
        # )
        
        self.label_data_limit = Label(
            self.location,
            text="Data Limit (n)  "
        )
        self.label_data_limit.grid(
            column=1, row=2, sticky='e'
        )
        
        self.input_data_limit = Text(
            self.location,
            width=settings.INPUT_TEXT_WIDTH,
            height=settings.INPUT_TEXT_HEIGHT
        )
        self.input_data_limit.grid(
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
            print(f"[ignore] port error handling {com.port_state + 1}")
        
            time_config = [int(float(self.input_time_interval.get(1.0, "end-1c"))), 
                        # int(float(self.input_read_duration.get(1.0, "end-1c"))),
                        int(float(self.input_data_limit.get(1.0, "end-1c"))),
                        int(float(self.input_executions.get(1.0, "end-1c")))]
        
            com.publish_experiment_state(settings.START)
            com.publish_time_config(time_config)
            
            # ask folder name
            th = threading.Thread(target=self.experiment_prestart)
            th.start()
            
        
        except:
            # pop up
            
            th = threading.Thread(target=self.error_popup)
            th.start()
        
    def experiment_prestart(self):
        
        """edit this
        """
        utils.ask_for_text(self.root) 
        
        if com.experiment_folder_path != None:

                # display the folder name
                self.experiment_folder_variable.set(
                    com.experiment_folder_display
                )
                
                # run experiment
                threads.main()
                
                # run displays callback
                # th = threading.Thread(target= self.displays_callback())
                # th.start()
                
                self.start_button.config(
                    state="disabled"
                )
                
                self.stop_button.config(
                    state="normal"
                )
        
    def stop(self, event):

        com.publish_experiment_state(settings.KILLED)
        
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
        if com.actuator_port == None or com.sensor_port == None:
            msg = "Invalid ports \nand time configurations"
        messagebox.showerror(
            title="Error",
            message=msg
        )
        
    def auto_manual_enable(self):
        if self.auto_manual_variable.get() == settings.MODE_AUTO:
            com.publish_experiment_state(settings.KILLED)
            # kill manual thread
            com.publish_manual_control_state(settings.KILLED)
            
            # buttons
            self.start_button.config(state="normal")
            self.leftBottomFrame.push_actuator_button.config(state="disabled")
            self.leftBottomFrame.push_actuator_button.config(state="disabled")
            self.leftBottomFrame.pull_actuator_button.config(state="disabled")
            self.leftBottomFrame.idle_actuator_button.config(state="disabled")
            self.leftBottomFrame.start_read_button.config(state="disabled")
            self.leftBottomFrame.save_read_button.config(state="disabled")

        elif com.experiment_state != settings.KILLED:
            self.radiobutton_error_popup()
            return
        elif self.auto_manual_variable.get() == settings.MODE_MANUAL:
            com.publish_experiment_state(settings.START)
            com.publish_manual_control_state(settings.START)
            

            # buttons 
            self.start_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            self.leftBottomFrame.push_actuator_button.config(state="normal")
            self.leftBottomFrame.pull_actuator_button.config(state="normal")
            self.leftBottomFrame.idle_actuator_button.config(state="normal")
            self.leftBottomFrame.start_read_button.config(state="normal")
            self.leftBottomFrame.save_read_button.config(state="normal")
            
            # run manual thread
            threads.manual_control()
            
            # print("Manual mode")

            
    
    def radiobutton_error_popup(self):
        msg = "Experiment still running"
        messagebox.showerror(
            title="Error",
            message=msg
        )
        
    def experiment_log_window(self, event):
        # self.experiment_log_button.config(
        #         state="disabled"
        #     )
        try:
            utils.terminal()
        except:
            pass
        
        # self.experiment_log_button.config(
        #         state="normal"
        #     )
        
    def displays_callback(self):
        while com.experiment_state != settings.KILLED:
            self.executions_count_variable = com.count_executions
            # self.time_left_until_next_execution_variable = com.minutes_countdown
            self.actuator_state_variable = com.actuator_state
            self.read_state_variable = com.read_state
            
            # graph callback
            # self.rightTopFrame.
        
        
class LeftBottomFrame:
    def __init__(self, location):
        self.location = location
            
            
        self.manual_control_label = Label(
            self.location,
            text="MANUAL CONTROL",
            font='Helvetica 8 bold', 
            # background="lightgrey"
        )
        self.manual_control_label.grid(
            column=2, row = 0, columnspan=2, padx=70, pady=9
            )
        
        self.start_read_button = Button(
            self.location,
            text="Start Read",
            command=utils.dummy,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
            state="disabled"
        )
        self.start_read_button.grid(
            column=3, row=1, rowspan=2, sticky='nw'
        )
        
        self.save_read_button = Button(
            self.location,
            text="Save Data",
            command=utils.dummy,
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
            state="disabled"
        )
        self.save_read_button.grid(
            column=3, row=2, rowspan=2, sticky='nw', pady= 5
        )
        
        self.push_actuator_button = Button(
            self.location,
            text="Push", 
            command=self.push_actuator, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
            state="disabled"
        )
        self.push_actuator_button.grid(
            column=2, row=1, rowspan=2, padx=10, sticky='ne'
        )
        
        self.idle_actuator_button = Button(
            self.location,
            text="Idle", 
            command=self.idle_actuator, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
            state="disabled"
        )
        self.idle_actuator_button.grid(
            column=2, row=2, rowspan=2, padx=10, pady= 5, sticky='ne'
        )
        
        self.pull_actuator_button = Button(
            self.location,
            text="Pull", 
            command=self.pull_actuator, 
            width=settings.BUTTON_WIDTH,
            height=settings.BUTTON_HEIGHT,
            state="disabled"
        )
        self.pull_actuator_button.grid(
            column=2, row=3, rowspan=2, padx=10, sticky='ne'
        )
        
        
        
        self.select_port_label = Label(
            self.location, 
            text="SELECT PORT", 
            font='Helvetica 8 bold', 
            # background="lightgrey"
            )
        self.select_port_label.grid(
            column=0, row=0, columnspan=2, padx=40, pady=7
        )
        
        self.sensor_label = Label(
            self.location,
            text="Sensor:",
            # background="lightgrey"
        )
        self.sensor_label.grid(
            column=0, row=1
        )
        
        self.actuator_label = Label(
            self.location,
            text="Actuator:",
            # background="lightgrey"
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
        self.refresh_button.grid(column=0, row=4, columnspan=2, pady=5, sticky='n')
        
        # refresh the port option from the start
        self.refresh_port()
        
    @property
    def get_ports(self):
        ports = []
        is_exist = False
        for port in port_list.comports():
            is_exist = True
            ports.append(port.device)
            
        if is_exist == False:
            ports = ["None"]
            
        return ports
    
    def refresh_port(self):
        ports = self.get_ports
        print('\n')
        for port in ports:
            print(f"Detected port: {port}")
            
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
                              command=lambda value=port: self.actuator_port_variable.set(value))
            

        
    
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
            sensor_port = sensor_port.strip("(),'")
            actuator_port = actuator_port.strip("(),'")
            
            com.publish_sensor_port(sensor_port)
            com.publish_actuator_port(actuator_port)
            com.publish_port_state(1)
            
            # assign the ports
            threads.port_assignment()
            
            print("Ports applied")
        
    
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
        
        
        
    # NAVIGATIONS
    
    def push_actuator(self):
        # com.publish_manual_control_state(settings.FORWARD)
        com.publish_manual_control_state(settings.BACKWARD)
    
    def pull_actuator(self):
        # com.publish_manual_control_state(settings.BACKWARD)
        com.publish_manual_control_state(settings.FORWARD)
    
    def idle_actuator(self):
        com.publish_manual_control_state(settings.IDLE)

        

        
        
        
        