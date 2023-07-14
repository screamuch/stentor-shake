# stentor-shake
A collection of scripts to shake *Stentor coeruleus* and image results using Robocam

`all scripts use Python 3.8 but, chances are, will work even with Python 3.12`

## Usage
`shake.py` -> follow instructions in this file.

## Extras
`Untitled.ipynb` -> here are acceleration values at different printer bed displacements. You can either use these, or record your own. To run this code you will need to run the following two files:

`accelerometer_test.ino` -> Arduino code to record G-force every 20ms and send it to the computer via serial port.

`shake_and_record_accelerometer.py` -> Python script to shake the 3D printer's Y-axis and record accelerometer values from the Arduino during the shake.

## Acknowledgement
This software is developed by Peter A. Chudinov, is currently unlicensed and provided as is. This work is funded by the National Science Foundation (NSF) grant No. DBI-1548297, Center for Cellular Construction. Disclaimer: Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the National Science Foundation.
