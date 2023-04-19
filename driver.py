from audio_utils import run_threads
from arduino_controller import create_commands, connect_arduino, sendCommand, setupTurntable, BUTTON_DELAY
from contextlib import closing
from time import sleep
from SignalProcessing import process_files
from os import listdir
from datetime import datetime

# default serial settings
BAUD = 115200

def main(play_file: str, rec_dir: str, angleStep: int, freq: int, port: str, baud = BAUD):
    '''
    Main driver that handles rotation, audio playback, audio recording, and plotting results.

    Parameters
    ----------
    play_file : str
        Path to file to send to speaker
    rec_dir : str
        Path to directory to store recorded data
    angleStep : int
        Angle increment in degrees
    freq : int
        Frequency to plot in Hz
    port : str
        Serial port that Arduino is connected to
    baud : str, optional
        Baud rate of Arduino Serial connection. This is always set to 115,200
    '''
    commands, batch_size = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        setupTurntable(arduino)
        for idx, (sleepTime, command) in enumerate(commands):
            # status of angle
            if is_int(360 / idx):
                print(f'Current angle: {360 // idx} degrees')
            
            # only execute audio if done rotating
            if idx % batch_size == 0:
                run_threads(play_file, rec_dir)
            
            sendCommand(sleepTime, command, arduino)

    print('test complete, beginning processing')
    process_files(angleStep, freq)


def rotate_only(angleStep: int, port: str, baud = BAUD):
    '''
    Debug function that only performs the rotation component of the test.
    
    Parameters
    ----------
    angleStep : int
        Angle increment in degrees
    port : str
        Serial port that Arduino is connected to
    baud : str, optional
        Baud rate of Arduino Serial connection. This is always set to 115,200
    '''
    commands, _ = create_commands(angleStep)

    with closing(connect_arduino(port, baud)) as arduino:
        setupTurntable(arduino)
        for sleepTime, command in commands:
            # sleep(max(0, BUTTON_DELAY - sleepTime))
            sendCommand(sleepTime, command, arduino)
            

    print('test complete')


def get_filenames_in_order(directory: str, limit=None) -> list:
    '''
    Gets list of filenames sorted in chronological order.

    Parameters
    ----------
    directory : str
        Directory from which to get files
    limit : int, optional
        Optional, number of files to return

    Returns
    -------
    List that contains filesnames sorted in chronological order, with a limit if given.
    '''
    filenames = listdir(directory)
    timestamps = []
    for filename in filenames:
        timestamp_str = filename.split('-')[-1].split('.')[0]
        timestamp = datetime.fromtimestamp(int(timestamp_str))
        timestamps.append((timestamp, filename))
    
    files = [filename for _, filename in sorted(timestamps)]
    return files[:limit] if limit else files


def is_int(val) -> bool:
    '''
    Checks if a value is an integer.

    Parameters
    ----------
    val
        Value to test as an integer

    Returns
    -------
    True if val is an integer, False otherwise
    '''
    try:
        int(val)
    except:
        return False
    
    return True

if __name__ == '__main__':
    rotate_only(1, 'COM7')
