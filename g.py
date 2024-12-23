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


if __name__ == '__main__':
    # Initialize audio objects
    audio1 = Audio()
    audio2 = Audio(input_device_num=6, output_device_num=2)

    # Test getting the default input and output devices
    default_input_device1 = audio1.get_default_input_device('print')
    default_output_device1 = audio1.get_default_output_device('print')

    default_input_device2 = audio2.get_default_input_device('print')
    default_output_device2 = audio2.get_default_output_device('print')

    # Test setting the default input and output devices
    set_input_device1 = audio1.set_default_input_device()
    set_output_device1 = audio1.set_default_output_device()

    set_input_device2 = audio2.set_default_input_device()
    set_output_device2 = audio2.set_default_output_device()

    print(f"Audio1 Default Input: {set_input_device1}, Default Output: {set_output_device1}")
    print(f"Audio2 Default Input: {set_input_device2}, Default Output: {set_output_device2}")
