"""
This script shakes a 3D printer bed for a certain distance and records a video of the process using a USB camera.

Prerequisites:

1. Install Python: You need to have Python installed on your system. You can download Python from https://www.python.org/downloads/. However, prefered way to install Python is through Miniconda: https://docs.conda.io/en/latest/miniconda.html

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

7. Setup the lightbox on the 3d printer bed, clip it on with binder clips! Place a Stentor plate underneath the camera, and using "Photo Booth", "Cheese" (or a windows analog) aim and focus the camera on the drop of water inside the plate. Glue on a paper dot, or some sort of a marker near the plate (visible to the camera) to track movement of the plate.

    7.1. Try various lenses to get the best image (full frame image of the water droplet)

8. Check the TODO comments in the code!

Once these prerequisites are met, you can run the script from your terminal with 'python shake.py'
"""

import time
import serial
import subprocess
import datetime

# Define the port and baudrate for the printer
printer_port = '/dev/ttyUSB0'
baudrate = 115200

# Open serial connections
printer_ser = serial.Serial(printer_port, baudrate, timeout=1)

# Allow some time for printer to initialize
time.sleep(5)

# Define amplitude
amplitude = 0.5  # Distance in mm

# Define number of shakes
number_of_shakes = 5

# Define speed
speed = 5000  # Maximum speed in mm/min

# Get current date and time for video name
now = datetime.datetime.now()
date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

# Start the ffmpeg recording
# TODO: replace /dev/video0 with actual video device (for Peter it is /dev/video0)
cmd = f"ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 -vcodec rawvideo -pix_fmt yuv420p output_{date_string}.avi"

# TODO: try 100fps!
# cmd = f"ffmpeg -f v4l2 -framerate 100 -video_size 1280x720 -i /dev/video0 -vcodec rawvideo -pix_fmt yuv420p output_{date_string}.avi"

# Old, validated command - requires VLC to watch video
# cmd = "ffmpeg -f v4l2 -video_size 1280x720 -i /dev/video0 output.mp4"

# Run ffmpeg
p = subprocess.Popen(cmd, shell=True)
print(f"Recording {date_string}.mp4 (or .avi)")

# allow some time for camera to load
time.sleep(2)

# Set relative positioning
printer_ser.write(b'G91\n')

# Shake the bed
for _ in range(number_of_shakes):
    # Move in positive Y direction
    printer_ser.write('G1 Y{} F{}\n'.format(amplitude, speed).encode())
    time.sleep(amplitude/speed*60)  # Wait for the movement to complete

    # Move in negative Y direction
    printer_ser.write('G1 Y-{} F{}\n'.format(amplitude, speed).encode())
    time.sleep(amplitude/speed*60)  # Wait for the movement to complete

# Set back to absolute positioning
printer_ser.write(b'G90\n')

# allow extra time to finish shaking
time.sleep(3)

# Stop the ffmpeg recording
p.terminate()

# Close the printer serial connection
printer_ser.close()
