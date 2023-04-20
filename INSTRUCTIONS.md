# Instructions for the User

## Automatic Characterization Test

1. Set up the hardware  
    - Attach the IR LED to the Arduino board by grounding the GRND label, connecting 5V to VCC, and attaching the DAT pin to pin 3. Ensure that the IR transmitter is in line with the IR receiver on the turntable so that commands can be sent.  
    - If desired, connect the laser module to the Arduino, black to ground and red to digital pin 5.  
    - Connect the Arduino board to a dedicated computer (PC) via USB.  
    - Connect the turntable's power supply and turn it on.  
    - •	Place the microphone on top of the turntable and perform the alignment procedure towards the speaker. For more accurate beam plotting, ensure that the sensor on the microphone is aligned with the vertical axis which the turntable rotates about.  
    - •	Connect the audio interface to your computer. Then, make sure to connect the microphone to the audio interface via the input port and the speaker to the ‘Monitor’ output port. On your computer, ensure that the speaker and microphone are connected and set as the default devices.  
2. Clone or download the repository on [GitHub](https://github.com/alexgobert/utme-acoustic/)  
3. Install the required packages by running `pip3 install -r requirements.txt` in the command line.  
4. Open the `IR/ir_transmitter.ino` file and upload it to the Arduino. You can test its functionality by opening the Serial Monitor, setting the BAUD rate to 115200, and entering commands such as `p` for pause and play. This should start moving the turntable.  
5. In the Serial Monitor at 115200 BAUD, send `p` to begin continuous rotation of the turntable. Send ‘P’ again when the 0-degree marker is in line with the red operation LED of the turntable. Send ‘S’ to set the origin there.  
6. Run the `main_gui.py` script using Python 3. You can do this by navigating to the project directory in the command line and typing `python3 main_gui.py` or by using an integrated development environment (IDE) such as PyCharm.  
7. Use the "Browse" buttons in the GUI to select the test audio file (white/pink noise, or frequency sweeps) and the directory (where you save the recorded audio files). For ease of use, it is recommended to create a new recording folder for each test run.  
8. Enter the angle increment you want to use for the test. This is the amount by which the turntable will be rotated between each recording.  
9. Using the dropdown menu, set the `PORT` to the serial port where the Arduino board is connected.  
10. Input a frequency in the “Frequency” field. The program will output a beam pattern plot of this frequency at the end of the test. After the test, you can change the frequency and generate different plots of those frequencies.  
11. Click the "Play" button to start the test. The turntable will begin rotating and the audio file will be played. The microphone will record the audio, and the recorded files will be saved in the directory you specified.  
12. Once the test is complete, the program will output a message saying "test complete" in the console.  

## Plotting

1. In the GUI, ensure that the recording directory is specified to where the WAV files are located.
2. Input the desired frequency to be plotted in the corresponding text field.  
3. Hit the “Plot Only” button to generate a plot of your desired frequency. If this is done with multiple frequencies from the same broadband recording data set, then the Beam pattern will be plotted on the same figure.  
