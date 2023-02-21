import serial
import time

ser = serial.Serial(port="COM4", baudrate=9800, timeout=1)

def send(x):
    ser.write(bytes(x, "utf-8"))
    time.sleep(0.05)
    
def receive():
    data = ser.readline()
    print(data)
    
while True:
    send(input("r or n: "))
    receive()
    