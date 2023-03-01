import os

cwd = os.getcwd()

def create_directory(name):
    dir = f"{cwd}\{name}"
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
create_directory("test")

"""
check for reading and writing 
from files inside directories

"""

def write_read(name):
    with open(f"{cwd}\\test\{name}.txt", 'w') as f:
        f.write("test")
        
    with open(f"{cwd}\\test\{name}.txt", 'r') as f:
        print(f.readline())
    
write_read("test")