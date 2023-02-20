from tkinter import *
import settings

root = Tk()
root.title("Experiment Control Station")

# ganti fullscreen aja langsung
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}") 
root.configure(bg="black")

#run the window 
root.mainloop()