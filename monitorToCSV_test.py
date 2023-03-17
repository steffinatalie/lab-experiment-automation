import csv
import pandas as pd
import serial

"""- maybe try to print line.decode()
"""

# str = "100.70, 77.77"
ser = serial.Serial("COM6", 9800, timeout=1)
line = ser.readline()
while(line == ''):
    line = ser.readline()

f = float(line.decode())

# num = float(line.decode())
print(f)

# list = [item for item in str.split(',')]

# print(list)
# with open("test.csv", 'w') as file:
#     write = csv.writer(file, delimiter=',')
    
#     write.writerow(list)
    
# df = pd.read_csv("test.csv")

# df.to_excel("test.xlsx", index=False)
