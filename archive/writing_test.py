import numpy as np
import serial
import utils
import pandas as pd
import datetime

# Open serial port
ser = serial.Serial("COM4", 9600, timeout=1)

# Create ReadLine object
rl = utils.ReadLine(ser)

# Initialize variables
data = []
counter = 0

# file = open("data.txt", 'w', encoding="utf-8")

c1 = ["Timestamp"]
c2 = [f"Sensor{i}" for i in range(1,17)]
c = c1+c2

df = pd.DataFrame(columns=c)

# Read data from serial port
while counter < 1000:
    line = rl.readline()
    
    # Parse line of text

    # vals = line.decode('latin-1').split(',')
    # d = [float(v.strip()) for v in vals[1:]]
    vals = line.decode('latin-1')
    
    decoded_list = vals.split(',')
    
    list = [utils.conversion(x) for x in decoded_list]
    timestamp = {"Timestamp": datetime.datetime.now()}
    data = {f"Sensor{index+1}": value for index, value in enumerate(list)}
    data.update(timestamp)
    datas = [data]
    
    ndf = pd.DataFrame(datas)
    df = pd.concat([df, ndf], axis=0)
    


    # Append data to arrays
    # data.append(d)
    counter += 1
    # file.write(vals)
    
# file.close()
with pd.ExcelWriter("data.xlsx") as writer:
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    

# Convert arrays to NumPy arrays
# data = np.array(data)

# Save arrays to .npz file
# np.savez_compressed('data.npz', data=data)
