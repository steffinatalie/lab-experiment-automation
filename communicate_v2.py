class Communicate:
    experiment_state = None
    time_config = []
    count_executions = None
    arduino_state = None
    sensor_port = None
    actuator_port = None
    
    # PUBLISHES
    
    @staticmethod
    def publish_sensor_port(port):
        Communicate.sensor_port = port
        
    @staticmethod
    def publish_actuator_port(port):
        Communicate.actuator_port = port
    
    @staticmethod
    def publish_experiment_state(state):
        Communicate.experiment_state = state
        
    @staticmethod
    def publish_time_config(config):
        Communicate.time_config = config
        
    @staticmethod
    def publish_count_executions(count):
        Communicate.count_executions = count
        
        
        
    # UPDATES
    
    @staticmethod
    def update_sensor_port():
        return Communicate.sensor_port
    
    @staticmethod
    def update_actuator_port():
        return Communicate.actuator_port
    
    @staticmethod
    def update_experiment_state():
        return Communicate.experiment_state
    
    @staticmethod
    def update_time_config():
        return Communicate.time_config
    
    @staticmethod
    def update_count_executions():
        return Communicate.count_executions

