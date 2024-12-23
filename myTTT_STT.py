import sounddevice as sd
import time as t
#import matplotlib.pyplot as plt

# get sound devices
# set sound device input and output
# store sound chunks in an array using numpy and linspace
# from array take chunk of a certain amount (word aware) feed it to wisper
# take that trascribed and then translate it
# output tranlated and transcribed (make it optional) terminal or 

import sounddevice as sd

class Audio:
    def __init__(self, audio_file=None, input_device_num=None, output_device_num=None, playback=False):
        self.audio_file = audio_file  # Takes in an audio file .wav
        self.input_device_num = input_device_num  # Sets input device
        self.output_device_num = output_device_num  # Sets output device
        self.playback = playback  # True or false plays audio or not

        # Initialize default devices
        if self.input_device_num is None:
            self.input_device_num = sd.default.device[0]
        else:
            sd.default.device = (self.input_device_num, sd.default.device[1])

        if self.output_device_num is None:
            self.output_device_num = sd.default.device[1]
        else:
            sd.default.device = (sd.default.device[0], self.output_device_num)

    # Set the input device
    def set_input_device(self, set_input_device_num=None):
        if set_input_device_num is not None:
            sd.default.device = (int(set_input_device_num), sd.default.device[1])
            self.input_device_num = int(set_input_device_num)
        return self.get_default_input_device()

    # Set the output device
    def set_output_device(self, set_output_device_num=None):
        if set_output_device_num is not None:
            sd.default.device = (sd.default.device[0], int(set_output_device_num))
            self.output_device_num = int(set_output_device_num)
        return self.get_default_output_device()

    # Set input device to default
    def set_default_input_device(self):
        default_input_device_index = sd.default.device[0]
        device_info = sd.query_devices(default_input_device_index)
        if device_info['max_input_channels'] > 0:
            self.input_device_num = default_input_device_index
            return self.input_device_num
        else:
            raise ValueError(f"Device at index {default_input_device_index} does not support input.")

    # Set output device to default
    def set_default_output_device(self):
        default_output_device_index = sd.default.device[1]
        device_info = sd.query_devices(default_output_device_index)
        if device_info['max_output_channels'] > 0:
            self.output_device_num = default_output_device_index
            return self.output_device_num
        else:
            raise ValueError(f"Device at index {default_output_device_index} does not support output.")


    # Get the list of input devices
    def get_input_devices(self, listview=False):
        devices = sd.query_devices()
        device_list = [
            {
                'name': device['name'],
                'index': device['index'],
                'input': device['max_input_channels'],
                'output': device['max_output_channels']
            }
            for device in devices if device['max_input_channels'] > 0
        ]
        device_list.sort(key=lambda x: x['name'])

        if listview == 'print':
            print('Available Input Devices:')
            for d in device_list:
                print(f"{d['name']} - index: {d['index']} - input: {d['input']} - output: {d['output']}")
        else:
            return device_list

    # Get the list of output devices
    def get_output_devices(self, listview=False):
        devices = sd.query_devices()
        device_list = [
            {
                'name': device['name'],
                'index': device['index'],
                'input': device['max_input_channels'],
                'output': device['max_output_channels']
            }
            for device in devices if device['max_output_channels'] > 0
        ]
        device_list.sort(key=lambda x: x['name'])

        if listview == 'print':
            print('Available Output Devices:')
            for d in device_list:
                print(f"{d['name']} - index: {d['index']} - input: {d['input']} - output: {d['output']}")
        else:
            return device_list

    # Get the default input device
    def get_default_input_device(self, listview=False):
        if listview == 'print':
            print(f"Default input device index: {sd.default.device[0]}")
        return int(sd.default.device[0])

    # Get the default output device
    def get_default_output_device(self, listview=False):
        if listview == 'print':
            print(f"Default output device index: {sd.default.device[1]}")
        return int(sd.default.device[1])
#------------------------------------------------------------------------------------------
#-----------------------------------LIVE MIC-----------------------------------------------
#------------------------------------------------------------------------------------------
    def live_mic(self, channels=2, samplerate=None, blocksize=None, latency=None, dtype=None):
        def callback(indata, outdata, frames, time, status):
            if status:
                print(status)
            outdata[:] = indata

        try:
            with sd.Stream(
                device=(self.input_device_num, self.output_device_num),
                samplerate=samplerate,
                blocksize=blocksize,
                dtype=dtype,
                latency=latency,
                channels=channels,
                callback=callback,
            ):
                print("#" * 80)
                print("Press Enter to quit")
                print("#" * 80)
                input()
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
#------------------------------------------------------------------------------------------
#-----------------------------------Play Audio File-----------------------------------------------
#------------------------------------------------------------------------------------------
    # Play an audio file
    def play_audio_file(self, audio_file=None):
        if not audio_file and not self.audio_file:
            raise ValueError("No audio file provided.")
        file_to_play = audio_file or self.audio_file

        try:
            data, samplerate = sf.read(file_to_play)
            print(f"Playing audio file: {file_to_play}")
            sd.play(data, samplerate=samplerate, device=self.output_device_num)
            sd.wait()  # Wait until the playback is finished
        except Exception as e:
            print(f"Error playing audio file: {type(e).__name__}: {e}")

if __name__ == '__main__':
  # Initialize Audio
  #3 is the input device from headset mic and 10 is the output device to asus
    audio = Audio(False,3, 10,False)

    try:
        file_path = "example_audio.wav"  # Replace with your audio file path
        audio.play_audio_file(file_path)
    except ValueError as e:
        print(e)

    # Start live mic streaming
    print("Starting live microphone streaming...")
    # Start live mic streaming
    print("Starting live microphone streaming...")
    