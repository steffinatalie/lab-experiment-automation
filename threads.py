import threading
import csv
import time
import serial
import settings

experiment_state = ""
read_state =""
count = 0
is_timekeeping = False
# ser_sensor = serial.Serial("COM4", 9800, timeout=1)
# ser_actuator = serial.Serial("COM5", 9800, timeout=1)


"""
Experiment state : start, stop, killed
Read state       : reading, notreading

TODO:
- try the time keeper
- 'stop' affects all the processes
- read state should also be sent through serial to the other arduino
- put the files in folders 'topics' 'readings'
- time_keeper thread
- change read_state for data_write()
- handling if arduino not detected
- handling for time keeper if killed (maybe it indeed needs to be killed)



"""

def countdown(n):
    global is_timekeeping
    
    for i in range(n):
        if is_timekeeping == False:
            break
        print(n-i)
        time.sleep(0.99)

def time_keeper():
    global experiment_state, is_timekeeping #read_state
    
    if experiment_state == "start":
        with open(settings.FILE_TIME_CONFIG, 'r') as f:   
            time_interval, read_duration, executions = [int(float(f.readline())) for _ in range(3)]
            # print(time_interval)
            # print(read_duration)
            # print(executions)
            
        time_interval *= 5 #later to be changed to 60
        is_timekeeping = True
        n = 0
        while n < executions and is_timekeeping == True:
            countdown(time_interval)
            print("reading")
            # read_state = "reading"
            
            countdown(read_duration)
            print("notreading")
            # read_state = "notreading"
            
            n+=1
            
    is_timekeeping = False
        

def experiment_state_check():
    global experiment_state, is_timekeeping
    
    """
    
    use count for the time being,
    later to be changed with kill pid from the gui
    
    """
    while experiment_state != "killed":
        with open(settings.FILE_EXPERIMENT_STATE, 'r') as f:
            experiment_state = f.read()
        # print(experiment_state)
        time.sleep(0.5)

        
        if experiment_state == "stop":
            is_timekeeping = False
        
        if experiment_state == "start" and not is_timekeeping:
            th = threading.Thread(target=time_keeper)
            th.start()
            

# def data_write():
#     global read_state, count
    
#     count += 1
#     file = open(f"input{count}.csv", 'w', newline='')
#     write = csv.writer(file)

#     while read_state == "read":
#         line = ser_sensor.readline()
        
#         try:
#             num = int(line.decode())
#         except:
#             pass
        
#         string = str(num)
#         write.writerow([string])
#         time.sleep(1)

#     file.close()

def main():
    th = threading.Thread(target=experiment_state_check)
    th.start()
    


