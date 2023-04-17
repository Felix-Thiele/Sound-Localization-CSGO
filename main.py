from dataclasses import dataclass
import overlay
import locator
from audio_tools import record_samples, calibrate_mouse

## These two functions were used to record wav files of steps.
#calibrate_mouse()
#record_samples()

@dataclass
class Calibration:
    MIN_VOL = 200  # volume threshhold at which recording of a step starts.
    START_LISTENING_AGAIN = 2000 # time after which start listening for new steps after an old step.
    STEP_SHOW_TIME = 2000

    SCREEN_WIDTH = 3800
    SCREEN_LEFT = 10
    SCREEN_HEIGHT = 500
    SCREEN_TOP = 1500

    ANGLE_RANGE = 90 # range of angles that can be seen on screen, if out of range just shows step at the edge.

cal = Calibration
overlay.calibrate(cal)
overlay.overlay(cal)