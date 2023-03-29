from ArduinoDAQ import SerialConnect
from typing import List, Dict

PORT = 'COM7'
BAUD = 9600
DEGREE_THRESHOLD = 5
CONTINUOUS_SPEED = 40 # deg/sec
BUTTON_DELAY = 1
PLAY_PAUSE = 'p'
ONE_DEGREE = '1'

def createCommands(angleStep: int, recordDelay: int) -> Dict[str, List]:
    '''
    Creates a list of commands that will be sent to the Arduino.

    Parameters
    ---------
    angleStep : int
        User-defined angle increment
    recordDelay : int
        Time to wait before proceeding to next increment

    Returns
    -------
    commandDict : dict
        Dictionary containing command information. Keys are 'time', 'command', and 'value'
    commandTimes : list
        List of times to send Arduino commands
    commandTypes : list
        List of command keys to send
    '''

    commandTimes = []
    commandTypes = []
    
    if recordDelay < DEGREE_THRESHOLD:
        # one degree button angleStep times
        
        pass
    else:
        # play/pause for enough time
        rotationTime = angleStep / CONTINUOUS_SPEED

        for i in range(0, 360 + angleStep, angleStep):
            # TODO: derive time formula
            commandTimes.append(i * (1 + rotationTime + recordDelay))
            commandTypes.append(PLAY_PAUSE)
    
    return {'time': commandTimes, 'command': commandTypes}