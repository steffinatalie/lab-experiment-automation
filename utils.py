import settings
import os
from communicate_v2 import Communicate as com

def width_prct(percentage):
    return (settings.WINDOW_WIDTH / 100) * percentage

def height_prct(percentage):
    return (settings.WINDOW_HEIGHT / 100) * percentage

def create_path(folder):
    # creates the string only
    cwd = os.getcwd()
    dir = f"{cwd}\{folder}"
    return dir
        
def create_folder(folder):
    # not only create the string
    # it creates the actual folder
    dir = create_path(folder)
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    return dir

def conversion(x):
    # remove spaces and convert to float
    try:
        return float(x.strip())
    except:
        return None 

def dummy():
    pass

# def kill():
#     com.publish_experiment_state(settings.KILLED)
    
    
    