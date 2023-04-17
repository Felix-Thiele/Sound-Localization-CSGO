import pyaudio
import pyaudiowpatch
import wave
import matplotlib.pyplot as plt
import numpy as np
import win32api
import time


def step_filter(adata: np.ndarray, bandlimit: int =2000, sampling_rate: int = 44100) -> np.ndarray:

    bandlimit_index = int(bandlimit * adata.size / sampling_rate)
    fsig = np.fft.fft(adata)

    fsig[bandlimit_index + 1: len(fsig) - bandlimit_index] = 0

    adata_filtered = np.fft.ifft(fsig)

    return np.real(adata_filtered)

def calibrate_mouse():
    # Use this function to calculate how much mouse movement 360 degree in csgo is
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Left button down = 0 or 1. Button up = -127 or -128
    hor_movement = 0
    click_nr = True
    sample = 0
    while True:
        x, y = win32api.GetCursorPos()
        hor_movement += x - 1280
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)
        if a != state_left:
            state_left = a
            if a < 0:
                if click_nr:
                    if sample > 0:
                        print(hor_movement)
                    sample += 1
                    hor_movement = 0

                click_nr = not click_nr


        elif b != state_right:
            break
        time.sleep(.001)

def record_samples(FILENAME):
    """ Use this function to record sound.
    I did this in https://steamcommunity.com/sharedfiles/filedetails/?id=697998669&searchtext=sound.
    This function records sound when left mouse is pressed, does nothing at the next press, and then repeats.
    Additionally during every seccond click, starting at the third click, the mouse movement tracked since the last iteration is saved.
    """
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Left button down = 0 or 1. Button up = -127 or -128
    hor_movement = 0
    click_nr = True
    sample = 0
    while True:
        x, y = win32api.GetCursorPos()
        hor_movement += x - 1280
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)
        if a != state_left:
            state_left = a
            if a < 0:
                if click_nr:
                    if sample>0:
                        with open(FILENAME + '.txt', 'a+') as f:
                            f.write(FILENAME + str(sample) + ".wav" + " | " + str(hor_movement)  + " | guess degree: "+ str(hor_movement/5000*365) + "\n")
                            print('saving mouse movement.')
                    sample += 1
                    hor_movement = 0
                    print('\ncollecting mouse movement:')
                    record_out(FILENAME + str(sample) + ".wav", 0.5)

                click_nr = not click_nr


        elif b != state_right:
            break

        time.sleep(.001)


def play_wav(wav_file = "output.wav"):
    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(wav_file, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

        # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


# https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_record_wasapi_loopback.py
def record_out(outfile=None,seconds=3):
    FORMAT = pyaudio.paInt16
    p = pyaudiowpatch.PyAudio()

    try:
        # Get default WASAPI info
        wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
    except OSError:
        print("Looks like WASAPI is not available on the system. Exiting...")
        exit()

    # Get default WASAPI speakers
    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

    if not default_speakers["isLoopbackDevice"]:
        for loopback in p.get_loopback_device_info_generator():
            if default_speakers["name"] in loopback["name"]:
                default_speakers = loopback
                break
        else:
            print('Loopback not found')
    print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")

    CHANNELS = default_speakers["maxInputChannels"]
    RATE = int(default_speakers["defaultSampleRate"])
    FRAMES_PER_BUFFER = pyaudio.get_sample_size(FORMAT)

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=FRAMES_PER_BUFFER,
                input=True,
                input_device_index=default_speakers["index"]
                )
    frames = []
    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
    stream.stop_stream()
    stream.close()

    if outfile:
        write_to_wav(frames, CHANNELS, p.get_sample_size(FORMAT), FORMAT, RATE, outfile)

    return frames





def record_mic(seconds=3, outfile=None):

    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )
    frames = []
    second_tracking = 0
    second_count = 0
    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
        second_tracking += 1
        if second_tracking == RATE / FRAMES_PER_BUFFER:
            second_count += 1
            second_tracking = 0
            print(f'Time Left: {seconds - second_count} seconds')
    stream.stop_stream()
    stream.close()

    if outfile:
        write_to_wav(frames, CHANNELS, p.get_sample_size(FORMAT), FORMAT, RATE, outfile)

    return frames


def write_to_wav(frames, CHANNELS, SAMPLESIZE, FORMAT, RATE, outfile= "output.wav"):

    with wave.open(outfile, 'wb') as obj:
        obj.setnchannels(CHANNELS)
        obj.setsampwidth(SAMPLESIZE)
        obj.setframerate(RATE)
        obj.writeframes(b''.join(frames))


def wav_to_np(outfile = "output.wav"):
    with wave.open(outfile, 'rb') as file:
        sample_freq = file.getframerate()
        frames = file.getnframes()
        channels = file.getnchannels()
        signal_wave = file.readframes(-1)

    time = frames / sample_freq

    audio_signals = []
    for channel in range(channels):
        audio_signals.append(np.frombuffer(signal_wave, dtype=np.int16)[channel::channels])
    return audio_signals


def plot(outfile = "output.wav"):
    with wave.open(outfile, 'rb') as file:
        sample_freq = file.getframerate()
        frames = file.getnframes()
        channels = file.getnchannels()
        signal_wave = file.readframes(-1)

    time = frames / sample_freq

    fig, axs = plt.subplots(channels+1, figsize=(15, 4*channels))
    for channel in range(channels):
        audio_array = np.frombuffer(signal_wave, dtype=np.int16)[channel::channels]
        times = np.linspace(0, time, num=len(audio_array))
        axs[channels].plot(times, audio_array)
        axs[channel].plot(times, audio_array)
        axs[channel].plot(times, audio_array)
        axs[channel].set_title(outfile+" channel: "+ str(channel))

    plt.show()
