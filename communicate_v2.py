import settings

class Communicate:
    experiment_state = None
    time_config = []
    count_executions = None
    
    @staticmethod
    def publish_experiment_state(state):
        Communicate.experiment_state = state
        
    @staticmethod
    def publish_time_config(config):
        Communicate.time_config = config
        
    @staticmethod
    def publish_count_executions(count):
        Communicate.count_executions = count
    
    @staticmethod
    def update_experiment_state():
        return Communicate.experiment_state
    
    @staticmethod
    def update_time_config():
        return Communicate.time_config
    
    @staticmethod
    def update_count_executions():
        return Communicate.count_executions

