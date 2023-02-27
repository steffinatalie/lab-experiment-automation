from tkinter import *
import settings
import utils
from elements import LeftFrame

root = Tk()
root.title("Experiment Control Station")

root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}") 
# root.configure(bg="black")

left_frame = Frame(
    root,
    # bg = "red",
    width=utils.width_prct(50),
    height=utils.height_prct(100)
)
left_frame.place(x=0, y=0)

right_frame = Frame(
    root,
    # bg="green",
    width=utils.width_prct(50),
    height=utils.height_prct(100)
)
right_frame.place(x=utils.width_prct(50), y=0)

#frames
lf = LeftFrame(left_frame)

#run the window 
root.mainloop()

# print("I'm dead")
utils.kill()