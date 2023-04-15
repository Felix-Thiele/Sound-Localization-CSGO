import pyaudio
import pyaudiowpatch
import numpy as np
from dataclasses import dataclass

import locator


## These two functions were used to record wav files of steps.
#calibrate_mouse()
#record_samples(GEN_FILENAME)

@dataclass
class Calibration:
    MIN_VOL = 200  # volume threshhold at which recording of a step starts.
    START_LISTENING_AGAIN = 2000 # time after which start listening for new steps after an old step.

    SCREEN_WIDTH = 3700
    SCREEN_HEIGHT = 1900
    SCREEN_LEFT = -200
    SCREEN_TOP = -150

    ANGLE_RANGE = 100 # range of angles that can be seen on screen, if out of range just shows step at the edge.

cal = Calibration
locator.locator(cal)