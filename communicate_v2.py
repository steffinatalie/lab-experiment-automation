# for testing, don't delete
import settings

class Communicate:
    
    # KZG
    sensor_port = settings.DEFAULT_SENSOR_PORT # default: None, testing: settings.DEFAULT_SENSOR_PORT
    actuator_port = settings.DEFAULT_ACTUATOR_PORT # default: None, testing: settings.DEFAULT_ACTUATOR_PORT
    port_state = 1 # default: None, values: (None, 1), testing: 1
    

    experiment_state = settings.START # default: None, testing: settings.START
    experiment_folder_display = None
    time_config = []
    
    # for displays in GUI
    count_executions = None
    minutes_countdown = None
    actuator_state = None
    read_state = None
    
    
    manual_control_state = None
    experiment_folder_path = None
    
    
    
    # PUBLISHES
    
    @staticmethod
    def publish_read_state(state):
        Communicate.read_state = state
    
    @staticmethod
    def publish_actuator_state(state):
        Communicate.actuator_state = state
    
    @staticmethod
    def publish_minutes_countdown(m):
        Communicate.minutes_countdown = m
    
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
    
    """
    wait probably all these should be @property instead
    
    """
    
    @staticmethod
    def update_read_state():
        return Communicate.read_state
    
    @staticmethod
    def update_actuator_state():
        return Communicate.actuator_state
    
    @staticmethod
    def update_minutes_countdown():
        return Communicate.minutes_countdown
    
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

