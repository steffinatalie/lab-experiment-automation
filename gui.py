from tkinter import *
import settings
import utils
from elements import LeftTopFrame, LeftBottomFrame, RightTopFrame, RightBottom1Frame
from communicate_v2 import Communicate as com
# import time
# import threading
# from tkterminal import Terminal

root = Tk()
root.title("Experiment Control Station")
root.resizable(False, False)

root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}") 
# root.configure(bg="black")

left_top_frame = Frame(
    root,
    width=utils.width_prct(45),
    height=utils.height_prct(50),
    # background="lightgrey"
    
)
left_top_frame.place(x=0, y=0)

left_bottom_frame = Frame(
    root,
    width=utils.width_prct(45),
    height=utils.height_prct(50),

)
left_bottom_frame.place(relx=0, rely=1.0, anchor='sw')


right_top_frame = Frame(
    root,
    background="white",
    width=utils.width_prct(55),
    height=utils.height_prct(80)
)
right_top_frame.place(x=utils.width_prct(45), y=0)

right_bottom_1_frame = Frame(
    root,
    width=utils.width_prct(30),
    height=utils.height_prct(20)
)
right_bottom_1_frame.place(x=utils.width_prct(45), y=utils.height_prct(80))

# frames
lbf = LeftBottomFrame(left_bottom_frame)
ltf = LeftTopFrame(root, left_top_frame, lbf)
rtf = RightTopFrame(right_top_frame)
rb1f = RightBottom1Frame(right_bottom_1_frame)


# def kill():
#     com.publish_experiment_state(settings.KILLED)
#     root.after(2500)
#     root.destroy()
    
# root.protocol('WM_DELETE_WINDOW', kill)

#run the window 
root.mainloop()

com.publish_experiment_state(settings.KILLED)
