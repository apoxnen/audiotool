import pyaudio
import wave
import keyboard  # using module keyboard
import demucs
from time import time

# Record in chunks of 1024 samples
chunk = 1024 
 
# 16 bits per sample
sample_format = pyaudio.paInt16 
chanels = 2
 
# Record at 44400 samples per second
smpl_rt = 44400 

timeout = 60000 # value in ms
 
# Create an interface to PortAudio
pa = pyaudio.PyAudio() 
dev_index = 3

print("Setting index for audio mixer")

for i in range(pa.get_device_count()):
    dev = pa.get_device_info_by_index(i)
    if (dev['name'] == 'Stereo Mix (Realtek HD Audio Stereo input)' and dev['hostApi'] == 0):
        dev_index = dev['index']
        print('dev_index', dev_index)

stream = pa.open(format=sample_format, channels=chanels,
                 rate=smpl_rt, input=True,
                 input_device_index = dev_index,
                 frames_per_buffer=chunk)
 
print('Recording...')
 
# Initialize array that be used for storing frames
frames = [] 
start_time = time()
current_time = time()

# Record audio until space is pressed
while (current_time - start_time) < timeout:

    # Record data audio data
    data = stream.read(chunk)
    # Add the data to a buffer (a list of chunks)
    frames.append(data)

    # Get new timestamp
    current_time = time()

    # If q is pressed, advance to next part of the experiment
    if keyboard.is_pressed('q'):
        # Record data audio data
        data = stream.read(chunk)
        # Add the data to a buffer (a list of chunks)
        frames.append(data)
        break

else:
    # Record data audio data
    data = stream.read(chunk)
    # Add the data to a buffer (a list of chunks)
    frames.append(data)


# Stop and close the stream
stream.stop_stream()
stream.close()
 
# Terminate - PortAudio interface
pa.terminate()
 
print('Done recording!')
 
# Save the recorded data in a .wav format
filename = "recording.wav"
sf = wave.open(filename, 'wb')
sf.setnchannels(chanels)
sf.setsampwidth(pa.get_sample_size(sample_format))
sf.setframerate(smpl_rt)
sf.writeframes(b''.join(frames))
sf.close()