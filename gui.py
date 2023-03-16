from tkinter import *
import settings
import utils
from elements import LeftTopFrame, LeftMiddleFrame, LeftBottomFrame
from communicate_v2 import Communicate as com
import time
import threading
# from tkterminal import Terminal

root = Tk()
root.title("Experiment Control Station")

root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}") 
# root.configure(bg="black")

left_top_frame = Frame(
    root,
    # bg = "red",
    width=utils.width_prct(50),
    height=utils.height_prct(30),
)
left_top_frame.place(x=0, y=0)

left_middle_frame = Frame(
    root,
    width=utils.width_prct(50),
    height=utils.height_prct(30),
    # highlightbackground="grey",
    # highlightthickness=2
)
left_middle_frame.place(x=0, y=utils.height_prct(30))

left_bottom_frame = Frame(
    root,
    width=utils.width_prct(50),
    height=utils.height_prct(20),
    # background="white"
)
left_bottom_frame.place(x=0, y=utils.height_prct(60))

# terminal = Terminal(
#     root,
# )
# terminal.place(x=0, y=utils.height_prct(60))


right_frame = Frame(
    root,
    # bg="green",
    width=utils.width_prct(50),
    height=utils.height_prct(100)
)
right_frame.place(x=utils.width_prct(50), y=0)

#frames
ltf = LeftTopFrame(left_top_frame)
# lmf = LeftMiddleFrame(left_middle_frame)
# lbf = LeftBottomFrame(left_bottom_frame)


# def kill():
#     com.publish_experiment_state(settings.KILLED)
#     root.after(2500)
#     root.destroy()
    
# root.protocol('WM_DELETE_WINDOW', kill)

#run the window 
root.mainloop()

com.publish_experiment_state(settings.KILLED)
