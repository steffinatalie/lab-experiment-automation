import threading
import time
import serial
import settings
import utils
import datetime
import pandas as pd
from communicate_v2 import Communicate as com
import os

experiment_state = None
read_state = None
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

TODO:
- check excel file regarding None returned if conversion error occurs 
- when running new experiment without closing the gui first, empty the dataframe
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
    experiment_state = com.update_experiment_state()
    
    # if start button pressed
    if experiment_state == settings.START:
        # move to initial position
        move_forward()
        
        # stop the actuator
        idle()
        
        
        time_interval, read_duration, executions = [x for x in com.update_time_config()]
        
        # convert minutes to seconds
        time_interval *= settings.TIME_MULTIPLIER
        
        execution_counter = 0
        while execution_counter < executions and is_timekeeping == True:
            
            # wait for the time interval
            countdown(time_interval)
            
            # move the sensors to the reading position
            move_backward()
            
            # stop the actuator
            idle()
            
            # begin reading data from sensors
            read_state = settings.START
            # print("is reading")
            th = threading.Thread(target=data_write)
            th.start()
            
            # reading duration
            countdown(read_duration)
            
            # stop reading
            read_state = settings.STOP
            th.join()
            
            # go back to the initial position
            move_forward()
            
            # stop the actuator
            idle()
            
            
            # count the executions
            execution_counter+=1
            com.publish_count_executions(execution_counter)
            
        # stop time keeper and the experiment
        is_timekeeping = False
        com.publish_experiment_state(settings.STOP)
        
            

def experiment_state_check():
    global experiment_state, is_timekeeping, read_state

    while experiment_state != settings.KILLED:
        experiment_state = com.update_experiment_state()
        # time.sleep(0.5)

        
        if experiment_state == settings.STOP:
            idle()
            read_state = False
            is_timekeeping = False

        
        if experiment_state == settings.START and not is_timekeeping:
            
            is_timekeeping = True
            th = threading.Thread(target=time_keeper)
            th.start()
            
    is_timekeeping = False
            

def data_write():
    global read_state, count, ser_sensor
    
    # xyz
    # ser_sensor = serial.Serial("COM4", 9800, timeout=1)
    
    # path = utils.create_folder(settings.FOLDER_READINGS)
    folder_path = com.update_experiment_folder_path()
    
    
    
    # file naming and prevent override
    count += 1
    filename = f"{folder_path}\input{count}.xlsx"
    if os.path.isfile(filename) == True:
        count += 1
        filename = f"{folder_path}\input{count}.xlsx"
    
    print(f"\nIs writing to {filename}")
    
    c1 = ["Timestamp"]
    c2 = [f"Sensor{i}" for i in range(1,21)]
    c = c1+c2
    
    df = pd.DataFrame(columns=c)
    df.to_excel(filename, index=False)
    
    # print(df)
    

    while read_state == settings.START:
        # print("is reading\n")
        
        line = ser_sensor.readline()
        while(line.decode() == ''):
            line = ser_sensor.readline()
         
        decoded = line.decode()
        
        try:
            decoded_list = decoded.split(',')
        except:
            continue
        
        list = [utils.conversion(x) for x in decoded_list]
        timestamp = {"Timestamp": datetime.datetime.now()}
        data = {f"Sensor{index+1}": value for index, value in enumerate(list)}
        data.update(timestamp)
        datas = [data]
        
        ndf = pd.DataFrame(datas)
        df = pd.concat([df, ndf], axis=0)
        
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)

        
def move_forward():
    print("FORWARD")
    try:
        ser_actuator.write(bytes(settings.FORWARD, "utf-8"))
        countdown(settings.PUSH_DURATION)
    except:
        print("Serial communication not established")
    

def idle():
    print("IDLE")
    try:
        ser_actuator.write(bytes(settings.IDLE, "utf-8"))
        countdown(settings.IDLE_SEND_DURATION)
    except:
        print("Serial communication not established")

def move_backward():
    print("BACKWARD")
    try:
        ser_actuator.write(bytes(settings.BACKWARD, "utf-8"))
        countdown(settings.PULL_DURATION)
    except:
        print("Serial communication not established")


def manual_control_time_keeper():
    global is_timekeeping, manual_control_state, previous_manual_control_state
    
    # to check the change of control state
    # it will interrupt the current time countdown
    # so it can start another command
    
    
    if previous_manual_control_state != com.update_manual_control_state():
        is_timekeeping = False
        
    # if manual_control_state == settings.KILLED:
    #     is_timekeeping = False
    #     idle()

def manual_control_state_check():
    global manual_control_state, is_timekeeping
    
    th = threading.Thread(target=manual_control_time_keeper)
    th.start()
    
    # previous_manual_control_state = com.update_manual_control_state
    while manual_control_state != settings.KILLED:
        is_timekeeping = True
        manual_control_state = com.update_manual_control_state()
        time.sleep(0.5)
        
        if manual_control_state == settings.FORWARD:
            move_forward()
            
        elif manual_control_state == settings.IDLE:
            idle()
            
        elif manual_control_state == settings.BACKWARD:
            move_backward()
    
    is_timekeeping = False
    idle()
    
def port_assignment():
    global ser_sensor, ser_actuator
    
    sensor_port = com.update_sensor_port()
    actuator_port = com.update_actuator_port()
    
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
    


