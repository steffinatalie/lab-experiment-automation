def time_keeper():
    print("begin time keeping")
    # t = threading.Thread(target=actuator_check)
    # t.start()
    global experiment_state, is_timekeeping, read_state
    
    # print(f"Experiment state: {experiment_state}")
    experiment_state = com.update_experiment_state()
    
    if experiment_state == settings.START:
        time_interval, read_duration, executions = [x for x in com.update_time_config()]
        
    
            
        time_interval *= 3 #later to be changed to 60
        n = 0
        while n < executions and is_timekeeping == True:
            read_state = settings.START
            countdown(time_interval)

            """tell the actuator to move forward and wait untill it arrives"""
            # move_forward()
            
            """actuator idle"""
            # idle()
            
            countdown(time_interval)
            
            th = threading.Thread(target=data_write)
            th.start()
            
            countdown(read_duration)
            read_state = settings.STOP
            th.join()
            
            """tell the actuator to go back and wait untill it arrives"""
            # move_backward()
            
            """actuator idle"""
            # idle()
            
            n+=1
            print(f"n : {n}")
            

            com.publish_count_executions(n)
            
    is_timekeeping = False
    com.publish_experiment_state(settings.STOP)