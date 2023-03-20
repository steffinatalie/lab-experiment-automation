import threading
import csv
import time
import serial
import settings
import utils
import datetime
import pandas as pd
from communicate_v2 import Communicate as com

experiment_state = None
read_state = None
count = 0
is_timekeeping = False

ser_sensor = None
ser_actuator = None

# ser_sensor = serial.Serial("COM4", 9800, timeout=1)
ser_actuator = serial.Serial("COM4", 9800, timeout=1)


"""
Experiment state : start, stop, killed, paused 
Read state       : reading, notreading

TODO:
- make it won't ovveride the previous files
- stop needs improvement
- read state should also be sent through serial to the other arduino
- handling if arduino not detected
- first thing when main is called is to check availability of arduino

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
            print("is reading")
            # th = threading.Thread(target=data_write)
            # th.start()
            
            # reading duration
            countdown(read_duration)
            
            # stop reading
            read_state = settings.STOP
            # th.join()
            
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
        time.sleep(0.5)

        
        if experiment_state == settings.STOP:
            idle()
            read_state = False
            is_timekeeping = False

        
        if experiment_state == settings.START and not is_timekeeping:
                    
            """
            halt gui until the sensors have arrived 
            
            """
            
            
            is_timekeeping = True
            th = threading.Thread(target=time_keeper)
            th.start()
            
    is_timekeeping = False
            

def data_write():
    global read_state, count
    
    ser_sensor = serial.Serial("COM4", 9800, timeout=1)
    
    path = utils.create_path(settings.FOLDER_READINGS)
    
    
    count += 1
    filename = f"{path}\input{count}.xlsx"
    
    c1 = ["Timestamp"]
    c2 = [f"Sensor{i}" for i in range(1,21)]
    c = c1+c2
    
    df = pd.DataFrame(columns=c)
    df.to_excel(filename, index=False)
    
    print(df)
    

    while read_state == settings.START:
        print("is reading\n")
        
        line = ser_sensor.readline()
        while(line.decode() == ''):
            line = ser_sensor.readline()
         
        decoded = line.decode()
        
        list = [float(x.strip()) for x in decoded.split(',')]
        timestamp = {"Timestamp": datetime.datetime.now()}
        data = {f"Sensor{index+1}": value for index, value in enumerate(list)}
        data.update(timestamp)
        datas = [data]
        
        ndf = pd.DataFrame(datas)
        df = pd.concat([df, ndf], axis=0)
        
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)

"""
tambahin while supaya bisa di stop midway
"""   
        
        
def move_forward():
    print("FORWARD")
    ser_actuator.write(bytes(settings.FORWARD, "utf-8"))
    countdown(settings.PUSH)
    

def idle():
    print("IDLE")
    ser_actuator.write(bytes(settings.IDLE, "utf-8"))
    countdown(2)

def move_backward():
    print("BACKWARD")
    ser_actuator.write(bytes(settings.BACKWARD, "utf-8"))
    countdown(settings.PULL)

# def actuator_check():
#     read = ser_actuator.readline()
#     line = read.decode()
#     print(str(line))
    
"""
create new settings.ACTUATOR LALALA

"""

# def actuator_state_check():
#     # while 
#     pass

def main():

    
    th = threading.Thread(target=experiment_state_check)
    th.start()
    


