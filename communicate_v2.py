import settings

class Communicate:
    experiment_state = None
    time_config = []
    count_executions = None
    arduino_state = None
    
    # PUBLISHES
    
    @staticmethod
    def publish_arduino_state(state):
        Communicate.arduino_state = state
    
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
    def update_arduino_state():
        return Communicate.arduino_state
    
    @staticmethod
    def update_experiment_state():
        return Communicate.experiment_state
    
    @staticmethod
    def update_time_config():
        return Communicate.time_config
    
    @staticmethod
    def update_count_executions():
        return Communicate.count_executions

