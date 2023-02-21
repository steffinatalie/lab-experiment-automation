import threading
import csv
import time
import serial
import settings

state = ""
count = 0
ser = serial.Serial("COM4", 9800, timeout=1)
# check = serial.Serial("COM5", 9800, timeout=1)


"""
Experiment state : start, stop
Read state       : reading, notreading

"""

def time_keeper():
    configs = []
    with open(settings.FILE_TIME_CONFIG, 'r') as f:
        configs = f.readline()
        
    time_interval, read_duration, executions = [configs[i] for i in range(3)]
    
    # this should probably have it's own file.txt to command for readings
    
    

def ask_input():
    global state
    
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
        with open(settings.FILE_COMMAND, 'r') as f:
            state = f.read()
        print(state)
        time.sleep(2)
        count+=1
            
        if state == "endread":
            state = input(">>> ")
           
        if state == "read":  
            new_thread = threading.Thread(target=data_write)
            new_thread.start()

def data_write():
    global state, count
    
    count += 1
    file = open(f"input{count}.csv", 'w', newline='')
    write = csv.writer(file)

    while state == "read":
        line = ser.readline()
        
        try:
            num = int(line.decode())
        except:
            pass
        
        string = str(num)
        write.writerow([string])
        time.sleep(1)

    file.close()

th = threading.Thread(target=ask_input)

th.start()


