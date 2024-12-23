import myTTT_STT as myTTT
from pynput import keyboard
import numpy as np
import sounddevice as sd


import sounddevice as sd

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def liveMic(input_device=None, output_device=None, channels=2, samplerate=None, blocksize=None, latency=None, dtype=None):
    try:
        with sd.Stream(device=(input_device, output_device),
                       samplerate=samplerate, blocksize=blocksize,
                       dtype=dtype, latency=latency,
                       channels=channels, callback=callback):
            print('#' * 80)
            print('Press Enter to quit')
            print('#' * 80)
            input()
    except KeyboardInterrupt:
        print("Interrupted by user.")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # List devices
    print("Available audio devices:")
    print(sd.query_devices())
    
    # Set your desired device indices or pass None for defaults
    liveMic(input_device=3, output_device=10)





















if __name__ == '__main__':
  
  Audio = myTTT.Audio
  Audio1 = Audio()
    