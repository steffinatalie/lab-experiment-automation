import settings
import os

def width_prct(percentage):
    return (settings.WINDOW_WIDTH / 100) * percentage

def height_prct(percentage):
    return (settings.WINDOW_HEIGHT / 100) * percentage
        
def create_path(folder):
    cwd = os.getcwd()
    dir = f"{cwd}\{folder}"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    return f"{dir}"
    
    
    