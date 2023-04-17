import serial
from communicate_v2 import Communicate as com

def test_serial():
    ser = serial.Serial(com.sensor_port, 9800, timeout=1)
    print("done")