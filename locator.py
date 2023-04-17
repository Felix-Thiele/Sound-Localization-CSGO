import audio_tools
from audio_tools import *
import numpy as np
from sklearn.linear_model import LinearRegression

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal
import overlay

"""
Here we first train a regression model to predict the directions of incoming sounds.
locator() is a listener that listens for steps, and shows an overlay with the predicted directions
"""
class LocatorThread(QtCore.QThread):
    show_angle_trigger = pyqtSignal(float)
    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.window = window

    def run(self):
        GEN_FILENAME = 'samples/output'
        vec1 = []
        deg = []

        for j in range(200):
            # comparing
            audio_signals = wav_to_np(GEN_FILENAME + str(j + 1) + ".wav")

            a = np.copy(audio_signals[0]).reshape(-1)[3600:4000]
            b = np.copy(audio_signals[1]).reshape(-1)[3600:4000]

            vec1.append((np.mean(np.abs(b)) - np.mean(np.abs(a))) / (np.mean(np.abs(b)) + np.mean(np.abs(a))))

            # degrees
            with open('samples/output.txt') as f:
                lines = f.readlines()
                deg.append(float(lines[j].split(':')[-1]))

        deg = (np.array(deg) * np.pi / 180).reshape(-1, 1)
        vec1 = np.array(vec1).reshape(-1, 1)

        reg = LinearRegression().fit(vec1, deg)


        # Record sounds
        FORMAT = pyaudio.paInt16
        p = pyaudiowpatch.PyAudio()
        try:
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            print("Looks like WASAPI is not available on the system. Exiting...")
            exit()

        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else:
                print('Loopback not found')

        CHANNELS = default_speakers["maxInputChannels"]
        RATE = int(default_speakers["defaultSampleRate"])
        FRAMES_PER_BUFFER = self.window.cal.FRAMES_PER_BUFFER#pyaudio.get_sample_size(FORMAT)

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        frames_per_buffer=FRAMES_PER_BUFFER,
                        input=True,
                        input_device_index=default_speakers["index"]
                        )

        # Listens for sounds above MIN_VOL and then records the next 400 sound inputs. These are the used to predict a direction
        # which is then shown in the overlay.

        heard_step = False
        hear_ago = 0

        while True:
            data = stream.read(FRAMES_PER_BUFFER)
            ch1, ch2 = audio_tools.step_filter(self.window.cal, np.frombuffer(data, dtype=np.int16)[1::2], np.frombuffer(data, dtype=np.int16)[0::2])

            if heard_step:
                if hear_ago == 200:
                    if (np.mean(np.abs(ch1)) + np.mean(np.abs(ch2))>0):
                        angle = reg.predict([[(np.mean(np.abs(ch1)) - np.mean(np.abs(ch2))) / (
                                    np.mean(np.abs(ch1)) + np.mean(np.abs(ch2)))]])[0][0]
                        # angle = np.arcsin((np.mean(np.abs(ch1)) - np.mean(np.abs(ch2))) / (np.mean(np.abs(ch1)) + np.mean(np.abs(ch2))))
                        self.show_angle_trigger.emit(angle * 180 / np.pi)
                if hear_ago > self.window.cal.START_LISTENING_AGAIN:
                    heard_step = False
                    hear_ago = 0
                hear_ago += 1
            elif np.max(np.abs(ch1)) > self.window.cal.MIN_VOL or np.max(np.abs(ch2)) > self.window.cal.MIN_VOL:
                heard_step = True


