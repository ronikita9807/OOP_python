from tkinter import *
import time
import random

import forconst
import bankbranch
import externalworld
import interface

if __name__ == "__main__":
    external_world_initialization = externalworld.ExternalWorld()
    external_world_initialization.interface.master.mainloop()