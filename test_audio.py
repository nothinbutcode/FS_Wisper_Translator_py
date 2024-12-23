# Description: Test the audio class in g.py
#from g import Audio

if __name__ == '__main__':
    audio1 = Audio()
    audio2 = Audio(input_device_num=1, output_device_num=6)

    # # Test getting the default input and output devices
    # default_input_device1 = audio1.get_default_input_device('print')
    # default_output_device1 = audio1.get_default_output_device('print')
    # print(default_input_device1)
    # print(default_output_device1)

    # default_input_device2 = audio2.get_default_input_device('print')
    # default_output_device2 = audio2.get_default_output_device('print')
    # print(default_input_device2)
    # print(default_output_device2)

    # Test setting the default input and output devices
    # set_input_device1 = audio1.set_default_input_device()
    # set_output_device1 = audio1.set_default_output_device()
    # print(set_input_device1)
    # print(set_output_device1)

    set_input_device2 = audio2.set_default_input_device()
    set_output_device2 = audio2.set_default_output_device()
    print(set_input_device2)
    print(set_output_device2)

    

    #set ouput device
    set_output_device2 = audio1.set_output_device(5)
    print(set_output_device2)
    #set input device
    set_input_device2 = audio1.set_input_device(5)
    print(set_input_device2)

# Test getting the list of input and output devices
    input_devices = audio1.get_input_devices('print')
    output_devices = audio1.get_output_devices('print') 
    print(input_devices)
    print(output_devices)
    input_devices = audio2.get_input_devices('print')
    output_devices = audio2.get_output_devices('print')
    print(input_devices)
    print(output_devices)