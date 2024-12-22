import numpy as np
import sounddevice as sd
import time as t
#import matplotlib.pyplot as plt

# get sound devices
# set sound device input and output
# store sound chunks in an array using numpy and linspace
# from array take chunk of a certain amount (word aware) feed it to wisper
# take that trascribed and then translate it
# output tranlated and transcribed (make it optional) terminal or 

class  Audio:
    def __init__(self,audio_file =None, input_device_num=None, output_device_num=None, playback=False):
        self.audio_file= audio_file # takes in and audio file .wav
        self.input_device_num= input_device_num # int sets device input
        self.output_device_num= output_device_num # int sets device input
        self.playback= playback # # True or false plays audio or not

    #GET METHODS
    def get_devices(self):
        devices = sd.query_devices()  # Get the list of all devices
        device_list = []  # Create an empty list to store device details
        
        for device in devices:
            # Append the device details as a dictionary to the device_list
            device_list.append({
                'name': device['name'],
                'index': device['index'],
                'input': device['max_input_channels'],
                'output': device['max_output_channels']
            })

        # Sort the list of devices by the 'name' key (alphabetically)
        device_list.sort(key=lambda x: x['name'])  # You can also use sorted(device_list, key=lambda x: x['name'])
        for d in device_list: print(d['name'],'index:',{ d['index']},'input:',d['input'],'output:',d['output'])  # Return the list of devices

    #SET METHODS


#Main Function
if __name__ == '__main__':

    # Start the timer
    start_time = t.time()

    audio = Audio()
    devices = audio.get_devices()
    
    # End the timer
    end_time = t.time()

    # Print the devices and the execution time
    print(devices)
    print(f"Execution Time: {end_time - start_time} seconds")


