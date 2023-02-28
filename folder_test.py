import os

def create_directory(name):
    cwd = os.getcwd()
    dir = f"{cwd}\{name}"
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
create_directory("test")

"""
check for reading and writing 
from files inside directories

"""
    