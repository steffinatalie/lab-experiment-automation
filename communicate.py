import settings
import utils

class PublishToGUI:
    @staticmethod
    def experiment_count(n):
        n = str(n)
        path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_COUNT_EXPERIMENT)
        with open(path, 'w') as f:
            f.write(n)
            f.close
            
class GUIUpdate:
    @staticmethod
    def experiment_count():
        path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_COUNT_EXPERIMENT)
        with open(path, 'r') as f:
            return f.read()
        
class PublishToThreads:
    @staticmethod
    def experiment_state(state):
        state = str(state)
        path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_EXPERIMENT_STATE)
        with open(path, 'w') as f:
            f.write(state)
            f.close
            
    # @staticmethod
    # def read_state(state):
    #     state = str(state)
    #     path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_READ_STATE)
    #     with open(path, 'w') as f:
    #         f.write(state)
    #         f.close
            
    @staticmethod
    def time_config(time_interval, read_duration, executions):
        state = str(state)
        path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_READ_STATE)
        with open(path, 'w') as f:
            f.write(time_interval)
            f.write(read_duration)
            f.write(executions)
            f.close
            
class ThreadsUpdate:
    @staticmethod
    def experiment_state():
        path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_EXPERIMENT_STATE)
        with open(path, 'r') as f:
            return f.read()
       
    # @staticmethod
    # def read_state():
    #     path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_READ_STATE)
    #     with open(path, 'r') as f:
    #         return f.readline() 
    
    @staticmethod
    def time_config():
        path = utils.create_path(settings.FOLDER_TOPICS, settings.FILE_TIME_CONFIG)
        with open(path, 'r') as f:
            time_conf = [f.readline() for _ in range(3)]
            return time_conf
        
# PublishToGUI.experiment_count(7)