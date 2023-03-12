import threading
import csv
import time
import serial
import settings
import utils
from communicate_v2 import Communicate as com

experiment_state = None
read_state = None
count = 0
is_timekeeping = False

ser_sensor = None
ser_actuator = None


"""
Experiment state : start, stop, killed, paused 
Read state       : reading, notreading

TODO:
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
    
    # print(f"Experiment state: {experiment_state}")
    experiment_state = com.update_experiment_state()
    
    if experiment_state == settings.START:
        time_interval, read_duration, executions = [x for x in com.update_time_config()]
        
    
            
        time_interval *= 2 #later to be changed to 60
        n = 0
        while n < executions and is_timekeeping == True:
            read_state = settings.START
            countdown(time_interval)
            
            th = threading.Thread(target=data_write)
            th.start()
            
            countdown(read_duration)
            read_state = settings.STOP
            th.join()
            
            n+=1
            print(f"n : {n}")
            

            com.publish_count_executions(n)
            
    is_timekeeping = False
    com.publish_experiment_state(settings.STOP)
        

def experiment_state_check():
    global experiment_state, is_timekeeping, read_state

    while experiment_state != settings.KILLED:
        experiment_state = com.update_experiment_state()
        time.sleep(0.5)

        
        if experiment_state == settings.STOP:
            read_state = False
            is_timekeeping = False

        
        if experiment_state == settings.START and not is_timekeeping:
            is_timekeeping = True
            th = threading.Thread(target=time_keeper)
            th.start()
            
    is_timekeeping = False
            

def data_write():
    global read_state, count, ser_sensor, ser_actuator
    
    path = utils.create_path(settings.FOLDER_READINGS)
    
    
    # check the execution of these
    count += 1
    file = open(f"{path}\input{count}.csv", 'w', newline='')
    write = csv.writer(file)

    while read_state == settings.START:
        print("is reading\n")
        line = ser_sensor.readline()
        
        try:
            num = int(line.decode())
        except:
            pass
        
        string = str(num)
        write.writerow([string])
        time.sleep(1)

    file.close()
    
def move_forward():
    global ser_actuator
    
    # ser_actuator.write(bytes(settings.START, "utf-8"))
    time.sleep(0.05)
    

def idle():
    global ser_actuator
    
    # ser_actuator.write(bytes(settings.KILLED, "utf-8"))
    time.sleep(0.05)

def move_backward():
    global ser_actuator
    
    # ser_actuator.write(bytes(settings.STOP, "utf-8"))
    time.sleep(0.05)
    
"""
create new settings.ACTUATOR LALALA

"""

def actuator_state_check():
    # while 
    pass

def main():
    global ser_sensor, ser_actuator
    
    ser_sensor = serial.Serial("COM4", 9800, timeout=1)
    ser_actuator = serial.Serial("COM5", 9800, timeout=1)
    
    th = threading.Thread(target=experiment_state_check)
    th.start()
    


