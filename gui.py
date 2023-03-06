from tkinter import *
import settings
import utils
from elements import LeftTopFrame
from communicate_v2 import Communicate as com

root = Tk()
root.title("Experiment Control Station")

root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}") 
# root.configure(bg="black")

left_top_frame = Frame(
    root,
    # bg = "red",
    width=utils.width_prct(50),
    height=utils.height_prct(50)
)
left_top_frame.place(x=0, y=0)

right_frame = Frame(
    root,
    # bg="green",
    width=utils.width_prct(50),
    height=utils.height_prct(100)
)
right_frame.place(x=utils.width_prct(50), y=0)

#frames
ltf = LeftTopFrame(root, left_top_frame)

#run the window 
root.mainloop()

com.publish_experiment_state(settings.KILLED)
