import threading
import time
import serial
import tools.settings as settings
import tools.utils as utils
import datetime
import pandas as pd
from tools.communicate_v2 import Communicate as com
import os
import numpy as np


experiment_state = None
read_state = False
count = 0
is_timekeeping = False

ser_sensor = None
ser_actuator = None

manual_control_state = None
previous_manual_control_state = None

# ser_sensor = serial.Serial("COM6", 9800, timeout=1)
# ser_actuator = serial.Serial("COM4", 9800, timeout=1)

"""
Experiment state : start, stop, killed, paused (maybe)
Read state       : reading, not reading

BUG:
- auto to manual

TODO:
- begin by start reading and then move
- change all the variable = com.variable to just use com.variable
- time interval - push pull idle duration
- create the file during the wait time
- send average distance value to gui
- check first file written
- try stop the reading halfway
- read based on data limit
- check excel file regarding None returned if conversion error occurs 
- manual reading
- modifiy all the prints [problem: non stop IDLE at log]

"""

def countdown(n):
    global is_timekeeping
    
    for i in range(n):
        if is_timekeeping == False:
            break
        print(n-i)
        time.sleep(0.99)
    
        

def time_keeper():
    global experiment_state, is_timekeeping, read_state
    
    # updating experiment state
    experiment_state = com.experiment_state
    
    # if start button pressed
    if experiment_state == settings.START:
        # move to initial position
        # move_forward()
        # move_backward()

        
        # stop the actuator
        # idle()
        
        
        # time_interval, read_duration, executions = [x for x in com.time_config]
        time_interval, data_limit, executions = [x for x in com.time_config]
        
        # convert minutes to seconds
        time_interval *= settings.TIME_MULTIPLIER
        
        execution_counter = 0
        while execution_counter < executions and is_timekeeping == True:
            
            # wait for the time interval
            countdown(time_interval)
            if experiment_state != settings.KILLED:
            
            # move the sensors to the reading position
            # move_backward()
                move_forward(settings.PUSH_DURATION)
            
            # stop the actuator
                idle(1)
            
            # begin reading data from sensors
            # read_state = True
            # print("is reading")
            # th = threading.Thread(target=data_write)
            # th.start()
            
                data_write(data_limit)
                
            # reading duration
            # countdown(read_duration)
            # while(read_state != False):
            #     read_state = com.read_state
            
            # stop reading
            # read_state = False
            # th.join()
            
            # go back to the initial position
            # move_forward()
                move_backward(settings.PULL_DURATION)
            
            # stop the actuator
                idle(1)
            
            
            # count the executions
                execution_counter+=1
                com.publish_count_executions(execution_counter)
            
        # stop time keeper and the experiment
        is_timekeeping = False
        com.publish_experiment_state(settings.KILLED)
        
            

def experiment_state_check():
    global experiment_state, is_timekeeping, read_state, count

    experiment_state = com.experiment_state

    while experiment_state != settings.KILLED:
        experiment_state = com.experiment_state
        # time.sleep(0.5)

        
        if experiment_state == settings.STOP:
            idle(1)
            read_state = False
            is_timekeeping = False

        
        if experiment_state == settings.START and not is_timekeeping:
            read_state = True
            count = 0
            is_timekeeping = True
            th = threading.Thread(target=time_keeper)
            th.start()
            
    print("is killed")
    idle(1)
    is_timekeeping = False
    read_state = False
            

def data_write(data_limit):
    global read_state, count, ser_sensor

    if experiment_state == settings.KILLED:
        return
    
    
    folder_path = com.experiment_folder_path
    
    # file naming and prevent override
    count += 1
    filename = f"{folder_path}\input{count}.xlsx"
    if os.path.isfile(filename) == True:
        count += 1
        filename = f"{folder_path}\input{count}.xlsx"
    
    print(f"\nIs writing to {filename}\n")

    c1 = ["Timestamp"]
    c2 = [f"Sensor{i}" for i in range(1,17)]
    c = c1+c2

    df = pd.DataFrame(columns=c)
   
    counter = 0

    # Create ReadLine object
    rl = utils.ReadLine(ser_sensor)

   # Read data from serial port
    while counter < data_limit and read_state == True:
        line = rl.readline()
        
        # Parse line of text

        # vals = line.decode('latin-1').split(',')
        # d = [float(v.strip()) for v in vals[1:]]
        vals = line.decode('latin-1')
        
        decoded_list = vals.split(',')
        
        list = [utils.conversion(x) for x in decoded_list]
        timestamp = {"Timestamp": datetime.datetime.now()}
        data = {f"Sensor{index+1}": value for index, value in enumerate(list)}
        data.update(timestamp)
        datas = [data]
        
        ndf = pd.DataFrame(datas)
        df = pd.concat([df, ndf], axis=0)

        counter += 1

    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    
    
    
        
    

        
def move_forward(duration):
    if com.experiment_state == settings.KILLED:
        return
    
    print("FORWARD")
    try:
        ser_actuator.write(bytes(settings.FORWARD, "utf-8"))
        countdown(duration)
    except:
        print("Serial communication not established")
    

def idle(duration):
    print("IDLE")
    try:
        ser_actuator.write(bytes(settings.IDLE, "utf-8"))
        # countdown(settings.IDLE_SEND_DURATION)
    except:
        print("Serial communication not established")
    

def move_backward(duration):
    if com.experiment_state == settings.KILLED:
        return
    
    print("BACKWARD")
    try:
        ser_actuator.write(bytes(settings.BACKWARD, "utf-8"))
        countdown(duration)
    except:
        print("Serial communication not established")


def manual_control_time_keeper():
    global is_timekeeping, manual_control_state, previous_manual_control_state
    
    # to check the change of control state
    # it will interrupt the current time countdown
    # so it can start another command
    
    while manual_control_state != settings.KILLED:
        if manual_control_state != com.manual_control_state:
            is_timekeeping = False
            manual_control_state = com.manual_control_state
        
    # if manual_control_state == settings.KILLED:
    #     is_timekeeping = False
    #     idle()

def manual_control_state_check():
    global manual_control_state, is_timekeeping, previous_manual_control_state
    
    th = threading.Thread(target=manual_control_time_keeper)
    th.start()
    
    manual_control_state = com.manual_control_state
    while com.manual_control_state != settings.KILLED:
        manual_control_state = com.manual_control_state
        time.sleep(0.5)
        
        if manual_control_state == settings.FORWARD:
            is_timekeeping = True
            move_forward(2)
            
        if manual_control_state == settings.IDLE:
            is_timekeeping = True
            idle(1)
            
        if manual_control_state == settings.BACKWARD:
            is_timekeeping = True
            move_backward(2)
    
    is_timekeeping = False
    idle(1)
    print("is killed")
    
    return
    
def port_assignment():
    global ser_sensor, ser_actuator
    
    sensor_port = com.sensor_port
    actuator_port = com.actuator_port
    
    ser_sensor = serial.Serial(sensor_port, 9800, timeout=1)
    ser_actuator = serial.Serial(actuator_port, 9800, timeout=1)
    
    print(f"Sensor port: {sensor_port}\n")
    print(f"Actuator port: {actuator_port}\n")
    

def manual_control():
    
    th = threading.Thread(target=manual_control_state_check)
    th.start()
    
    print("MANUAL MODE")
    

def main():
    th = threading.Thread(target=experiment_state_check)
    th.start()
    


