from typing import List, Tuple
from time import sleep
from serial import Serial

CONTINUOUS_SPEED = 1 / 60 * 360 # deg/sec
BUTTON_DELAY = 3.5 # sec
DEGREE_THRESHOLD = CONTINUOUS_SPEED * BUTTON_DELAY

# codes
ONE_DEGREE = '1'
PLAY_PAUSE = 'p'
SET_ORIGIN = 's'
GO_ORIGIN = 'o'
CCW = 'a'
CW = 'd'
HALF_CIRCLE = 'f' # 180 deg
SLOWER = 'q'
FASTER = 'e'


def sendCommand(startDelay: float, command: str, arduino: Serial):
    sleep(startDelay)

    print(f'Sleep: {startDelay}\tCommand: {command}')
    arduino.write(command.encode())


def setupTurntable(arduino: Serial):
    minimizeSpeed(arduino)
    
    # make sure it's going CW
    sendCommand(BUTTON_DELAY, SET_ORIGIN, arduino)
    sendCommand(BUTTON_DELAY, CCW, arduino)
    sendCommand(BUTTON_DELAY, GO_ORIGIN, arduino)


def minimizeSpeed(arduino: Serial):
    sleep(3) # give arduino time to init
    for _ in range(10):
        sendCommand(BUTTON_DELAY, SLOWER, arduino)


def create_commands(angleStep: int) -> Tuple[List[Tuple[float, str]], int]:
    '''
    Creates a list of commands that will be sent to the Arduino.

    Parameters
    ---------
    angleStep : int
        User-defined angle increment

    Returns
    -------
    commands : List[Tuple[float, str]]
        List containing tuples of commands, where the tuple is of the form (sleepTime, command). sleepTime is the time to sleep the current thread before executing its respective command
    
    batch_size: int
        Number of commands needed per iteration
    '''

    commands = []
    batch_size = 0
    
    if angleStep <= DEGREE_THRESHOLD:
        # one degree button angleStep times
        batch_size = angleStep

        commands = [(BUTTON_DELAY, ONE_DEGREE)] * 360
    else:
        # play/pause for enough time
        rotationTime = angleStep / CONTINUOUS_SPEED
        batch_size = 2

        commands = [(0.5, PLAY_PAUSE), (rotationTime, PLAY_PAUSE)] * (360 // angleStep)
    
    return commands, batch_size

def connect_arduino(port: str, baud: int):
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
    commands, batch_size = create_commands(30)
    print(len(commands))
    print(commands)