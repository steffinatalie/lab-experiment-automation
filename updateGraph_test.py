import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Create a Pandas DataFrame
df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

# Create a Tkinter window
root = tk.Tk()
root.title('My Plot')

# Create a Matplotlib figure and canvas
fig = plt.figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a Matplotlib line plot of the DataFrame
ax = fig.add_subplot(111)
line, = ax.plot(df['x'], df['y'])

# Define a function to update the plot
def update_plot():
    # Modify the DataFrame
    df.loc[2, 'y'] = 7
    
    # Update the plot data
    line.set_data(df['x'], df['y'])
    
    # Redraw the plot
    canvas.draw()

# Create a button to update the plot
button = tk.Button(root, text='Update Plot', command=update_plot)
button.pack()

# Start the Tkinter event loop
root.mainloop()
