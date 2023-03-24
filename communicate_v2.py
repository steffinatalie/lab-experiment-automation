# for testing, don't delete
import settings

class Communicate:
    sensor_port = None
    actuator_port = None
    port_state = None # 1 or None for error handling
    
    experiment_folder_display = None
    experiment_state = None # change to None
    time_config = []
    count_executions = None
    
    
    manual_control_state = None
    experiment_folder_path = None
    
    
    
    # PUBLISHES
    
    @staticmethod
    def publish_experiment_folder_display(folder):
        Communicate.experiment_folder_display = f"Dir: {folder}"
    
    @staticmethod
    def publish_experiment_folder_path(path):
        Communicate.experiment_folder_path = path
    
    @staticmethod
    def publish_manual_control_state(state):
        Communicate.manual_control_state = state
    
    @staticmethod
    def publish_port_state(oneOrNone):
        Communicate.port_state = oneOrNone
    
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
    def update_experiment_folder_display():
        return Communicate.experiment_folder_display
    
    @staticmethod
    def update_experiment_folder_path():
        return Communicate.experiment_folder_path
    
    @staticmethod
    def update_manual_control_state():
        return Communicate.manual_control_state
    
    @staticmethod
    def update_port_state():
        return Communicate.port_state
    
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

