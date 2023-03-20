import pandas as pd
import serial

"""- throw the empty values
"""

ser = serial.Serial("COM4", 9800, timeout=1)
line = ser.readline()

filename = "test.xlsx"

c1 = ["Timestamp"]
c2 = [f"Sensor{i}" for i in range(1,21)]
c = c1+c2
print(c)

df = pd.DataFrame(columns=c)
print(df)

df.to_excel(filename, index=False)

counter = 0
while(counter < 7):
    ##########################
    
    
    
    
    
    while(line.decode() == ''):
        line = ser.readline()
        
    decoded = line.decode()
        
    list = [float(x.strip()) for x in decoded.split(',')]

    print(list)

    data = [{f"Sensor{index+1}": value for index, value in enumerate(list)}]

    print(data)

    ndf = pd.DataFrame(data)
    df = pd.concat([df, ndf], axis=0)
    # new_data = pd.DataFrame(data)

    print(df)
    
    
    
    
    
    
    ##########################
    counter+=1



with pd.ExcelWriter(filename) as writer:
    df.to_excel(writer, sheet_name="Sheet1", index=False)
