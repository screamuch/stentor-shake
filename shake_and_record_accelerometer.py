import time
import serial

# Start the timer
start_time = time.time()

# Define the port and baudrate for the printer and the accelerometer
printer_port = '/dev/ttyUSB0'
accelerometer_port = '/dev/ttyACM0'
baudrate = 115200

# Open serial connections
printer_ser = serial.Serial(printer_port, baudrate, timeout=1)
accelerometer_ser = serial.Serial(accelerometer_port, baudrate, timeout=1)

# Allow some time for printer to initialize
time.sleep(2)

# Define different amplitudes
amplitudes = [0.1, 0.2, 0.5, 1, 2, 5, 10]

# Define speed
speed = 5000  # Maximum speed in mm/min

# Set relative positioning
printer_ser.write(b'G91\n')

# Shake the bed
for i, amplitude in enumerate(amplitudes):
    # so plot starts flat
    time.sleep(0.5)

    for _ in range(5):  # Repeat each amplitude 5 times
        # Move in positive Y direction
        printer_ser.write('G1 Y{} F{}\n'.format(amplitude, speed).encode())
        time.sleep(amplitude/speed*60)  # Wait for the movement to complete

        # Move in negative Y direction
        printer_ser.write('G1 Y-{} F{}\n'.format(amplitude, speed).encode())
        time.sleep(amplitude/speed*60)  # Wait for the movement to complete

    # Read accelerometer data
    end_time = time.time() + 3  # Define end time 3 seconds from now
    data = ""  # Initialize data string
    while time.time() < end_time:
        data += accelerometer_ser.read(accelerometer_ser.in_waiting).decode()

    # Write all data to a text file
    with open(f'accelerometer_data_{amplitude}.csv', 'w') as file:
        file.write(data)

# Set back to absolute positioning
printer_ser.write(b'G90\n')

# Close the printer serial connection
printer_ser.close()

# Close accelerometer serial connection
accelerometer_ser.close()
