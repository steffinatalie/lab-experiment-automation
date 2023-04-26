import settings
import os
from communicate_v2 import Communicate as com
import pandas as pd 
import numpy as np

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
    
def calc_avg(data, start_col, end_col):
    return data.iloc[:, start_col:end_col].mean().mean()

def dummy():
    pass

# def kill():
#     com.publish_experiment_state(settings.KILLED)

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s
    
    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)
    

# class ReadLine:
#     def __init__(self, s):
#         self.buf = bytearray()
#         self.s = s
    
#     def readline(self):
#         i = self.buf.find(b"\n")
#         if i >= 0:
#             r = self.buf[:i+1]
#             self.buf = self.buf[i+1:]
#             return r
#         while True:
#             i = max(1, min(2048, self.s.in_waiting))
#             data = bytearray(i)
#             n = self.s.readinto(data)
#             self.buf.extend(data[:n])
#             i = self.buf.find(b"\n")
#             if i >= 0:
#                 r = self.buf[:i+1]
#                 self.buf = self.buf[i+1:]
#                 return r


    
    