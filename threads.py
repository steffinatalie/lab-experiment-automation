import threading
import csv
import time
import serial
import settings

experiment_state = ""
read_state =""
count = 0
ser_sensor = serial.Serial("COM4", 9800, timeout=1)
# ser_actuator = serial.Serial("COM5", 9800, timeout=1)


"""
Experiment state : start, stop
Read state       : reading, notreading

TODO:
- try the time keeper
- 'stop' affects all the processes
- read state should also be sent through serial to the other arduino
- put the files in folders 'topics' 'readings'
- time_keeper thread
- change read_state for data_write()



"""

def time_keeper():
    configs = []
    with open(settings.FILE_TIME_CONFIG, 'r') as f:
        configs = f.readline()
        
    time_interval, read_duration, executions = [configs[i] for i in range(3)]
    
    # this should probably have it's own file.txt to command for readings
    
    
    

def experiment_state_check():
    global experiment_state
    
    # while state != "stop":
        
    #     """
    #         start       (from gui)
    #         read        (from serial: check)
    #         endread     (from serial: check)
    #         stop        (from gui)
            
    #     """
    #     print("\n")
    #     print("'start' to begin experiment")
    #     print("'read' to begin data writing")
    #     print("'endread' to stop data writing")
    #     print("'stop' to stop experiment")
        
    #     state = input(">>> ")
        
    #     if state == "endread":
    #         state = input(">>> ")
           
    #     if state == "read":  
    #         new_thread = threading.Thread(target=data_write)
    #         new_thread.start()
    
    """
    
    use count for the time being,
    later to be changed with kill pid from the gui
    
    """
    count = 0
    while count < 10:
        with open(settings.FILE_EXPERIMENT_STATE, 'r') as f:
            experiment_state = f.read()
        print(experiment_state)
        time.sleep(2)
        count+=1
            
        # if read_state == "endread":
        #     state = input(">>> ")
           
        # if read_state == "read":  
        #     new_thread = threading.Thread(target=data_write)
        #     new_thread.start()

def data_write():
    global read_state, count
    
    count += 1
    file = open(f"input{count}.csv", 'w', newline='')
    write = csv.writer(file)

    while read_state == "read":
        line = ser_sensor.readline()
        
        try:
            num = int(line.decode())
        except:
            pass
        
        string = str(num)
        write.writerow([string])
        time.sleep(1)

    file.close()

def main():

    th = threading.Thread(target=experiment_state_check)

    th.start()


