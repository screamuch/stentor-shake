"""
This script shakes a 3D printer bed for a certain distance and records a video of the process using a USB camera.

Prerequisites:

1. Install Python: You need to have Python installed on your system. You can download Python from https://www.python.org/downloads/.

2. Install the required Python packages:
   You can install them via pip (Python's package manager) by running the following command in your terminal:

   pip install pyserial opencv-python

   For some systems, you may need to use pip3 instead of pip.

3. Install ffmpeg: ffmpeg is a powerful tool that can be used for video recording and processing.

   On Ubuntu:
   sudo apt update
   sudo apt install ffmpeg

   On macOS (with Homebrew):
   brew install ffmpeg

   On Windows, download and install ffmpeg from: https://ffmpeg.org/download.html#build-windows.

4. Setup 3D printer: The 3D printer should be connected to the computer and should be accessible via a serial port.

5. Connect the USB camera: The USB camera should be properly connected to your computer.

6. Determine the path to your camera:

   On Linux, the path usually looks like /dev/videoN, where N is a number. You can check the available devices in the /dev directory.

   On macOS, the path can be obtained by using AVFoundation (https://developer.apple.com/av-foundation/).

   On Windows, the path can be obtained by checking the available devices in Device Manager under the "Sound, video and game controllers" or "Imaging devices" sections.

Once these prerequisites are met, you can run the script from your terminal with 'python script_name.py' (replace script_name.py with the name of this script).
"""

import time
import serial
import subprocess

# Define the port and baudrate for the printer
printer_port = '/dev/ttyUSB0'
baudrate = 115200

# Open serial connections
printer_ser = serial.Serial(printer_port, baudrate, timeout=1)

# Allow some time for printer to initialize
time.sleep(2)

# Define amplitude
amplitude = 1  # Distance in mm

# Define speed
speed = 5000  # Maximum speed in mm/min

# Start the ffmpeg recording
cmd = "ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 output.mp4"
p = subprocess.Popen(cmd, shell=True)

# Set relative positioning
printer_ser.write(b'G91\n')

# Shake the bed
# Move in positive Y direction
printer_ser.write('G1 Y{} F{}\n'.format(amplitude, speed).encode())
time.sleep(amplitude/speed*60)  # Wait for the movement to complete

# Move in negative Y direction
printer_ser.write('G1 Y-{} F{}\n'.format(amplitude, speed).encode())
time.sleep(amplitude/speed*60)  # Wait for the movement to complete

# Set back to absolute positioning
printer_ser.write(b'G90\n')

# Stop the ffmpeg recording
p.terminate()

# Close the printer serial connection
printer_ser.close()
