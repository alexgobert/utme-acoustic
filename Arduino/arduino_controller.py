# from ArduinoDAQ import SerialConnect
from typing import List, Tuple
from time import sleep
from serial import Serial

# default serial settings
PORT = 'COM7'
BAUD = 9600

DEGREE_THRESHOLD = 5
CONTINUOUS_SPEED = 40 # deg/sec TODO: determine default speed
BUTTON_DELAY = 1
PLAY_PAUSE = 'p'
ONE_DEGREE = '1'

def startRotate(commands: List[Tuple[float, str]], arduino: Serial):

    for time, command in commands:
        sleep(time)

        arduino.write(command.encode())
        

def createCommands(angleStep: int, recordDelay: float) -> List[Tuple[float, str]]:
    '''
    Creates a list of commands that will be sent to the Arduino.

    Parameters
    ---------
    angleStep : int
        User-defined angle increment
    recordDelay : float
        Seconds to wait before proceeding to next increment

    Returns
    -------
    commands : List[Tuple[float, str]]
        List containing tuples of commands, where the tuple is of the form (sleepTime, command). sleepTime is the time to sleep the current thread before executing its respective command
    '''

    commands = []
    
    if angleStep < DEGREE_THRESHOLD:
        # one degree button angleStep times
        
        for _ in range(0, 360 + angleStep, angleStep):
            commands.append((recordDelay, ONE_DEGREE))
            [commands.append(BUTTON_DELAY, ONE_DEGREE) for _ in range(angleStep)]
    else:
        # play/pause for enough time
        rotationTime = angleStep / CONTINUOUS_SPEED

        for _ in range(0, 360 + angleStep, angleStep):

            commands.append((recordDelay, PLAY_PAUSE)) # start rotation
            commands.append((rotationTime, PLAY_PAUSE)) # stop rotation
    
    return commands

def connectToArduino(port: str, baud: int):
    '''
    Attempts to connect to Arduino through the serial port and sends the acquistion data rate to the Arduino
    '''
    serialConnection = None

    print(f'Trying to connect to: {port} at {baud} BAUD.')
    try:
        serialConnection = Serial(port, baud, timeout=4)
        print(f'Connected to {port} at {baud} BAUD.')
    except:
        print(f'Failed to connect with {port} at {baud} BAUD.')

    if serialConnection:
        serialConnection.reset_input_buffer()

    return serialConnection

if __name__ == '__main__':
    # commands = createCommands(10, 1)
    commands = createCommands(1, )
    print(commands)