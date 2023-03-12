import serial
import serial.tools.list_ports
import settings
from communicate_v2 import Communicate as com

def check():
    ports = list(serial.tools.list_ports.comports())
    
    for p in ports:
        print(p)

def main():

    try:
        ser_sensor = serial.Serial("COM4", 9800, timeout=1)
        ser_actuator = serial.Serial("COM5", 9800, timeout=1)
        
        com.publish_arduino_state(settings.DETECTED)
        
        
    except:
        com.publish_arduino_state(settings.NOTDETECTED)
        
        
check()