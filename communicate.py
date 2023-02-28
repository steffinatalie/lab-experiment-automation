import settings

class TellGUI:
    def experiment_count(n):
        with open(settings.FILE_COUNT_EXPERIMENT, 'w') as f:
            f.write(n)
        
class GUIUpdate:
    def experiment_count():
        with open(settings.FILE_COUNT_EXPERIMENT, 'r') as f:
            return f.readline()
